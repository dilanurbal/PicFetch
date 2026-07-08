"""
pipeline.py - Core Pipeline Entegrasyonu

Tüm modülleri birleştirir:
Türkçe kelime → İngilizce çeviri → Görsel arama → İndirme → YOLOE-26 ile doğrulama → Sonuç
"""

from pathlib import Path
from typing import List, Dict
from .mapping import translate_to_english
from .search import ImageSearcher
from .detector import ObjectDetector  # Detector modülü hazır olduğunu varsayıyoruz
from .cleanup import cleanup_downloads
from .config import get_config


class ImagePipeline:
    """
    Ana pipeline sınıfı. Tüm işlem akışını yönetir.
    """
    
    def __init__(self):
        config = get_config()
        
        # Modülleri başlat
        self.searcher = ImageSearcher()
        self.detector = ObjectDetector()  # Detector'ı başlat
        self.confidence_threshold = config.get("confidence_threshold", 0.5)
        self.max_images = config.get("max_images", 10)
    
    def run(self, turkish_query: str) -> List[Dict]:
        """
        Ana pipeline akışı.
        
        Args:
            turkish_query: Türkçe arama kelimesi (örn: "at")
        
        Returns:
            Sonuç listesi. Her sonuç:
            {
                "filepath": "downloads/horse-123.jpg",
                "is_valid": True/False,
                "confidence": 0.94,
                "label": "horse"
            }
        """
        print(f"🔍 Pipeline başlatılıyor: '{turkish_query}'")
        print("=" * 60)
        
        results = []
        
        try:
            # ADIM 1: Türkçe → İngilizce çeviri
            print("\n1️⃣ Türkçe kelime İngilizce'ye çevriliyor...")
            english_query = translate_to_english(turkish_query)
            print(f"   ✅ '{turkish_query}' → '{english_query}'")
            
            # ADIM 2: Görsel arama
            print(f"\n2️⃣ Pixabay'de '{english_query}' aranıyor...")
            image_urls = self.searcher.search_images(
                query=english_query,
                per_page=self.max_images
            )
            print(f"   ✅ {len(image_urls)} görsel bulundu")
            
            if not image_urls:
                print("   ⚠️ Hiç sonuç bulunamadı!")
                return []
            
            # ADIM 3: YOLOE-26 için hedef sınıfı ayarla
            print(f"\n3️⃣ YOLOE-26 modeli '{english_query}' sınıfına ayarlanıyor...")
            self.detector.set_classes([english_query])
            print(f"   ✅ Model hazır")
            
            # ADIM 4: Her görseli indir ve doğrula
            print(f"\n4️⃣ Görseller indiriliyor ve doğrulanıyor...")
            for idx, url in enumerate(image_urls, 1):
                print(f"\n   📥 Görsel {idx}/{len(image_urls)} indiriliyor...")
                
                # Görseli indir
                filepath = self.searcher.download_image(url)
                
                if not filepath:
                    print(f"   ⚠️ İndirme başarısız, atlanıyor...")
                    continue
                
                # Görselin geçerli olduğunu kontrol et
                if not self.searcher.is_valid_image(filepath):
                    print(f"   ⚠️ Bozuk dosya, siliniyor...")
                    Path(filepath).unlink(missing_ok=True)
                    continue
                
                print(f"   ✅ İndirildi: {filepath}")
                
                # ADIM 5: YOLOE-26 ile nesne tespiti
                print(f"   🔎 YOLOE-26 ile doğrulama yapılıyor...")
                detection_result = self.detector.detect(filepath)
                
                # Sonuçları işle
                if detection_result and len(detection_result) > 0:
                    # Nesne bulundu
                    best_detection = max(detection_result, key=lambda x: x['confidence'])
                    is_valid = best_detection['confidence'] >= self.confidence_threshold
                    
                    result = {
                        "filepath": filepath,
                        "is_valid": is_valid,
                        "confidence": best_detection['confidence'],
                        "label": best_detection.get('label', english_query)
                    }
                    
                    status = "✅ DOĞRULANDI" if is_valid else "❌ ELENEDİ"
                    print(f"   {status} (Güven: {best_detection['confidence']:.2%})")
                    
                else:
                    # Nesne bulunamadı
                    result = {
                        "filepath": filepath,
                        "is_valid": False,
                        "confidence": 0.0,
                        "label": english_query
                    }
                    print(f"   ❌ ELENEDİ (Nesne bulunamadı)")
                
                results.append(result)
            
            # Özet
            print("\n" + "=" * 60)
            print("📊 PIPELINE ÖZET")
            print("=" * 60)
            valid_count = sum(1 for r in results if r['is_valid'])
            print(f"Toplam işlenen: {len(results)}")
            print(f"Doğrulanan (✅): {valid_count}")
            print(f"Elenen (❌): {len(results) - valid_count}")
            print("=" * 60)
            
            return results
            
        except Exception as e:
            print(f"\n❌ Pipeline hatası: {e}")
            import traceback
            traceback.print_exc()
            return []
        
        finally:
            # İşlem bitince geçici dosyaları temizle
            print("\n🧹 Geçici dosyalar temizleniyor...")
            cleanup_downloads()
            print("✅ Temizlik tamamlandı")


# Test için
if __name__ == "__main__":
    print("🧪 Pipeline Testi")
    print("=" * 60)
    
    pipeline = ImagePipeline()
    results = pipeline.run("at")
    
    print("\n📋 SONUÇLAR:")
    for idx, result in enumerate(results, 1):
        status = "✅" if result['is_valid'] else "❌"
        print(f"{idx}. {status} {result['filepath']} (Güven: {result['confidence']:.2%})")