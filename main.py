import uvicorn
from fastapi import FastAPI, Response
from fastapi.middleware.cors import CORSMiddleware
from models import SearchRequest, DetectionResult, PipelineResponse

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

# 4. Kök endpoint: Sağlık/Hoş geldin mesajı
@app.get("/")
def read_root():
    """
    Sağlık ve hoş geldin mesajı dönen kök endpoint.
    """
    return {
        "status": "success",
        "message": "PicFetch Web Backend Sunucusuna Hoş Geldiniz!"
    }

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

    # Kelime bazlı sahte görsel veritabanı (Pixabay kaynaklı)
    mock_images_db = {
        "at": [
            {"url": "https://cdn.pixabay.com/photo/2017/02/15/11/05/texture-2068278_1280.jpg", "is_verified": True, "score": 0.94},
            {"url": "https://cdn.pixabay.com/photo/2016/11/14/17/39/dog-1824166_1280.jpg", "is_verified": False, "score": 0.12},
            {"url": "https://cdn.pixabay.com/photo/2016/11/29/04/18/horse-1867278_1280.jpg", "is_verified": True, "score": 0.88}
        ],
        "kedi": [
            {"url": "https://cdn.pixabay.com/photo/2017/02/20/18/03/cat-2083492_1280.jpg", "is_verified": True, "score": 0.96},
            {"url": "https://cdn.pixabay.com/photo/2016/11/14/17/39/dog-1824166_1280.jpg", "is_verified": False, "score": 0.08},
            {"url": "https://cdn.pixabay.com/photo/2014/04/13/20/49/cat-323262_1280.jpg", "is_verified": True, "score": 0.91}
        ],
        "köpek": [
            {"url": "https://cdn.pixabay.com/photo/2016/11/14/17/39/dog-1824166_1280.jpg", "is_verified": True, "score": 0.95},
            {"url": "https://cdn.pixabay.com/photo/2017/02/20/18/03/cat-2083492_1280.jpg", "is_verified": False, "score": 0.15},
            {"url": "https://cdn.pixabay.com/photo/2016/12/13/05/15/puppy-1903313_1280.jpg", "is_verified": True, "score": 0.89}
        ],
        "araba": [
            {"url": "https://cdn.pixabay.com/photo/2012/11/02/13/02/car-63930_1280.jpg", "is_verified": True, "score": 0.97},
            {"url": "https://cdn.pixabay.com/photo/2015/04/23/22/00/tree-736885_1280.jpg", "is_verified": False, "score": 0.11},
            {"url": "https://cdn.pixabay.com/photo/2016/11/22/23/44/porsche-1851246_1280.jpg", "is_verified": True, "score": 0.92}
        ],
        "ev": [
            {"url": "https://cdn.pixabay.com/photo/2016/11/18/17/46/house-1836070_1280.jpg", "is_verified": True, "score": 0.93},
            {"url": "https://cdn.pixabay.com/photo/2016/11/14/17/39/dog-1824166_1280.jpg", "is_verified": False, "score": 0.14},
            {"url": "https://cdn.pixabay.com/photo/2014/07/10/17/18/large-home-389271_1280.jpg", "is_verified": True, "score": 0.87}
        ],
        "ağaç": [
            {"url": "https://cdn.pixabay.com/photo/2015/04/23/22/00/tree-736885_1280.jpg", "is_verified": True, "score": 0.98},
            {"url": "https://cdn.pixabay.com/photo/2017/02/20/18/03/cat-2083492_1280.jpg", "is_verified": False, "score": 0.05},
            {"url": "https://cdn.pixabay.com/photo/2015/06/08/15/02/forest-801757_1280.jpg", "is_verified": True, "score": 0.90}
        ],
        "çiçek": [
            {"url": "https://cdn.pixabay.com/photo/2014/02/27/16/10/flowers-276014_1280.jpg", "is_verified": True, "score": 0.97},
            {"url": "https://cdn.pixabay.com/photo/2017/02/20/18/03/cat-2083492_1280.jpg", "is_verified": False, "score": 0.09},
            {"url": "https://cdn.pixabay.com/photo/2015/04/19/08/32/rose-729509_1280.jpg", "is_verified": True, "score": 0.93}
        ],
        "kuş": [
            {"url": "https://cdn.pixabay.com/photo/2015/11/16/16/28/bird-1045954_1280.jpg", "is_verified": True, "score": 0.95},
            {"url": "https://cdn.pixabay.com/photo/2016/11/14/17/39/dog-1824166_1280.jpg", "is_verified": False, "score": 0.13},
            {"url": "https://cdn.pixabay.com/photo/2017/05/08/13/15/bird-2295431_1280.jpg", "is_verified": True, "score": 0.87}
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
            {"url": "https://cdn.pixabay.com/photo/2016/08/11/23/48/mountains-1587287_1280.jpg", "is_verified": True, "score": score1},
            {"url": "https://cdn.pixabay.com/photo/2016/11/14/17/39/dog-1824166_1280.jpg", "is_verified": False, "score": score2},
            {"url": "https://cdn.pixabay.com/photo/2015/04/23/22/00/tree-736885_1280.jpg", "is_verified": True, "score": score3}
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

    return PipelineResponse(
        search_keyword=keyword,
        translated_keyword=translated,
        results=results
    )

# 5. Uvicorn ile uygulamanın lokalde (port 8000) çalışmasını sağlayacak blok
if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
