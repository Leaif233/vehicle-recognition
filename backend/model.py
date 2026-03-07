import torch
from PIL import Image
from torchvision import transforms

class VehicleRecognizer:
    def __init__(self, model_path):
        self.device = torch.device('cpu')
        self.model = torch.load(model_path, map_location=self.device)
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
            probabilities = torch.nn.functional.softmax(output[0], dim=0)
            confidence, predicted = torch.max(probabilities, 0)

        return predicted.item(), confidence.item()
