import os
from torch.utils.data import Dataset, DataLoader, Subset, random_split
from PIL import Image
from torchvision import transforms
from model import size, FaceCNN, get_device
import torch
import torch.nn as nn

class faces(Dataset):
    def __init__(self, dir, transform):
        self.samples = []
        self.transform = transform
        self.classes = sorted(i for i in os.listdir(dir) if os.path.isdir(os.path.join(dir, i)))
        self.classToIdx = {c: i for i, c in enumerate(self.classes)}

        for c in self.classes:
            classDir = os.path.join(dir, c)
            for fname in os.listdir(classDir):
                if fname.lower().endswith((".png", ".jpg", ".jpeg")):
                    self.samples.append((os.path.join(classDir, fname), self.classToIdx[c]))

    def __len__(self):
        return len(self.samples)
    
    def __getitem__(self, idx):
        path, label = self.samples[idx]
        img = Image.open(path).convert("L")
        img = self.transform(img)
        return img, label
    
trainTransform = transforms.Compose([
    transforms.Resize((size, size)),
    transforms.RandomHorizontalFlip(),
    transforms.RandomRotation(10),
    transforms.ColorJitter(brightness=0.3, contrast=0.3),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.5], std=[0.5]),
])

valTransforms = transforms.Compose([
    transforms.Resize((size, size)),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.5], std=[0.5]),
])

torch.manual_seed(42)

# fullDataset = faces(dir="./dataset", transform=trainTransform)

fullDatasetTrain = faces(dir="./dataset", transform=trainTransform)
fullDatasetVal = faces(dir="./dataset", transform=valTransforms)

valSize = max(1, int(0.15 * len(fullDatasetTrain)))
trainSize = len(fullDatasetTrain) - valSize

indicies = torch.randperm(len(fullDatasetTrain)).tolist()
trainIndices, valIndicies = indicies[:trainSize], indicies[trainSize:]

# trainSet, valSet = random_split(fullDataset, [trainSize, valSize])

trainSet = Subset(fullDatasetTrain, trainIndices)
valSet = Subset(fullDatasetVal, valIndicies)

trainLoader = DataLoader(trainSet, batch_size=32, shuffle=True)
valLoader = DataLoader(valSet, batch_size=32, shuffle=False)

# device = get_device()
device = torch.device("cpu")
model = FaceCNN(num=len(fullDatasetTrain.classes)).to(device)
optimizer = torch.optim.Adam(model.parameters(), lr=1e-3)
criterion = nn.CrossEntropyLoss()

bestValAcc = 0.0

for epoch in range(1, 26):
    model.train()
    for imgs, labels in trainLoader:
        imgs, labels = imgs.to(device), labels.to(device)

        optimizer.zero_grad()
        outputs = model(imgs)
        loss = criterion(outputs, labels)
        loss.backward()
        optimizer.step()
    
    model.eval()
    correct = 0
    total = 0
    with torch.no_grad():
        for imgs, labels in valLoader:
            imgs, labels = imgs.to(device), labels.to(device)
            outputs = model(imgs)
            preds = outputs.argmax(dim=1)
            correct += (preds == labels).sum().item()
            total += labels.size(0)

    valAcc = correct / total if total else 0.0
    print(f"epoch {epoch}/25 - val_acc: {valAcc:.3f}")

    if valAcc >= bestValAcc:
        bestValAcc = valAcc
        cpuStateDict = {k: v.cpu() for k, v in model.state_dict().items()
                        }
        torch.save({
            "model_state": cpuStateDict,
            "classes": fullDatasetTrain.classes,
        }, "face_model.pt")