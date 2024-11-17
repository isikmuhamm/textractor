import chardet
from typing import Optional, Set
from .base_extractor import BaseExtractor
from ..utils.logger import logger

class TextExtractor(BaseExtractor):
    # Desteklenen metin dosyası uzantıları
    SUPPORTED_EXTENSIONS: Set[str] = {
        '.txt', '.csv', '.log', '.md',
        '.py', '.java', '.cpp', '.c', '.h', '.hpp',
        '.cs', '.js', '.ts', '.php', '.rb', '.go',
        '.rs', '.swift', '.kt', '.scala', '.pl',
        '.vb', '.r', '.sql', '.sh', '.bat', '.ps1',
        '.html', '.htm', '.css', '.jsx', '.tsx', '.vue',
        '.xml', '.json', '.yaml', '.yml', '.ini',
        '.conf', '.cfg', '.properties', '.def',
        '.ipynb', '.gradle', '.maven', '.sln',
        '.csproj', '.env', '.gitignore', '.editorconfig'
    }

    def can_handle(self, file_path: str) -> bool:
        """Dosya uzantısının desteklenip desteklenmediğini kontrol eder"""
        ext = file_path.lower().split('.')[-1] if '.' in file_path else ''
        return f'.{ext}' in self.SUPPORTED_EXTENSIONS

    def detect_encoding(self, file_path: str) -> str:
        """Dosyanın karakter kodlamasını tespit eder"""
        try:
            with open(file_path, 'rb') as file:
                raw_data = file.read()
                result = chardet.detect(raw_data)
                return result['encoding'] if result['encoding'] else 'utf-8'
        except Exception:
            return 'utf-8'

    def extract_text(self, file_path: str) -> Optional[str]:
        """Dosyadan text çıkarır"""
        try:
            encoding = self.detect_encoding(file_path)
            with open(file_path, 'r', encoding=encoding) as file:
                content = file.read()
                if any(ord(c) < 32 and c not in '\n\r\t' for c in content):
                    logger.warning(f"{file_path} binary içerik içeriyor olabilir.")
                    return None
                return content
        except Exception as e:
            logger.error(f"Text okuma hatası {file_path}: {str(e)}")
            return None