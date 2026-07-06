"""
cleanup.py - Geçici Dosya Temizleme Modülü

Pipeline (iş akışı) tamamlandıktan sonra geçici 'downloads/' 
klasörünü silerek diskte gereksiz yer kaplanmasını engeller.
"""

import shutil
from pathlib import Path


def cleanup_downloads(folder_path: str = "downloads"):
    """
    Belirtilen geçici klasörü ve içindeki tüm dosyaları siler.
    
    Args:
        folder_path: Silinecek klasörün adı (varsayılan: 'downloads')
    """
    path = Path(folder_path)
    
    # Klasör var mı kontrol et
    if path.exists() and path.is_dir():
        try:
            # Klasörü ve içindeki her şeyi sil
            shutil.rmtree(path)
            print(f"✅ '{folder_path}' klasörü ve içindekiler başarıyla silindi.")
        except Exception as e:
            print(f"❌ Silme işlemi sırasında hata oluştu: {e}")
    else:
        print(f"ℹ️ '{folder_path}' klasörü bulunamadı, temizlik yapılmadı.")


# Test etmek için
if __name__ == "__main__":
    print("🧪 Cleanup Modülü Testi")
    print("=" * 40)
    
    # 1. Test için sahte bir klasör ve dosya oluşturalım
    test_dir = Path("test_cleanup")
    test_dir.mkdir(exist_ok=True)
    (test_dir / "fake_image.jpg").write_text("bu sahte bir resim verisi")
    print(f"📁 Test için '{test_dir}' klasörü oluşturuldu.")
    # ⏸️ 5 saniye bekle ki klasörü görebil
    print("⏸️ 5 saniye bekle, klasöre bakabilirsin...")
    import time
    time.sleep(5)
    
    # 2. Cleanup fonksiyonunu çağıralım
    cleanup_downloads("test_cleanup")
    
    # 3. Gerçekten silindi mi kontrol edelim
    if not test_dir.exists():
        print("✨ Test başarılı! Klasör gerçekten silindi.")
    else:
        print("❌ Test başarısız! Klasör hala duruyor.")