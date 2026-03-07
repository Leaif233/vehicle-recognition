from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from model import VehicleRecognizer
import time
import io

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

recognizer = VehicleRecognizer("../v3.pt")

vehicle_types = ["轿车", "SUV", "MPV", "跑车", "皮卡", "客车", "货车"]

@app.get("/health")
async def health():
    return {"status": "ok"}

@app.post("/api/recognize")
async def recognize(image: UploadFile = File(...)):
    if image.content_type not in ["image/jpeg", "image/png"]:
        raise HTTPException(400, "Invalid file format")

    contents = await image.read()
    if len(contents) > 5 * 1024 * 1024:
        raise HTTPException(400, "File too large")

    start_time = time.time()
    predicted_idx, confidence = recognizer.predict(io.BytesIO(contents))
    processing_time = time.time() - start_time

    vehicle_type = vehicle_types[predicted_idx] if predicted_idx < len(vehicle_types) else f"类型{predicted_idx}"

    return {
        "success": True,
        "vehicle_type": vehicle_type,
        "confidence": round(confidence, 2),
        "processing_time": round(processing_time, 2)
    }
