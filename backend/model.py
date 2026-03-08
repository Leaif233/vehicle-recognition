import torch
from PIL import Image
from torchvision import transforms

class VehicleRecognizer:
    def __init__(self, model_path):
        self.device = torch.device('cpu')
        self.model = torch.load(model_path, map_location=self.device, weights_only=False)
        self.model.eval()

        self.transform = transforms.Compose([
            transforms.Resize((224, 224)),
            transforms.ToTensor(),
            transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
        ])

        # 测试获取输出类别数
        test_input = torch.randn(1, 3, 224, 224).to(self.device)
        with torch.no_grad():
            test_output = self.model(test_input)
            if isinstance(test_output, (list, tuple)):
                test_output = test_output[0]
            self.num_classes = test_output.shape[-1]
            print(f"模型输出类别数: {self.num_classes}")

    def predict(self, image_bytes):
        image = Image.open(image_bytes).convert('RGB')
        input_tensor = self.transform(image).unsqueeze(0).to(self.device)

        with torch.no_grad():
            output = self.model(input_tensor)
            print(f"模型输出: {output}")
            probabilities = output[0]
            confidence, predicted = torch.max(probabilities, 0)
            print(f"预测索引: {predicted.item()}, 置信度: {confidence.item()}")

        return predicted.item(), confidence.item()
