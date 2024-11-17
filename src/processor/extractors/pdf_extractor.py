from typing import Optional
from pdfminer.high_level import extract_text
from .base_extractor import BaseExtractor
from ..utils.logger import logger

class PDFExtractor(BaseExtractor):
    def can_handle(self, file_path: str) -> bool:
        """Dosya uzantısının PDF olup olmadığını kontrol eder"""
        return file_path.lower().endswith('.pdf')

    def extract_text(self, file_path: str) -> Optional[str]:
        """PDF dosyasından text çıkarır"""
        try:
            return extract_text(file_path)
        except Exception as e:
            logger.error(f"PDF okuma hatası {file_path}: {str(e)}")
            return None