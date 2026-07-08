# PicFetch

🇹🇷 [Türkçe versiyon](README.md)

# 🔍  Image Finder & Verification App

This project is an end-to-end application that finds legal, free images from the internet (Pixabay/Pexels API) based on a keyword the user enters, downloads them, and verifies whether the searched object actually appears in each image using an open-vocabulary AI model (**YOLOE-26**).

The project is designed with a **"One Core, Two Faces"** architecture, so it can run through both a **Web Interface (FastAPI + HTML/JS)** and a **Command-Line Interface (CLI - Typer)**. The whole system is packaged with **Docker (CPU-only)** to be portable.

**Repo:** https://github.com/dilanurbal/PicFetch.git

---

## 🚀 Project Architecture & "One Core, Two Faces"

All the core logic of the app — searching, downloading, verifying, and filtering — lives under the `core/` folder. The web interface and the CLI both call the same core to avoid code duplication, improve testability, and simplify Docker packaging.

```text
core/                  # Shared Core Pipeline
│  ├── search.py       # Image search + API integration + download
│  ├── detector.py     # YOLOE-26 + SAM wrapper (models are loaded at startup / on first use)
│  ├── pipeline.py     # Search -> Download -> Detect -> Filter flow
│  ├── mapping.py      # Turkish - English keyword mapping table
│  └── config.py       # Settings, model sizes, thresholds, and API key management
web/                   # Web Interface Layer
│  ├── main.py         # FastAPI backend app and endpoints
│  └── static/         # Plain HTML + CSS + JavaScript (Fetch API) frontend
cli/                   # Command-Line Layer
│  └── __main__.py     # Typer-based CLI app
models/                # YOLOE-26 / SAM weights (downloaded during Docker build)
downloads/             # Temp folder for downloaded images (cleaned up to save disk space)
tests/                 # Pytest test scenarios
Dockerfile             # Multi-stage Dockerfile for a single CPU-only image
requirements.txt       # Dependency list (including CPU-only PyTorch)
.env.example           # API key template (the real .env file is gitignored)
```

---

## 🛠️ Tech Stack

*   **Core Language:** Python 3.11+
*   **Object Detection & AI:** Ultralytics, YOLOE-26 (open-vocabulary object detection)
*   **Segmentation:** Meta SAM (Segment Anything Model — mobile_sam), pixel-level mask generation
*   **Web Backend:** FastAPI + Uvicorn (automatic Swagger docs at `/docs`)
*   **Web Frontend:** Pure HTML, CSS, JavaScript (Fetch API)
*   **CLI:** Typer
*   **HTTP & Image Downloading:** HTTPX or Requests
*   **Image Processing:** Pillow (PIL)
*   **Image Source:** Pixabay or Pexels API
*   **Packaging:** Docker (Python 3.11-slim + CPU-only PyTorch)

---

## 🔄 Pipeline Execution

1.  **Input:** The user enters a keyword (e.g. `"horse"` in Turkish: `"at"`).
2.  **Translation & Mapping:** The keyword is translated to English via `mapping.py` (`"horse"`). Translation matters both for richer search results and because YOLOE-26's text encoder is better optimized for English.
3.  **Search:** A query is sent to the search API, returning $N$ image URLs.
4.  **Download:** Images are temporarily downloaded to the `downloads/` folder.
5.  **Verification (AI):** The YOLOE-26 model, loaded into memory once at startup, scans each image targeting `set_classes(["horse"])`.
6.  **Filtering & Scoring:** Objects above the configured confidence threshold (default `0.5`) are marked as successful (`✓ [confidence score]`), and those below it as failed (`X`).
7.  **Segmentation (optional):** If requested, the bounding boxes found by YOLOE-26 are passed as prompts to the SAM model (`mobile_sam`), which generates a pixel-level segmentation mask around the object. SAM is only loaded into memory on first use (lazy-loading), so startup time is unaffected in scenarios that don't use segmentation.
8.  **Output:**
    *   **On the web:** Images are shown in a grid, each with a `✓/X` label, confidence score, and a download button.
    *   **On the CLI:** Images that pass verification are saved to the specified output folder.

---

## 🧩 Key Features

*   **YOLOE-26 (Open-Vocabulary Detection):** Detects objects based on any keyword the user provides (`set_classes`), without being limited to a predefined set of classes.
*   **SAM Segmentation Support:** The bounding boxes produced by YOLOE-26 are passed to Meta's SAM (mobile_sam) model, producing not just a box but the object's real pixel-level boundaries (a mask). Both models can run together in the same flow; SAM is lazy-loaded so it doesn't affect YOLOE-26's startup performance.

---

## 📦 Installation & Running

### 1. Local Setup (Local Development)

First, create a virtual environment and install dependencies:

```bash
# Clone the project
git clone https://github.com/dilanurbal/PicFetch.git
cd PicFetch

# Create and activate a virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

#### Setting Environment Variables:
Copy `.env.example` to `.env` and add the API key you obtained from Pixabay or Pexels:

```bash
cp .env.example .env
```
`.env` contents:
```env
PIXABAY_API_KEY=your_api_key_here
DEFAULT_MODEL_SIZE=small
CONFIDENCE_THRESHOLD=0.5
SAM_MODEL_SIZE=mobile
```

#### Note on Model Weights:
YOLOE-26 and SAM (mobile_sam) weights are not included in the repo; the `ultralytics` library automatically downloads them the first time the models are used. This means the app's first run (or the Docker build step) requires an internet connection.

#### Running the CLI App:
```bash
python -m cli --query "horse" --output ./results
```

#### Running the Web App:
```bash
uvicorn web.main:app --reload
```
Visit `http://127.0.0.1:8000` in your browser to access the interface, or `http://127.0.0.1:8000/docs` to explore the Swagger API documentation.

### 2. Running with Docker (Recommended / Portable Mode)

The app is packaged to run on **any CPU architecture without requiring a GPU**. Model weights are baked into the image during the build stage, so there's no waiting to download weights on first run.

```bash
# Build the Docker image (model weights are downloaded during build)
docker build -t image-verification-app .

# Start the container
docker run -d -p 8000:8000 --env-file .env image-verification-app
```
The app will be available at `http://localhost:8000`.

---

## ⚠️ Edge Cases & Error Handling

The system is designed to be resilient against issues that may come up in demos or production:
*   **Search returns 0 results:** The app doesn't crash; the user sees a "No results found" message.
*   **Keyword not in the mapping table:** The user is warned and advised to enter an English term instead.
*   **Corrupted file/image:** A broken downloaded image is skipped, and the pipeline continues with the remaining images.
*   **API limit reached:** The user sees a friendly error message and is asked to try again later.
*   **No image passes verification ($X$):** The screen isn't left empty; images are still shown, but labeled "Not verified".
*   **Internet/API access lost:** The system throws a handled error instead of crashing.

---

## 👥 Contributors

*   **Dilanur Bal (https://github.com/dilanurbal)**
*   **Mert Atmaca(https://github.com/MertAtmacaDev)**
*   **Ayşen Çiftçi(https://github.com/aysenciftci23)**
*   **Ayşe Semra Yaslan(https://github.com/semra2314)**

---

## 👥 Team Role Distribution (4 People)

The project is split into parallel work packages to reach an MVP (Minimum Viable Product) quickly:
*   **Person 1 (Search Module):** API integration, key management, image downloading, rate-limiting and caching. (`search.py`, `config.py`)
*   **Person 2 (Detection Module):** YOLOE-26 and SAM integration, model loading, `set_classes` mechanism, and output formatting. (`detector.py`)
*   **Person 3 (Web Layer):** Writing the FastAPI backend endpoints and the HTML/JS-based dynamic search grid interface. (`web/` folder)
*   **Person 4 (CLI, Docker & Integration):** Building the Typer CLI, setting up the Dockerfile architecture, test scenarios (`tests/`), and integrating the modules.

---

## 💡 Important Developer Notes

1.  **Model Optimization:** Models are **not** reloaded on every HTTP request. YOLOE-26 is loaded into memory once at app startup; SAM is lazy-loaded on first use. Both are used via a singleton pattern by the shared pipeline.
2.  **Disk Management:** Images downloaded to `downloads/` are cleaned up immediately after analysis and delivery to the client/interface, preserving server disk space.
3.  **Verification Visibility (Demo Note):** Since stock photo sites (Pixabay/Pexels) already have high-quality tags, the searched object will almost always be found ($✓$) in nearly every image. To prove during a demo that the system actually filters things out, it's important to not simply hide the rejected images — instead, show them under a **"Rejected"** section, or with a dimmed $X$ mark along with their confidence scores.
