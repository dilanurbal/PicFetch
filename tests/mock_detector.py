"""
tests/mock_detector.py

core/detector.py icindeki `model` degiskeninin (ultralytics YOLOE ornegi)
arayuzunu taklit eden sahte bir detector. Gercek model agirligi
indirmeden/yuklemeden verify_target(), save_detection() ve
detect_and_segment() gibi fonksiyonlari test etmek icin kullanilir.

Skorlar MOCK_DATABASE'den (tests/mock_data.py) okunur, boylece arama ve
tespit mock'lari ayni sahte veriyi paylasir ve tutarli kalir.
"""

import os

from tests.mock_data import MOCK_DATABASE


class _TolistWrapper(list):
    """ultralytics'in torch tensor .tolist() arayuzunu taklit eden basit liste sarmalayicisi."""

    def tolist(self):
        return list(self)


class _MockBoxes:
    def __init__(self, confidences, xyxy):
        self.conf = _TolistWrapper(confidences)
        self.xyxy = _TolistWrapper(xyxy)


class _MockResult:
    def __init__(self, confidences, xyxy):
        self.boxes = _MockBoxes(confidences, xyxy)

    def save(self, filename: str):
        """Gercek bir goruntu islemeden, cagrildigini dogrulayabilecegimiz sahte bir dosya yazar."""
        directory = os.path.dirname(filename)
        if directory:
            os.makedirs(directory, exist_ok=True)
        with open(filename, "wb") as f:
            f.write(b"MOCK_RESULT_IMAGE")


class MockDetector:
    """
    ultralytics.YOLOE'nin kullandigimiz kismi arayuzunu (set_classes, predict)
    taklit eder. `core.detector.model` yerine konularak, gercek YOLOE/SAM
    agirliklari indirilmeden detector.py fonksiyonlari test edilebilir.
    """

    def __init__(self, *args, **kwargs):
        self._target = None

    def set_classes(self, classes: list):
        self._target = classes[0].strip().lower() if classes else None

    def predict(self, image_path, verbose: bool = False, **kwargs):
        """
        MOCK_DATABASE'deki kayitlara gore sahte bir Results listesi uretir.
        Hedef kelime MOCK_DATABASE'de yoksa, bos tespit listesi (found=False) doner.
        """
        entries = MOCK_DATABASE.get(self._target, [])

        if not entries:
            return [_MockResult([], [])]

        confidences = [entry["score"] for entry in entries]
        # Gercekci olmasi icin her tespit icin sahte bir bounding box uretiyoruz.
        xyxy = [[10, 10, 100, 100] for _ in entries]

        return [_MockResult(confidences, xyxy)]
