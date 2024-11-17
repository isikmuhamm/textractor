import os
from typing import List, Set, Dict, Optional
from .extractors.base_extractor import BaseExtractor
from .extractors.text_extractor import TextExtractor
from .extractors.office_extractor import OfficeExtractor
from .extractors.pdf_extractor import PDFExtractor
from .utils.file_utils import FileUtils
from .utils.logger import logger

class FileProcessor:
    def __init__(self, max_file_size_mb: float = 5.0, output_file: str = "merged_content.txt"):
        """
        FileProcessor sınıfının başlatıcısı
        
        Args:
            max_file_size_mb (float): İşlenecek maksimum dosya boyutu (MB)
            output_file (str): Çıktı dosyasının adı
        """
        self.max_file_size_mb = max_file_size_mb
        self.output_file = output_file
        self.processed_files: Set[str] = set()
        self.error_files: Dict[str, str] = {}
        
        # Extractors'ları başlat
        self.extractors: List[BaseExtractor] = [
            TextExtractor(),
            OfficeExtractor(),
            PDFExtractor()
        ]
        
        # File utils'i başlat
        self.file_utils = FileUtils()

    def can_process_file(self, file_path: str) -> bool:
        """
        Dosyanın işlenip işlenemeyeceğini kontrol eder
        
        Args:
            file_path (str): Dosya yolu
            
        Returns:
            bool: İşlenebilir ise True, değilse False
        """
        # Dosya boyutunu kontrol et
        if self.file_utils.get_file_size_mb(file_path) > self.max_file_size_mb:
            logger.warning(f"{file_path} dosyası boyut limitini ({self.max_file_size_mb}MB) aşıyor.")
            return False

        # Binary kontrolü
        if self.file_utils.is_binary_file(file_path):
            # Extractorların desteklediği binary dosyalar için devam et
            for extractor in self.extractors:
                if extractor.can_handle(file_path):
                    return True
            return False

        # Text dosyaları için TextExtractor'ı kontrol et
        return any(extractor.can_handle(file_path) for extractor in self.extractors)

    def extract_content(self, file_path: str) -> Optional[str]:
        """
        Dosyadan içerik çıkarır
        
        Args:
            file_path (str): Dosya yolu
            
        Returns:
            Optional[str]: Çıkarılan içerik veya None
        """
        for extractor in self.extractors:
            if extractor.can_handle(file_path):
                content = extractor.extract_text(file_path)
                if content:
                    return self.format_content(file_path, content)
        return None

    def format_content(self, file_path: str, content: str) -> str:
        """
        Dosya içeriğini formatlar
        
        Args:
            file_path (str): Dosya yolu
            content (str): Dosya içeriği
            
        Returns:
            str: Formatlanmış içerik
        """
        separator = "-" * 80
        return f"""
{separator}
Dosya: {file_path}
Boyut: {self.file_utils.get_file_size_mb(file_path):.2f}MB
MIME Type: {self.file_utils.get_mime_type(file_path)}
{separator}
{content}
{separator}

"""

    def process_file(self, file_path: str) -> Optional[str]:
        """
        Tek bir dosyayı işler
        
        Args:
            file_path (str): Dosya yolu
            
        Returns:
            Optional[str]: İşlenmiş dosya içeriği veya None
        """
        if file_path in self.processed_files:
            return None

        try:
            if not os.path.exists(file_path):
                logger.error(f"Dosya bulunamadı: {file_path}")
                return None

            if not self.can_process_file(file_path):
                logger.warning(f"Dosya desteklenmiyor: {file_path}")
                return None

            content = self.extract_content(file_path)
            if content:
                self.processed_files.add(file_path)
                return content
            else:
                logger.warning(f"Dosya boş: {file_path}")
                return None
            
        except Exception as e:
            self.error_files[file_path] = str(e)
            logger.error(f"Dosya işlenirken hata oluştu {file_path}: {str(e)}")
        
        logger.warning(f"Hesapta olmayan bir sorun var: {file_path}")
        return None

    def process_directory(self, directory_path: str) -> List[str]:
        """
        Bir dizini ve alt dizinlerini işler
        
        Args:
            directory_path (str): Dizin yolu
            
        Returns:
            List[str]: İşlenmiş içerikler listesi
        """
        contents = []
        
        try:
            for root, _, files in os.walk(directory_path):
                for file in files:
                    file_path = os.path.join(root, file)
                    content = self.process_file(file_path)
                    if content:
                        contents.append(content)
                        
        except Exception as e:
            logger.error(f"Dizin işlenirken hata oluştu: {str(e)}")
            
        return contents

    def save_output(self, contents: List[str]) -> None:
        """
        İşlenmiş içerikleri dosyaya kaydeder
        
        Args:
            contents (List[str]): İşlenmiş içerikler listesi
        """
        try:
            with open(self.output_file, 'w', encoding='utf-8') as f:
                f.write('\n'.join(contents))
            logger.info(f"İçerikler {self.output_file} dosyasına kaydedildi.")
        except Exception as e:
            logger.error(f"Dosya kaydedilirken hata oluştu: {str(e)}")

    def process(self, path: str) -> None:
        """
        Ana işleme fonksiyonu
        
        Args:
            path (str): İşlenecek dosya veya dizin yolu
        """
        contents = []
        
        try:
            if os.path.isfile(path):
                content = self.process_file(path)
                if content:
                    contents.append(content)
            elif os.path.isdir(path):
                contents.extend(self.process_directory(path))
            else:
                logger.error(f"Geçersiz yol: {path}")
                return

            if contents:
                self.save_output(contents)
                logger.info(f"Toplam {len(self.processed_files)} dosya başarıyla işlendi.")
                if self.error_files:
                    logger.warning(f"{len(self.error_files)} dosya işlenemedi:")
                    for file_path, error in self.error_files.items():
                        logger.warning(f"- {file_path}: {error}")
            else:
                logger.warning("İşlenebilecek dosya bulunamadı.")
                
        except Exception as e:
            logger.error(f"İşlem sırasında beklenmeyen hata: {str(e)}")