from fastapi import FastAPI, File, UploadFile, HTTPException, Form
from fastapi.middleware.cors import CORSMiddleware
from model import VehicleRecognizer
import time
import io
import os

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

model_cache = {}
vehicle_types = ["AITO问界", "奥迪", "宝马", "奔驰", "本田", "大众", "东风风行", "东风纳米", "丰田", "吉利银河", "雷克萨斯", "理想汽车", "日产", "特斯拉", "星途"]

def get_recognizer(model_name):
    if model_name not in model_cache:
        model_cache[model_name] = VehicleRecognizer(f"../models/{model_name}")
    return model_cache[model_name]

@app.get("/health")
async def health():
    return {"status": "ok"}

@app.get("/api/models")
async def get_models():
    models_dir = "../models"
    if not os.path.exists(models_dir):
        return {"models": []}
    models = [f for f in os.listdir(models_dir) if f.endswith('.pt')]
    return {"models": models}

@app.post("/api/recognize")
async def recognize(image: UploadFile = File(...), model_name: str = Form("v3.pt")):
    if image.content_type not in ["image/jpeg", "image/png"]:
        raise HTTPException(400, "Invalid file format")

    contents = await image.read()
    if len(contents) > 5 * 1024 * 1024:
        raise HTTPException(400, "File too large")

    recognizer = get_recognizer(model_name)
    start_time = time.time()
    predicted_idx, confidence = recognizer.predict(io.BytesIO(contents))
    processing_time = time.time() - start_time

    vehicle_type = vehicle_types[predicted_idx] if predicted_idx < len(vehicle_types) else f"类型{predicted_idx}"

    return {
        "success": True,
        "vehicle_type": vehicle_type,
        "confidence": round(confidence, 2),
        "processing_time": round(processing_time, 2),
        "model_used": model_name
    }
