from typing import List

from pydantic import BaseModel


# Kullanıcıdan gelen görsel arama isteklerini temsil eden veri modeli.
class SearchRequest(BaseModel):
    query: str
    translate: bool = False
    target_lang: str = "tr"


# Görsel üzerindeki nesne tespiti ve doğrulama sonuçlarını temsil eden veri modeli.
class DetectionResult(BaseModel):
    image_id: str
    original_url: str
    is_verified: bool
    confidence_score: float


# Görsel arama ve nesne tespiti boru hattının (pipeline) nihai yanıt modelini temsil eder.
class PipelineResponse(BaseModel):
    search_keyword: str
    translated_keyword: str
    results: List[DetectionResult]


class ImageItem(BaseModel):
    id: str
    url: str


class DownloadZipRequest(BaseModel):
    selectedImageIds: List[str]
    images: List[ImageItem]

