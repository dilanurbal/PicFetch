import os
import shutil
from typing import List, Dict, Any
# Semra ve Mert'in yazdığı modülleri import ediyoruz
from core.search import pexels_search_and_download
from core.detector import YOLOE26Detector

class PicFetchPipeline:
    def __init__(self, output_dir: str = "output_images"):
        self.output_dir = output_dir
        
        # 1. Önce models klasörü yoksa otomatik oluşturuyoruz:
        if not os.path.exists("models"):
            os.makedirs("models")
            
        # 2. Sonra Mert'in modelini ayağa kaldırıyoruz (CPU-only)
        self.detector = YOLOE26Detector(model_path="models/yoloe26.pt")
        
        # 3. Çıktı klasörünün denetimi
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)
    def run(self, query: str) -> List[Dict[str, Any]]:
        print(f"🚀 Pipeline başlatıldı. Kelime: '{query}'")
        
        # 1. Adım: Semra'nın koduyla görselleri indir (Geçici klasöre)
        temp_dir = "temp_downloaded_images"
        downloaded_files = pexels_search_and_download(query=query, target_dir=temp_dir)
        
        pipeline_results = []

        # 2. Adım: Mert'in koduyla nesne doğrulaması yap
        for file_path in downloaded_files:
            file_name = os.path.basename(file_path)
            print(f"🤖 {file_name} YOLOE-26 ile analiz ediliyor...")
            
            # Model tahmini (Mert'in fonksiyonuna göre isimlendirmeyi revize edebilirsin)
            is_verified, confidence = self.detector.predict(file_path, target_label=query)
            
            if is_verified:
                # Görsel doğrulandıysa nihai çıktı klasörüne taşı
                final_path = os.path.join(self.output_dir, file_name)
                shutil.move(file_path, final_path)
                
                pipeline_results.append({
                    "image": file_name,
                    "confidence": confidence,
                    "verified": True
                })
            else:
                # Doğrulanmadıysa geçici dosyayı temizle
                os.remove(file_path)
                pipeline_results.append({
                    "image": file_name,
                    "confidence": confidence,
                    "verified": False
                })

        # Geçici klasörü temizle
        if os.path.exists(temp_dir) and not os.listdir(temp_dir):
            os.rmdir(temp_dir)
            
        return pipeline_results