import os
import uvicorn
from fastapi import FastAPI, Response
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from models import SearchRequest, DetectionResult, PipelineResponse
from core.mapping import translate_query
from core.mock_data import get_mock_images

# 1. FastAPI uygulamasını başlat, başlık ve açıklama ekle
app = FastAPI(
    title="PicFetch API",
    description="Görsel Arama ve Nesne Tespiti Boru Hattı API Sunucusu"
)

# 2. CORS politikaları için CORSMiddleware ekle
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 3. Tarayıcının otomatik aradığı site ikonunu (favicon) boş (204) dönerek 404 hatasını önle
@app.get("/favicon.ico", include_in_schema=False)
def favicon():
    return Response(status_code=204)

# 4. Kök endpoint: Modern Arayüzü (web/index.html) sunar
@app.get("/", response_class=HTMLResponse)
def read_root():
    """
    Kullanıcı arayüzünü (HTML) dönen kök endpoint.
    """
    filepath = os.path.join(os.path.dirname(__file__), "web", "index.html")
    if os.path.exists(filepath):
        with open(filepath, "r", encoding="utf-8") as f:
            return HTMLResponse(content=f.read())
    return HTMLResponse(content="<h3>Arayüz dosyası bulunamadı.</h3>", status_code=404)

# 4. Arama pipeline POST endpoint'i
@app.post("/api/v1/pipeline/search", response_model=PipelineResponse)
def search_pipeline(payload: SearchRequest):
    """
    Görsel arama ve nesne tespiti boru hattını (pipeline) simüle eden endpoint.
    """
    keyword = payload.query.strip()

    # Eğer payload.query boşsa veya 'çökert' ise boş sonuç dön
    if not keyword or keyword.lower() == "çökert":
        return PipelineResponse(
            search_keyword=keyword,
            translated_keyword="",
            results=[]
        )

    # translate_query ile SRP uyumlu çeviri işlemi
    translated = translate_query(keyword, translate=payload.translate, target_lang=payload.target_lang)

    # get_mock_images ile statik/dinamik sahte görsel verilerini al
    selected_data = get_mock_images(translated)

    # Sonuç listesini dinamik olarak oluştur
    results = [
        DetectionResult(
            image_id=f"img_{i+1:02d}",
            original_url=item["url"],
            is_verified=item["is_verified"],
            confidence_score=item["score"]
        )
        for i, item in enumerate(selected_data)
    ]

    return PipelineResponse(
        search_keyword=keyword,
        translated_keyword=translated if payload.translate else "",
        results=results
    )

# 5. Uvicorn ile uygulamanın lokalde (port 8000) çalışmasını sağlayacak blok
if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
