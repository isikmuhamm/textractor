from abc import ABC, abstractmethod
from typing import Optional

class BaseExtractor(ABC):
    """Temel extractor sınıfı"""
    
    @abstractmethod
    def can_handle(self, file_path: str) -> bool:
        """Bu extractor'ın dosyayı işleyip işleyemeyeceğini kontrol eder"""
        pass
        
    @abstractmethod
    def extract_text(self, file_path: str) -> Optional[str]:
        """Dosyadan text çıkarır"""
        pass