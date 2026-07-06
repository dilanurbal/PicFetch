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

def verify_target(image_path, target):
    """Bir görselde hedef nesneyi doğrular. Found, confidence (güven skoru) döndürür."""
    
    model.set_classes([target])
    results = model.predict(image_path, verbose=False)
    
    # Bulunan nesnelerin güven skorlarını toplar
    confidences = results[0].boxes.conf.tolist()

    if not confidences:
        return False, 0.0
    
    best_confidence = max(confidences)
    # en güçlü skoru eşik değer ile karşılaştırır, eşiği geçiyorsa hedef doğrulanır
    found = best_confidence >= config.CONFIDENCE_THRESHOLD
    return found, best_confidence
