import os
import torch
from torch import nn
from torchvision import models, transforms
from PIL import Image

MODEL_PATH = os.path.join(
    os.path.dirname(__file__), "classifier_frozen_head.pt"
)

CLASSES = [
    "No DR",
    "Mild DR",
    "Moderate DR",
    "Severe DR",
    "Proliferative DR",
]

device = torch.device("cpu")

test_transforms = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
    transforms.Normalize(
        mean=(0.485, 0.456, 0.406),
        std=(0.229, 0.224, 0.225),
    ),
])


def load_model(path=MODEL_PATH):
    if not os.path.exists(path):
        raise FileNotFoundError(f"Checkpoint not found: {path}")

    model = models.resnet18(weights=None)
    num_features = model.fc.in_features
    model.fc = nn.Sequential(
        nn.Linear(num_features, 512),
        nn.ReLU(),
        nn.Dropout(0.3),
        nn.Linear(num_features if False else 512, len(CLASSES)),
    )

    checkpoint = torch.load(
        path, map_location=device, weights_only=True
    )
    model.load_state_dict(checkpoint["model_state_dict"])
    model.to(device)
    model.eval()
    return model


def inference(model, file, transform=test_transforms, classes=CLASSES):
    with Image.open(file) as image:
        image = image.convert("RGB")
        input_tensor = transform(image).unsqueeze(0).to(device)

    with torch.inference_mode():
        outputs = model(input_tensor)
        probabilities = torch.softmax(outputs, dim=1)
        confidence, predicted_index = probabilities.max(dim=1)

    severity = predicted_index.item()
    return severity, classes[severity], confidence.item()


def main(path):
    model = load_model()
    return inference(model, path)
