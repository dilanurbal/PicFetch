from ultralytics import YOLOE
from core import config

MODEL_FILES = {
    "small": "yoloe-26s-seg.pt",
    "medium": "yoloe-26m-seg.pt",
    "large": "yoloe-26l-seg.pt"
}

# model size yüklenemezse default olarak small yüklenir
model_file = MODEL_FILES.get(config.MODEL_SIZE, "yoloe-26s-seg.pt")

model = YOLOE(model_file)

print(f"YOLOE-26 model yüklendi: {model_file}")