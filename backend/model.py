import torch
from PIL import Image
from torchvision import transforms

class VehicleRecognizer:
    def __init__(self, model_path):
        self.device = torch.device('cpu')
        checkpoint = torch.load(model_path, map_location=self.device, weights_only=False)
        self.model = checkpoint if not isinstance(checkpoint, dict) else checkpoint.get('model', checkpoint.get('ema', checkpoint))
        self.model.float()
        self.model.eval()

        self.transform = transforms.Compose([
            transforms.Resize((224, 224)),
            transforms.ToTensor(),
            transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
        ])

    def predict(self, image_bytes):
        image = Image.open(image_bytes).convert('RGB')
        input_tensor = self.transform(image).unsqueeze(0).to(self.device)

        with torch.no_grad():
            output = self.model(input_tensor)
            if isinstance(output, (list, tuple)):
                output = output[0]
            probabilities = output.squeeze()
            print(f"概率分布: {probabilities}")
            confidence, predicted = torch.max(probabilities, 0)
            print(f"预测: idx={predicted.item()}, conf={confidence.item()}")

        return predicted.item(), confidence.item()
