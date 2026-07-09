import os
from dotenv import load_dotenv

load_dotenv()

PIXABAY_API_KEY = os.getenv("PIXABAY_API_KEY")
MODEL_SIZE = os.getenv("MODEL_SIZE", "small")
CONFIDENCE_THRESHOLD = float(os.getenv("CONFIDENCE_THRESHOLD", "0.5"))
DEFAULT_LIMIT = int(os.getenv("DEFAULT_LIMIT", "20"))
SAM_MODEL_SIZE = "mobile"  # "mobile", "base" veya "large"
if not PIXABAY_API_KEY:
    print("UYARI: PIXABAY_API_KEY ayarlı değil. .env dosyanı kontrol et.")

"""
config.py - Uygulama Ayarları

Tüm yapılandırma parametrelerini yönetir.
"""

import os
from dotenv import load_dotenv

# .env dosyasını yükle
load_dotenv()


def get_config():
    """
    Uygulama konfigürasyonunu döndürür.
    """
    return {
        # Pixabay API
        "pixabay_api_key": os.getenv("PIXABAY_API_KEY", ""),
        
        # YOLOE-26 Ayarları
        "model_size": os.getenv("MODEL_SIZE", "nano"),  # nano, small, medium
        "confidence_threshold": float(os.getenv("CONFIDENCE_THRESHOLD", "0.5")),
        
        # Pipeline Ayarları
        "max_images": int(os.getenv("MAX_IMAGES", "10")),
        "download_timeout": int(os.getenv("DOWNLOAD_TIMEOUT", "15")),
        
        # Dizinler
        "downloads_dir": os.getenv("DOWNLOADS_DIR", "downloads"),
        "models_dir": os.getenv("MODELS_DIR", "models"),
    }