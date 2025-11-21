import torch
import torch.nn as nn
from torchvision import transforms
from torchvision.models import resnet18, ResNet18_Weights
from PIL import Image
import warnings
import os


warnings.simplefilter(action='ignore', category=FutureWarning)

# Set up
classes = [
    'battery', 'biological', 'brown-glass', 'cardboard', 'clothes',
    'green-glass', 'metal', 'paper', 'plastic', 'shoes', 'trash', 'white-glass'
]
num_classes = len(classes)
model_path = r"C:\Users\leek37\Desktop\Imperial Hackathon 2\garbage_classifier_v3.pth"

# --- Model definition
class GarbageClassifier(nn.Module):
    def __init__(self, num_classes):
        super().__init__()
        self.network = resnet18(weights=ResNet18_Weights.DEFAULT)
        self.network.fc = nn.Linear(self.network.fc.in_features, num_classes)

    def forward(self, xb):
        return self.network(xb)

# --- Device & model loading
device = torch.device("cpu")
model = GarbageClassifier(num_classes).to(device)

# Load state dict safely
if not os.path.exists(model_path):
    raise FileNotFoundError(f"Model not found: {model_path}")

try:
    model.load_state_dict(torch.load(model_path, map_location=device))
    print("Model loaded successfully.")
except RuntimeError as e:
    print("Error:", e)
    raise

model.eval()

# --- Helper functions
def generalisation(rubbish_class: str) -> str:
    if rubbish_class in ["cardboard", "paper"]:
        return b"A"
    elif rubbish_class == "plastic":
        return b"B"
    else:
        return b"C"

def infer(photo_path: str) -> str:
    transform = transforms.Compose([
        transforms.Resize((128, 128)),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406],
                             std=[0.229, 0.224, 0.225])
    ])

    if not os.path.exists(photo_path):
        raise FileNotFoundError(f"Image not found: {photo_path}")

    img = Image.open(photo_path).convert("RGB")
    img_tensor = transform(img).unsqueeze(0).to(device)

    with torch.no_grad():
        outputs = model(img_tensor)
        pred_idx = outputs.argmax(dim=1).item()

    pred_class = classes[pred_idx]
    return pred_class
