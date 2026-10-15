import os
import random
import numpy as np
import torch
from torch import nn, optim
from torchvision import datasets, transforms, models
from torch.utils.data import DataLoader, Subset
from sklearn.model_selection import train_test_split
from sklearn.utils.class_weight import compute_class_weight
from tqdm import tqdm

SEED = 42
DATA_DIR = "dataset/expanded_organized"
CHECKPOINT_PATH = "classifier_frozen_head.pt"
NUM_CLASSES = 5
NUM_EPOCHS = 10
BATCH_SIZE = 16
LEARNING_RATE = 0.0001

random.seed(SEED)
np.random.seed(SEED)
torch.manual_seed(SEED)

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print(f"Device: {device}")

train_transforms = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.RandomHorizontalFlip(),
    transforms.ToTensor(),
    transforms.Normalize(
        [0.485, 0.456, 0.406],
        [0.229, 0.224, 0.225],
    ),
])

val_transforms = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
    transforms.Normalize(
        [0.485, 0.456, 0.406],
        [0.229, 0.224, 0.225],
    ),
])

base_dataset = datasets.ImageFolder(DATA_DIR)
classes = base_dataset.classes
targets = np.array(base_dataset.targets)
indices = np.arange(len(base_dataset))

train_indices, val_indices = train_test_split(
    indices,
    test_size=0.2,
    random_state=SEED,
    stratify=targets,
)

train_base = datasets.ImageFolder(DATA_DIR, transform=train_transforms)
val_base = datasets.ImageFolder(DATA_DIR, transform=val_transforms)

train_dataset = Subset(train_base, train_indices.tolist())
val_dataset = Subset(val_base, val_indices.tolist())

train_loader = DataLoader(
    train_dataset, batch_size=BATCH_SIZE, shuffle=True, num_workers=0
)
val_loader = DataLoader(
    val_dataset, batch_size=BATCH_SIZE, shuffle=False, num_workers=0
)

train_labels = targets[train_indices]
class_weights = compute_class_weight(
    class_weight="balanced",
    classes=np.arange(NUM_CLASSES),
    y=train_labels,
)
class_weights = torch.tensor(class_weights, dtype=torch.float32).to(device)

print(f"Classes: {classes}")
print(f"Training images: {len(train_dataset)}")
print(f"Validation images: {len(val_dataset)}")
print(f"Class weights: {class_weights.cpu().tolist()}")

model = models.resnet18(weights=models.ResNet18_Weights.DEFAULT)

for param in model.parameters():
	param.requires_grad = False

num_features = model.fc.in_features
model.fc = nn.Sequential(
    nn.Linear(num_features, 512),
    nn.ReLU(),
    nn.Dropout(0.3),
    nn.Linear(512, NUM_CLASSES),
)
model = model.to(device)

criterion = nn.CrossEntropyLoss(weight=class_weights)
optimizer = optim.Adam(
filter(lambda p: p.requires_grad,model.parameters()),
lr = LEARNING_RATE
)
best_val_acc = -1.0

for epoch in range(NUM_EPOCHS):
    model.train()
    train_loss_sum = 0.0

    for inputs, labels in tqdm(
        train_loader, desc=f"Epoch {epoch + 1}/{NUM_EPOCHS}"
    ):
        inputs, labels = inputs.to(device), labels.to(device)
        optimizer.zero_grad()
        outputs = model(inputs)
        loss = criterion(outputs, labels)
        loss.backward()
        optimizer.step()
        train_loss_sum += loss.item() * labels.size(0)

    train_loss = train_loss_sum / len(train_dataset)

    model.eval()
    val_loss_sum = 0.0
    correct = 0
    total = 0

    with torch.inference_mode():
        for inputs, labels in val_loader:
            inputs, labels = inputs.to(device), labels.to(device)
            outputs = model(inputs)
            loss = criterion(outputs, labels)
            val_loss_sum += loss.item() * labels.size(0)
            predictions = outputs.argmax(dim=1)
            correct += (predictions == labels).sum().item()
            total += labels.size(0)

    val_loss = val_loss_sum / total
    val_acc = correct / total

    print(
        f"Epoch {epoch + 1}/{NUM_EPOCHS} | "
        f"Train Loss: {train_loss:.4f} | "
        f"Val Loss: {val_loss:.4f} | "
        f"Val Accuracy: {val_acc:.2%}"
    )

    if val_acc > best_val_acc:
        best_val_acc = val_acc
        torch.save(
            {
                "model_state_dict": model.state_dict(),
                "optimizer_state_dict": optimizer.state_dict(),
                "epoch": epoch + 1,
                "val_accuracy": val_acc,
                "classes": classes,
            },
            CHECKPOINT_PATH,
        )
        print(f"Saved best checkpoint: {CHECKPOINT_PATH}")

print(f"Training complete. Best validation accuracy: {best_val_acc:.2%}")
