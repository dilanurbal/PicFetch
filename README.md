# PicFetch

🇬🇧 [English version](README_EN.md)

# 🔍  Görsel Bulma ve Doğrulama Uygulaması

Bu proje, kullanıcının yazdığı bir kelimeye göre internetten (Pixabay/Pexels API) yasal ve ücretsiz görseller bulan, bu görselleri indiren ve her görselde aranan nesnenin gerçekten olup olmadığını açık-sözlüklü yapay zekâ modeli (**YOLOE-26**) ile doğrulayan uçtan uca bir uygulamadır.

Proje hem **Web Arayüzü (FastAPI + HTML/JS)** hem de **Komut Satırı (CLI - Typer)** üzerinden çalışabilecek şekilde "Tek Çekirdek, İki Yüz" mimarisiyle tasarlanmıştır. Tüm sistem **Docker (CPU-only)** ile paketlenerek taşınabilir hale getirilmiştir.

**Repo:** https://github.com/dilanurbal/PicFetch.git

---

## 🚀 Proje Mimarisi & "Tek Çekirdek, İki Yüz"

Uygulamanın arama, indirme, doğrulama ve filtreleme gibi tüm ana mantığı `core/` klasörü altında toplanmıştır. Web arayüzü ve CLI, kod tekrarını önlemek, test edilebilirliği artırmak ve Docker paketlemesini sadeleştirmek amacıyla aynı çekirdeği (core) çağırır.

```text
core/                  # Ortak Çekirdek (Core Pipeline)
│  ├── search.py       # Görsel arama + API entegrasyonu + indirme
│  ├── detector.py     # YOLOE-26 + SAM Sarmalayıcı (Modeller açılışta / ilk ihtiyaçta yüklenir)
│  ├── pipeline.py     # Arama -> İndirme -> Tespit -> Filtreleme akışı
│  ├── mapping.py      # Türkçe - İngilizce kelime eşleme tablosu
│  └── config.py       # Ayarlar, model boyutları, eşikler ve API Key yönetimi
web/                   # Web Arayüzü Katmanı
│  ├── main.py         # FastAPI Backend uygulaması ve uç noktalar (Endpoints)
│  └── static/         # Sade HTML + CSS + JavaScript (Fetch API) frontend arayüzü
cli/                   # Komut Satırı Katmanı
│  └── __main__.py     # Typer tabanlı CLI uygulaması
models/                # YOLOE-26 / SAM Ağırlıkları (Docker build sırasında indirilir)
downloads/             # İndirilen görseller için geçici klasör (Disk dolmaması için temizlenir)
tests/                 # Pytest test senaryoları
Dockerfile             # Tek CPU imajı için çok aşamalı (multi-stage) Docker dosyası
requirements.txt       # Bağımlılık listesi (CPU-only PyTorch dahil)
.env.example           # API Key şablonu (Gerçek .env dosyası gitignore'dadır)
```

---

## 🛠️ Teknoloji Yığını (Tech Stack)

*   **Çekirdek Dil:** Python 3.11+
*   **Nesne Tespiti & Yapay Zekâ:** Ultralytics, YOLOE-26 (Açık-sözlüklü / Open-vocabulary nesne tespiti)
*   **Segmentasyon:** Meta SAM (Segment Anything Model — mobile_sam), piksel-piksel maske üretimi
*   **Web Backend:** FastAPI + Uvicorn (Otomatik Swagger dokümantasyonu `/docs` adresindedir)
*   **Web Frontend:** Pure HTML, CSS, JavaScript (Fetch API)
*   **CLI (Komut Satırı):** Typer
*   **HTTP & Görsel İndirme:** HTTPX veya Requests
*   **Görsel İşleme:** Pillow (PIL)
*   **Görsel Kaynağı:** Pixabay veya Pexels API
*   **Paketleme:** Docker (Python 3.11-slim + CPU-only PyTorch)

---

## 🔄 Çalışma Akışı (Pipeline Execution)

1.  **Girdi:** Kullanıcı bir kelime girer (Örneğin: `"at"`).
2.  **Çeviri & Eşleme:** Kelime `mapping.py` kullanılarak İngilizceye çevrilir (`"horse"`). Çeviri, hem arama motorunun zengin sonuç getirmesi hem de YOLOE-26'nın metin kodlayıcısının (text encoder) İngilizce ile daha optimize çalışması için kritik öneme sahiptir.
3.  **Arama:** Arama API'sine sorgu gönderilir ve $N$ adet görsel URL'i alınır.
4.  **İndirme:** Görseller geçici olarak `downloads/` klasörüne indirilir.
5.  **Doğrulama (AI):** Uygulama açılışında belleğe 1 kez yüklenen YOLOE-26 modeli, `set_classes(["horse"])` hedeflemesiyle her görseli tarar.
6.  **Filtreleme & Skorlama:** Belirlenen güven eşiğinin (varsayılan `0.5`) üzerindeki nesneler Başarılı (`✓ [Güven Oranı]`), altındakiler ise Başarısız (`X`) olarak işaretlenir.
7.  **Segmentasyon (opsiyonel):** İstenirse, YOLOE-26'nın bulduğu bounding box'lar SAM modeline (`mobile_sam`) prompt olarak verilir ve nesnenin piksel-piksel sınırlarını çizen bir segmentasyon maskesi üretilir. SAM, sadece ihtiyaç anında (lazy-loading) belleğe alınır, böylece segmentasyon kullanılmayan senaryolarda başlangıç süresi etkilenmez.
8.  **Çıktı:**
    *   **Web'de:** Görsel grid yapısında gösterilir; her görselin üstünde `✓/X` etiketi, güven oranı ve indirme butonu yer alır.
    *   **CLI'da:** Doğrulamadan geçen başarılı görseller belirtilen çıktı klasörüne kaydedilir.

---

## 🧩 Öne Çıkan Özellikler

*   **YOLOE-26 (Açık-sözlüklü Tespit):** Önceden tanımlı sınıflarla sınırlı kalmadan, kullanıcının girdiği herhangi bir kelimeyi (`set_classes`) hedef alarak nesne tespiti yapar.
*   **SAM Segmentasyon Desteği:** YOLOE-26'nın ürettiği bounding box'lar Meta'nın SAM (mobile_sam) modeline aktarılır ve nesnenin sadece kutusu değil, gerçek piksel sınırları (maske) elde edilir. İki model aynı akış içinde birlikte çalışabilir; SAM modeli lazy-loading ile yüklenir, YOLOE-26'nın başlangıç performansını etkilemez.

---

## 📦 Kurulum ve Çalıştırma

### 1. Yerel Ortamda Kurulum (Lokal Geliştirme)

Öncelikle bir sanal ortam oluşturun ve bağımlılıkları yükleyin:

```bash
# Projeyi klonlayın
git clone https://github.com/dilanurbal/PicFetch.git
cd PicFetch

# Sanal ortam oluşturun ve aktif edin
python -m venv venv
source venv/bin/activate  # Windows için: venv\Scripts\activate

# Bağımlılıkları yükleyin
pip install -r requirements.txt
```

#### Ortam Değişkenlerinin Ayarlanması:
`.env.example` dosyasını `.env` olarak kopyalayın ve Pixabay veya Pexels platformundan aldığınız API anahtarını ekleyin:

```bash
cp .env.example .env
```
`.env` içeriği:
```env
PIXABAY_API_KEY=your_api_key_here
DEFAULT_MODEL_SIZE=small
CONFIDENCE_THRESHOLD=0.5
SAM_MODEL_SIZE=mobile
```

#### Model Ağırlıkları Hakkında Not:
YOLOE-26 ve SAM (mobile_sam) ağırlıkları repoya dahil değildir; `ultralytics` kütüphanesi, modeller ilk kez kullanıldığında bunları otomatik olarak indirir. Bu nedenle uygulamanın ilk çalıştırılışında (veya Docker build aşamasında) internet bağlantısı gereklidir.

#### CLI Uygulamasını Çalıştırma:
```bash
python -m cli --query "at" --output ./sonuclar
```

#### Web Uygulamasını Çalıştırma:
```bash
uvicorn web.main:app --reload
```
Tarayıcınızdan `http://127.0.0.1:8000` adresine giderek arayüze erişebilir, `http://127.0.0.1:8000/docs` adresinden Swagger API dokümantasyonunu inceleyebilirsiniz.

### 2. Docker ile Çalıştırma (Önerilen / Taşınabilir Mod)

Uygulama, taşınabilirlik odağıyla **GPU gerektirmeden, her CPU mimarisinde** çalışabilecek şekilde paketlenmiştir. Model ağırlıkları build aşamasında imaja gömüldüğü için ilk çalıştırmada internet üzerinden ağırlık indirme beklemesi yaşanmaz.

```bash
# Docker imajını oluşturun (Build aşamasında model ağırlıkları indirilir)
docker build -t gorsel-dogrulama-app .

# Konteyneri ayağa kaldırın
docker run -d -p 8000:8000 --env-file .env gorsel-dogrulama-app
```
Uygulama `http://localhost:8000` adresinde yayında olacaktır.

---

## ⚠️ Kenar Durumları ve Hata Yönetimi (Edge Cases)

Sistem, demoda ve canlı ortamda karşılaşılabilecek olası aksaklıklara karşı dirençli (resilient) tasarlanmıştır:
*   **Arama 0 Sonuç Döndürürse:** Uygulama çökmez, kullanıcıya "Sonuç bulunamadı" mesajı gösterilir.
*   **Kelime Eşleme Tablosunda Yoksa:** Kullanıcı uyarılır ve İngilizce terim girmesi önerilir.
*   **Bozuk Dosya/Görsel:** İndirilen görsel bozuksa o dosya atlanır ve pipeline kalan görsellerle devam eder.
*   **API Limiti Dolarsa:** Kullanıcıya dostça bir hata mesajı gösterilerek daha sonra tekrar denemesi istenir.
*   **Hiçbir Görsel Doğrulanamazsa ($X$):** Ekran boş bırakılmaz; görseller yine de gösterilir ancak üzerlerinde "Doğrulanamadı" etiketi yer alır.
*   **İnternet/API Erişimi Kesilirse:** Sistem çökmek yerine yakalanmış (handled) bir hata fırlatır.

---

## 👥 Katkıda Bulunanlar (Contributors)

*   **Dilanur Bal**
*   **Mert Atmaca**
*   **Ayşen Çiftçi**
*   **Ayşe Semra Yaslan**

---

## 👥 Ekip Rol Dağılımı (4 Kişi)

Proje, MVP (Minimum Viable Product) hedefine hızla ulaşmak için paralel iş paketlerine bölünmüştür:
*   **Kişi 1 (Arama Modülü):** API entegrasyonu, key yönetimi, görsel indirme süreçleri, rate-limit ve cache yönetimi. (`search.py`, `config.py`)
*   **Kişi 2 (Tespit Modülü):** YOLOE-26 ve SAM entegrasyonu, model yükleme, `set_classes` mekanizması ve çıktı formatlama. (`detector.py`)
*   **Kişi 3 (Web Katmanı):** FastAPI backend uç noktalarının yazılması ve HTML/JS tabanlı dinamik arama grid arayüzü. (`web/` klasörü)
*   **Kişi 4 (CLI, Docker & Entegrasyon):** Typer CLI geliştirilmesi, Dockerfile mimarisinin kurulması, test senaryoları (`tests/`) ve modüllerin birleştirilmesi.

---

## 💡 Önemli Geliştirici Notları

1.  **Model Optimizasyonu:** Modeller, her HTTP isteğinde (request) yeniden **yüklenmez**. YOLOE-26 uygulama ayağa kalkarken bir kez belleğe alınır; SAM ise ilk ihtiyaç anında (lazy-loading) yüklenir. Her ikisi de ortak pipeline tarafından singleton mantığıyla kullanılır.
2.  **Disk Yönetimi:** `downloads/` klasörüne indirilen görseller analiz edildikten ve istemciye/arayüze aktarıldıktan hemen sonra temizlenir. Sunucu disk alanı korunur.
3.  **Doğrulama Görünürlüğü (Demo Uyarısı):** Stok görsel sitelerindeki (Pixabay/Pexels) fotoğraflar zaten yüksek kaliteli etiketlere sahip olduğundan aranan nesne neredeyse her görselde bulunacaktır ($✓$). Demoda sistemin çalıştığını (eleme yaptığını) kanıtlamak adına; arayüzde elenen görselleri tamamen gizlemek yerine **"Elenenler"** başlığı altında veya pasifize edilmiş $X$ işaretiyle güven oranlarıyla birlikte göstermek kritik önem taşımaktadır.
