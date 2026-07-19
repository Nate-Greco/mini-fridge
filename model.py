import torch
import torch.nn as nn

size = 100

def get_device():
    if torch.cuda.is_available():
        return torch.device("cuda")
    try:
        import torch_directml
        return torch_directml.device()
    except ImportError:
        pass
    except Exception as e:
        print(f"BIG ERR")
    return torch.device("cpu")

class FaceCNN (nn.Module):
    def __init__(self, num: int):
        super().__init__()
        self.features = nn.Sequential(
            nn.Conv2d(1, 32, 3, padding=1), nn.BatchNorm2d(32), nn.ReLU(), nn.MaxPool2d(2),
            nn.Conv2d(32, 64, 3, padding=1), nn.BatchNorm2d(64), nn.ReLU(), nn.MaxPool2d(2),
            nn.Conv2d(64, 128, 3, padding=1), nn.BatchNorm2d(128), nn.ReLU(), nn.MaxPool2d(2),
        )
        self.classifier = nn.Sequential(
            nn.Flatten(),
            nn.Linear(128 * 12 *12, 256),
            nn.ReLU(),
            nn.Dropout(0.4),
            nn.Linear(256, num),
        )
    def forward(self, x):
        x = self.features(x)
        return self.classifier(x)