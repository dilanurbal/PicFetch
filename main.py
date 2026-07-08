import os
import uvicorn
from fastapi import FastAPI, Response, HTTPException
from fastapi.responses import HTMLResponse, StreamingResponse
from fastapi.middleware.cors import CORSMiddleware

# Model adları PR dallarında farklı olabilir; import hatası olmaması için esnek davranıyoruz.
try:
    from models import SearchRequest, DetectionResult, PipelineResponse, DownloadRequest, DownloadZipRequest
except Exception:
    # Eğer modellerden bazıları yoksa, higher-level işlemler sırasında getattr ile güvenli erişim kullanacağız.
    from models import SearchRequest, DetectionResult, PipelineResponse

import io
import zipfile
import requests

# Bellek içi görsel ID -> URL önbelleği
image_registry = {}

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
    keyword = payload.keyword.strip()

    # Eğer payload.keyword boşsa veya 'çökert' ise boş sonuç dön
    if not keyword or keyword.lower() == "çökert":
        return PipelineResponse(
            search_keyword=keyword,
            translated_keyword="",
            results=[]
        )

    # Basit Türkçe-İngilizce kelime çevirisi simülasyonu
    translation_map = {
        "at": "horse",
        "kedi": "cat",
        "köpek": "dog",
        "araba": "car",
        "kuş": "bird",
        "ağaç": "tree",
        "çiçek": "flower",
        "ev": "house"
    }
    
    # Kelime eşleşiyorsa haritadan al, yoksa simüle etmek için sonuna '-translated' ekle
    translated = translation_map.get(keyword.lower(), f"{keyword.lower()}-translated")

    # Kelime bazlı sahte görsel veritabanı (Unsplash kaynaklı - İndirilebilir & CORS hatasız)
    mock_images_db = {
        "at": [
            {"url": "https://images.unsplash.com/photo-1553284965-83fd3e82fa5a?w=800", "is_verified": True, "score": 0.94},
            {"url": "https://images.unsplash.com/photo-1543466835-00a7907e9de1?w=800", "is_verified": False, "score": 0.12},
            {"url": "https://images.unsplash.com/photo-1598974357801-cbca100e6543?w=800", "is_verified": True, "score": 0.88}
        ],
        "kedi": [
            {"url": "https://images.unsplash.com/photo-1514888286974-6c03e2ca1dba?w=800", "is_verified": True, "score": 0.96},
            {"url": "https://images.unsplash.com/photo-1543466835-00a7907e9de1?w=800", "is_verified": False, "score": 0.08},
            {"url": "https://images.unsplash.com/photo-1533738363-b7f9aef128ce?w=800", "is_verified": True, "score": 0.91}
        ],
        "köpek": [
            {"url": "https://images.unsplash.com/photo-1543466835-00a7907e9de1?w=800", "is_verified": True, "score": 0.95},
            {"url": "https://images.unsplash.com/photo-1514888286974-6c03e2ca1dba?w=800", "is_verified": False, "score": 0.15},
            {"url": "https://images.unsplash.com/photo-1583511655857-d19b40a7a54e?w=800", "is_verified": True, "score": 0.89}
        ],
        "araba": [
            {"url": "https://images.unsplash.com/photo-1494976388531-d1058494cdd8?w=800", "is_verified": True, "score": 0.97},
            {"url": "https://images.unsplash.com/photo-1502082553048-f009c37129b9?w=800", "is_verified": False, "score": 0.11},
            {"url": "https://images.unsplash.com/photo-1503376780353-7e6692767b70?w=800", "is_verified": True, "score": 0.92}
        ],
        "ev": [
            {"url": "https://images.unsplash.com/photo-1570129477492-45c003edd2be?w=800", "is_verified": True, "score": 0.93},
            {"url": "https://images.unsplash.com/photo-1543466835-00a7907e9de1?w=800", "is_verified": False, "score": 0.14},
            {"url": "https://images.unsplash.com/photo-1564013799919-ab600027ffc6?w=800", "is_verified": True, "score": 0.87}
        ],
        "ağaç": [
            {"url": "https://images.unsplash.com/photo-1502082553048-f009c37129b9?w=800", "is_verified": True, "score": 0.98},
            {"url": "https://images.unsplash.com/photo-1514888286974-6c03e2ca1dba?w=800", "is_verified": False, "score": 0.05},
            {"url": "https://images.unsplash.com/photo-1448375240586-882707db888b?w=800", "is_verified": True, "score": 0.90}
        ],
        "çiçek": [
            {"url": "https://images.unsplash.com/photo-1526047932273-341f2a7631f9?w=800", "is_verified": True, "score": 0.97},
            {"url": "https://images.unsplash.com/photo-1514888286974-6c03e2ca1dba?w=800", "is_verified": False, "score": 0.09},
            {"url": "https://images.unsplash.com/photo-1561181286-d3fee7d55364?w=800", "is_verified": True, "score": 0.93}
        ],
        "kuş": [
            {"url": "https://images.unsplash.com/photo-1452570053594-1b985d6ea890?w=800", "is_verified": True, "score": 0.95},
            {"url": "https://images.unsplash.com/photo-1543466835-00a7907e9de1?w=800", "is_verified": False, "score": 0.13},
            {"url": "https://images.unsplash.com/photo-1480069689960-5b3ff4b13390?w=800", "is_verified": True, "score": 0.87}
        ]
    }

    # Eğer aranan kelime veritabanımızda tanımlıysa onu seç, yoksa genel/dinamik değerler üret
    key_lower = keyword.lower()
    if key_lower in mock_images_db:
        selected_data = mock_images_db[key_lower]
    else:
        # Kelime uzunluğuna göre hafifçe değişen dinamik skorlar ve varsayılan manzara görselleri
        val = len(keyword) % 10
        score1 = round(0.90 + (val / 150), 2)
        score2 = round(0.10 + (val / 150), 2)
        score3 = round(0.80 + (val / 150), 2)
        selected_data = [
            {"url": "https://images.unsplash.com/photo-1464822759023-fed622ff2c3b?w=800", "is_verified": True, "score": score1},
            {"url": "https://images.unsplash.com/photo-1543466835-00a7907e9de1?w=800", "is_verified": False, "score": score2},
            {"url": "https://images.unsplash.com/photo-1502082553048-f009c37129b9?w=800", "is_verified": True, "score": score3}
        ]

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

    # Görsel ID'lerini ve URL'lerini önbelleğe kaydet
    global image_registry
    for res in results:
        image_registry[res.image_id] = res.original_url

    return PipelineResponse(
        search_keyword=keyword,
        translated_keyword=translated,
        results=results
    )

# 5. Görsel indirme ve ZIP paketi oluşturma POST endpoint'i
# İki route’u da destekleyelim (esneklik için)
@app.post("/api/v1/images/download-zip")
@app.post("/download-zip")
def download_images_zip(payload):
    """
    Hem feature hem developer daldaki payload biçimlerini destekleyen esnek bir handler.
    - Eğer payload.selectedImageIds ve payload.images varsa bu şekilde çalışır (daha zengin yapı).
    - Eğer payload.image_ids varsa bu eski biçimi de destekler ve image_registry'den URL alır.
    """
    # Uyumluluk: farklı dallarda farklı alan isimleri kullanılmış olabilir.
    selected_ids = None
    # try common names safely
    selected_ids = getattr(payload, "selectedImageIds", None) or getattr(payload, "image_ids", None)
    images_field = getattr(payload, "images", None)

    if not selected_ids:
        raise HTTPException(status_code=400, detail="Lütfen indirilecek en az bir görsel seçin.")

    # if images field provided (developer branch style), filter by selected ids
    selected_images = []
    if images_field:
        # images beklenen obje listesiyse (id, url)
        selected_images = [img for img in images_field if getattr(img, "id", None) in selected_ids]
    else:
        # images yoksa, image_registry'den URL bul ve geçici basit dict'ler oluştur
        for item_id in selected_ids:
            url = image_registry.get(item_id)
            if url:
                # basit objeye benzer davranış için küçük dict kullanıyoruz
                selected_images.append(type("Img", (), {"id": item_id, "url": url})())
            else:
                # Eğer id için URL bulunamazsa, hata yerine ZIP içine hata notu eklemek daha kullanıcı-dostu
                selected_images.append(type("Img", (), {"id": item_id, "url": None})())

    # ZIP dosyasını bellek üzerinde (in-memory) saklamak için BytesIO nesnesi oluştur
    zip_buffer = io.BytesIO()

    # Bellek-içi ZIP dosyası yazıcı sınıflarını hazırla
    with zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED) as zip_file:
        for img in selected_images:
            if not getattr(img, "url", None):
                zip_file.writestr(
                    f"hata_{getattr(img, 'id', 'unknown')}.txt",
                    f"Görsel URL bulunamadı. ID: {getattr(img, 'id', 'unknown')}"
                )
                continue

            try:
                headers = {
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
                }
                response = requests.get(img.url, headers=headers, timeout=10)

                if response.status_code == 200:
                    content_type = response.headers.get("content-type", "")
                    ext = "jpg"
                    if "png" in content_type:
                        ext = "png"
                    elif "webp" in content_type:
                        ext = "webp"
                    elif "gif" in content_type:
                        ext = "gif"
                    else:
                        clean_url = img.url.split('?')[0].split('#')[0]
                        url_ext = clean_url.split('.')[-1].lower()
                        if url_ext in ["jpg", "jpeg", "png", "webp", "gif"]:
                            ext = url_ext

                    filename = f"{getattr(img, 'id', 'image')}.{ext}"
                    zip_file.writestr(filename, response.content)
                else:
                    zip_file.writestr(
                        f"hata_{getattr(img, 'id', 'unknown')}.txt",
                        f"Görsel indirilemedi. Sunucu Yanıtı: {response.status_code}\nURL: {img.url}"
                    )
            except Exception as e:
                zip_file.writestr(
                    f"hata_{getattr(img, 'id', 'unknown')}.txt",
                    f"Görsel indirilirken hata oluştu: {str(e)}\nURL: {img.url}"
                )

    # Yazma işlemi bittiğinde arabelleğin okuma konumunu başa sar
    zip_buffer.seek(0)

    # ZIP dosyasını tarayıcının otomatik indireceği StreamingResponse olarak dön
    return StreamingResponse(
        zip_buffer,
        media_type="application/zip",
        headers={
            "Content-Disposition": "attachment; filename=secili_gorseller.zip",
            "Access-Control-Expose-Headers": "Content-Disposition"
        }
    )

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)