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