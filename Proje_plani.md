# Proje Planı: Görsel Bulma ve Doğrulama Uygulaması

*Ekip incelemesi için — güncel sürüm. Mentör eşliğinde güncellenmeye devam edecek.*

---

## 1. Projenin Amacı

Kullanıcının yazdığı bir kelimeye (ör. "at") göre internetten görsel bulan, bulunan görselleri indirmeye izin veren ve her görselde aranan nesnenin **gerçekten olup olmadığını** yapay zekâ ile doğrulayan bir uygulama. Hem web arayüzünden hem komut satırından (CLI) çalışır, en sonda Docker ile paketlenir.

**Örnek akış:** Kullanıcı "at" yazar → uygulama at görselleri getirir → her görseli YOLO ile kontrol eder → "bu görselde gerçekten at var (✓ %94)" veya "at bulunamadı (✗)" diye işaretler → kullanıcı beğendiğini indirir.

---

## 2. Temel Fikir

**İki katman (bu ayrım projenin özü):**

- **Arama katmanı — sınırsız.** İnternette milyonlarca etiketli görsel var; kullanıcı ne yazarsa (at, kuğu, bilgisayar, dağ...) arama onu bulup getirebilir. Burada "80 sınıf" gibi bir kısıt yok.
- **Doğrulama katmanı — YOLOE-26.** "Bu görselde gerçekten bu nesne var mı?" kontrolü. Açık-sözlüklü model kullandığımız için burada da geniş bir yelpaze mümkün.

**Tek çekirdek, iki yüz.** Uygulama mantığı (arama + indirme + doğrulama) tek bir Python paketinde toplanır; web arayüzü ve CLI bu **aynı** çekirdeği çağırır. Kod tekrarı olmaz, test kolaylaşır, Docker paketlemesi sadeleşir.

---

## 3. Alınan Kararlar (Özet)

| Konu | Karar | Not |
|------|-------|-----|
| Dil / çekirdek | Python 3.11+ | YOLO ekosistemi Python |
| Nesne tespiti | **Tek YOLOE-26 (açık-sözlük)** | Her kelime için tek model; 80 içi + dışı hepsini kapsar |
| Model boyutu | Varsayılan küçük (nano/small) | Güçlü makinede büyütülebilir |
| Görsel arama | Pixabay veya Pexels (ücretsiz, yasal) | Bing API kapandı; scraping yapılmayacak |
| Web backend | FastAPI | Otomatik Swagger arayüzü (`/docs`) |
| CLI | Typer | |
| Frontend | Basit HTML + JS | Sadelik için; React opsiyonel |
| Docker | **Tek CPU imajı, tek Dockerfile** | Her makinede kurulumsuz çalışır |
| Donanım | CPU temel, GPU opsiyonel hızlandırıcı | Taşınabilirlik önceliği |

---

## 4. MVP — Önce Bunu Bitirin

Bir staj projesinde en büyük risk, özelliklere boğulup bitirememektir. O yüzden "en az ne olursa proje çalışıyor sayılır?"ı baştan tanımlıyoruz:

> **MVP:** Web arayüzünde bir kelime yaz → görseller gelsin → YOLOE-26 her birini ✓/✗ (güven oranıyla) işaretlesin → beğenileni indir. Tek nesne, sade arayüz, süs yok.

Bu omurga çalışınca proje "var" olur. Mod düğmesi, çoklu nesne, cila, gelişmiş CLI — hepsi bunun **üstüne** eklenir. Vaktiniz daralsa bile elinizde çalışan bir şey kalır.

**Önerilen sıra:** çekirdek (arama + tespit + pipeline) → CLI (en sade yüz, çekirdeği doğrular) → web MVP → sonra cila / ekstralar.

---

## 5. Nasıl Çalışıyor (Pipeline Akışı)

1. Kullanıcı bir kelime yazar → "at"
2. Kelime İngilizceye çevrilir → "horse". Bu İngilizce **hem aramada hem YOLOE isteminde** kullanılır (İngilizce sorgu genelde daha çok/iyi sonuç getirir; YOLOE'nin metin kodlayıcısı da İngilizceyle daha iyi çalışır).
3. Görsel arama API'sine "horse" sorulur → N tane görsel URL'i döner
4. Görseller geçici bir klasöre indirilir
5. YOLOE-26 (uygulama açılışında **bir kez** yüklenmiştir) `set_classes(["horse"])` ile hedeflenir ve her görsel işlenir
6. Hedef nesne, belirlenen güven eşiğinin (ör. 0.5) üzerinde tespit edildiyse **geçti ✓ (+oran)**, değilse **eledi ✗**
7. Sonuç döner:
   - **Web:** küçük resim grid'i + her görselde ✓/✗ etiketi + güven oranı + indirme butonu
   - **CLI:** geçen görseller bir çıktı klasörüne kaydedilir

Tek model kullandığımız için her sorgu aynı yolu izler — "kelime 80 içinde mi?" gibi bir kontrole veya ikinci bir modele gerek yoktur. Sadelik buradan geliyor.

---

## 6. Teknoloji Yığını

- **Çekirdek:** Python 3.11+
- **Tespit:** `ultralytics` paketi, YOLOE-26 (açık-sözlüklü, küçük varyant — kesin checkpoint adı güncel dokümandan teyit edilecek)
- **Web backend:** FastAPI (+ uvicorn)
- **CLI:** Typer
- **Görsel indirme / HTTP:** httpx veya requests
- **Görsel işleme:** Pillow
- **Frontend:** sade HTML + CSS + JavaScript (fetch), FastAPI tarafından sunulur
- **Arama kaynağı:** Pixabay veya Pexels API (ücretsiz kayıt, API key gerekir)
- **Paketleme:** Docker — tek CPU imajı, tek Dockerfile (docker-compose'a gerek yok, çünkü frontend'i FastAPI sunuyor)

---

## 7. Klasör Yapısı

```
proje/
├── core/                  # ortak çekirdek (hem CLI hem web kullanır)
│   ├── search.py          # görsel arama + indirme
│   ├── detector.py        # YOLOE-26 sarmalayıcı (model açılışta 1 kez yüklenir)
│   ├── pipeline.py        # arama → indir → tespit → filtrele
│   ├── mapping.py         # Türkçe → İngilizce kelime eşlemesi
│   └── config.py          # ayarlar, model boyutu, eşik, API key (env'den)
├── web/
│   ├── main.py            # FastAPI uygulaması (endpoint'ler)
│   └── static/            # basit HTML + JS + CSS arayüz
├── cli/
│   └── __main__.py        # Typer CLI
├── models/                # YOLOE-26 ağırlıkları (build'de indirilir)
├── downloads/             # indirilen görseller için geçici klasör (biriktirilmez)
├── tests/                 # pytest testleri
├── Dockerfile             # tek CPU imajı
├── requirements.txt
├── .env.example           # API key şablonu (gerçek .env gitignore'da)
├── .gitignore
└── README.md
```

---

## 8. Donanım ve Taşınabilirlik Stratejisi

**Prensip: CPU temel alınır, GPU opsiyonel bonus sayılır.** Uygulama en zayıf makinede rahat çalışacak şekilde tasarlanır; güçlü makinede otomatik hızlanır.

- **Otomatik cihaz seçimi:** Ultralytics, GPU varsa GPU'yu, yoksa CPU'yu kendiliğinden kullanır. Tek kod, her donanımda çalışır.
- **Varsayılan küçük model:** nano/small her yerde akıcı çalışır. Güçlü makinesi olan için "hızlı mod / doğru mod" ayarı bırakılır (daha büyük modele geçiş).
- **Bellek:** 16 GB RAM / 8 GB VRAM fazlasıyla yeter. Model ağırlıkları minik (onlarca MB); asıl yükü paylaşılan PyTorch taşır. Zayıf makinelerde de sorun çıkarmaz.
- **Zayıf makine için ek kaldıraçlar (gerekirse):** aramada daha az görsel işlemek (30 yerine 8-10), çözünürlüğü düşürmek (640→480), ileri seviye ONNX/OpenVINO export.

---

## 9. Docker Yaklaşımı (Tek CPU İmajı)

- **Tek CPU imajı, tek Dockerfile.** CPU-only PyTorch ile derlenir → her makinede, GPU sürücüsü/toolkit gerekmeden, tek komutla çalışır.
- **Ağırlıklar imaja gömülür.** Build sırasında indirilir ki ilk çalıştırmada internet gerekmesin.
- **İmajı küçük tutma:** `python:3.11-slim` taban + CPU-only torch + çok-aşamalı (multi-stage) build → ~2-3 GB.
- **GPU nerede?** GPU yalnızca geliştirme sırasında (Docker'sız, yerel ortamda) kullanılır. Teslim edilen / demo yapılan konteyner CPU imajıdır. Böylece güçlü GPU geliştirmeyi hızlandırır ama taşınabilirliği bozmaz.
- İleride vakit kalırsa GPU'lu ikinci bir imaj eklenebilir (opsiyonel, bu yolun üstüne).

---

## 10. Yol Haritası (Fazlar)

**Faz 0 — Kurulum & kararlar:** Git repo (main + feature branch, PR ile merge), klasör iskeleti, ortak Python ortamı, görev panosu, API key'lerini alma. Çekirdek "sözleşmesini" netleştir: `pipeline.run("at")` ne döndürecek?

**Faz 1 — Çekirdek modüller (paralel):** `search.py` ve `detector.py` bağımsız çalışır hale gelsin, küçük test script'leriyle doğrulansın.

**Faz 2 — Pipeline:** İkisini `pipeline.py`'de birleştir + eşleme tablosunu ekle. "at" verince gerçekten at içeren görseller dönsün.

**Faz 3 — CLI:** Typer ile. Web'den önce yapılır; çekirdek mantığını sağlamlaştırır.

**Faz 4 — Web backend:** FastAPI endpoint'leri, `/docs` otomatik gelir.

**Faz 5 — Web frontend:** Arama kutusu, sonuç grid'i, ✓/✗ etiketi + güven oranı, indirme butonu. *(Faz 1–5 = MVP'yi tamamlar.)*

**Faz 6 — Docker:** Tek CPU imajı, ağırlıklar gömülü, tek komutla çalışır.

**Faz 7 — Cila, test, demo:** Hata yönetimi, kenar durumları, pytest testleri, README, sunum.

> **Zaman planı:** Fazlara mentörünüzle kaba süre biçin. Ağırlığı işin kalbi olan **çekirdek + pipeline**'a verin; **Docker + cila**'ya sandığınızdan fazla pay bırakın (bu kısımlar hep uzar). Staj süresine göre bir takvim çıkarıp görev panosuna işleyin.

---

## 11. Dikkat Edilecekler

- **⚠️ Doğrulama görünür olsun (en sinsi risk):** Pixabay/Pexels görselleri çok iyi etiketli döndürür — "at" arayınca gelen her görselde zaten at vardır, dolayısıyla YOLOE hepsini ✓ geçer, hiçbir şeyi elemez. Bu durumda projenin en havalı kısmı (doğrulama) demoda **hiçbir şey yapmıyormuş gibi** görünür. Çözümler: güven oranını ✓ durumunda da hep göster; elenenleri gizlemek yerine "şunlar elendi" diye göster; demoya kasıtlı olarak filtrenin çalıştığı bir örnek hazırla. **Sunumun can alıcı noktası budur — mentörle konuşun.**
- **Model bir kez yüklenir:** Model, her istekte değil, uygulama açılırken bir kez belleğe alınıp tutulmalı. Aksi halde her arama gereksiz yavaşlar.
- **İndirilen görseller geçici kalır:** Görseller geçici bir klasöre indirilir ve biriktirilmez (iş bitince temizlenir), yoksa disk zamanla dolar.
- **Güven eşiği:** çok yüksek → gerçek atları eler; çok düşük → yanlış pozitif kabul eder. Deneyerek ayarla (ör. 0.5'ten başla).
- **Türkçe→İngilizce eşleme:** "at→horse" kolay ama "çanta→handbag mı backpack mi?", yazım hataları vb. düşünülmeli. İngilizce karşılık hem aramada hem YOLOE isteminde kullanılır. Desteklenecek kelime kümesi netleştirilmeli.
- **Açık-sözlük sınırı:** net, somut nesneler (kuğu, sırt çantası) iyi çalışır; renk + nesne (kırmızı bardak) makul; şekilsiz/soyut şeyler (kırmızı taş, dağ) modeli zorlar. Kullanıcıya beklenti yönetimi yapılmalı.
- **API key güvenliği:** repo'ya konmaz. `.env` + `.gitignore`; `.env.example` şablonu paylaşılır.
- **Görsel lisansları:** stok API'ler (Pixabay/Pexels) lisansları net olduğu için tercih edilir.
- **Docker imaj boyutu:** CPU-only torch + slim base ile kontrol altında tutulur.

---

## 12. Kenar Durumları (Baştan Planlanmalı)

Demoda kesinlikle karşılaşacağınız durumlar ve her biri için beklenen davranış:

| Durum | Ne yapılmalı |
|-------|--------------|
| Arama 0 sonuç döndü | "Sonuç bulunamadı" mesajı göster, çökme |
| Kelime eşlemede yok | Kullanıcıyı uyar / İngilizce girmesini öner / eşlemeye ekle |
| İndirilen dosya bozuk | O görseli atla, kalanlarla devam et |
| API limiti doldu | Nazik hata mesajı + "biraz sonra tekrar dene" |
| Hiçbir görsel doğrulanamadı (hepsi ✗) | Yine de göster, "doğrulanamadı" etiketiyle; boş ekran bırakma |
| İnternet/API erişimi yok | Anlaşılır hata; uygulama çökmesin |

---

## 13. Karar ve Teyit Notları

**Kesinleşen kararlar:**
- Nesne tespiti: **tek YOLOE-26** (yönlendirme/ensemble değil).
- Docker: **tek CPU imajı, tek Dockerfile**.
- Frontend: **sade HTML + JS** ile başlanacak (React opsiyonel, zaman kalırsa).

**Mentör/ekiple netleştirilecekler:**
1. **Arama kaynağı:** Pixabay mı, Pexels mi? (İndirip kendi tarafında işleme akışı için Pixabay biraz daha uygun.)
2. **Desteklenen kelime kapsamı:** Her kelimeyi mi kabul edeceğiz, yoksa belirli bir liste mi? Eşleme tablosunun sınırı.
3. **Model boyutu varsayılanı:** nano mı, small mı? "Hızlı/doğru mod" ayarı olacak mı?
4. **Zaman planı:** Staj süresine göre fazların takvimi.

---

*Bu plan bir başlangıç çerçevesidir; mentör eşliğinde ve ekip incelemesiyle güncellenecektir.*
