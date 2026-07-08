from ultralytics import YOLOE, SAM
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

SAM_MODEL_FILES = {
    "mobile": "mobile_sam.pt",
    "base": "sam_b.pt",
    "large": "sam_l.pt"
}

_sam_model = None


def _get_sam_model():
    global _sam_model
    if _sam_model is None:
        sam_size = getattr(config, "SAM_MODEL_SIZE", "mobile")
        sam_file = SAM_MODEL_FILES.get(sam_size, "mobile_sam.pt")
        _sam_model = SAM(sam_file)
        print(f"SAM model yüklendi: {sam_file}")
    return _sam_model


def _generate_masks(image_path: str, boxes: list):
    if not boxes:
        return None
    sam_model = _get_sam_model()
    sam_results = sam_model.predict(image_path, bboxes=boxes, verbose=False)
    return sam_results[0]

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

def detect_and_segment(image_path: str, target: str) -> tuple[bool, float, str | None, str | None]:
    model.set_classes([target])
    results = model.predict(image_path, verbose=False)

    confidences = results[0].boxes.conf.tolist()
    if not confidences:
        return False, 0.0, None, None

    best_confidence = max(confidences)
    found = best_confidence >= config.CONFIDENCE_THRESHOLD

    if not found:
        return False, best_confidence, None, None

    os.makedirs("results", exist_ok=True)
    filename = os.path.basename(image_path)
    name, ext = os.path.splitext(filename)

    box_output_path = os.path.join("results", f"{target}_{filename}")
    results[0].save(filename=box_output_path)

    boxes = results[0].boxes.xyxy.tolist()
    sam_result = _generate_masks(image_path, boxes)

    mask_output_path = None
    if sam_result is not None:
        mask_output_path = os.path.join("results", f"{target}_{name}_mask{ext}")
        sam_result.save(filename=mask_output_path)

    return True, best_confidence, box_output_path, mask_output_path
