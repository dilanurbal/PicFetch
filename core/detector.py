from ultralytics import YOLOE
from core import config
import os

MODEL_FILES = {
    "small": "yoloe-26s-seg.pt",
    "medium": "yoloe-26m-seg.pt",
    "large": "yoloe-26l-seg.pt"
}

# model size yüklenemezse default olarak small yüklenir
model_file = MODEL_FILES.get(config.MODEL_SIZE, "yoloe-26s-seg.pt")

model = YOLOE(model_file)

print(f"YOLOE-26 model yüklendi: {model_file}")

def verify_target(image_path: str, target: str) -> tuple[bool, float]:
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

def save_detection(image_path: str, target:str) -> tuple[bool, float, str | None]:
    """Hedef doğrulanırsa görseli kutularla işaretleyip results klasörüne kaydeder"""

    model.set_classes([target])
    results = model.predict(image_path, verbose= False)

    confidences = results[0].boxes.conf.tolist()
    if not confidences:
        return False, 0.0 , None
    
    best_confidence = max(confidences)
    found = best_confidence >= config.CONFIDENCE_THRESHOLD

    # Sadece found = True görselleri kaydet
    if not found:
        return False, best_confidence, None
    
    os.makedirs("results", exist_ok=True)
    filename= os.path.basename(image_path)
    output_path = os.path.join("results", f"{target}_{filename}")
    results[0].save(filename=output_path)

    return True, best_confidence, output_path

