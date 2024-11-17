from typing import Optional, Set
import numpy as np
from tensorflow.keras.models import load_model #type: ignore
from ..utils.logger import logger
from .base_extractor import BaseExtractor


class ModelExtractor(BaseExtractor):
    # Desteklenen model dosyası uzantıları
    SUPPORTED_EXTENSIONS: Set[str] = {
        '.h5', '.keras', '.npy'
    }

    def can_handle(self, file_path: str) -> bool:
        """Dosya uzantısının desteklenip desteklenmediğini kontrol eder."""
        ext = file_path.lower().split('.')[-1] if '.' in file_path else ''
        return f'.{ext}' in self.SUPPORTED_EXTENSIONS

    def extract_model(self, file_path: str):
        """Model dosyasını okur ve içeriğini döner."""
        ext = file_path.lower().split('.')[-1]
        
        try:
            if ext in ['h5', 'keras']:
                return self._extract_keras_model(file_path)
            elif ext == 'npy':
                return self._extract_npy(file_path)
            else:
                logger.warning(f"Desteklenmeyen model dosya formatı: {file_path}")
                return None
        except Exception as e:
            logger.error(f"Model dosyası okuma hatası {file_path}: {str(e)}")
            return None

    def _extract_keras_model(self, file_path: str):
        """Keras modelini dosyadan yükler."""
        try:
            logger.info(f"Keras modeli yükleniyor: {file_path}")
            return load_model(file_path)
        except Exception as e:
            logger.error(f"Keras model yükleme hatası {file_path}: {str(e)}")
            raise RuntimeError(f"Keras model yükleme hatası: {e}")

    def _extract_npy(self, file_path: str) -> np.ndarray:
        """NPY dosyasını okur."""
        try:
            logger.info(f"NPY dosyası yükleniyor: {file_path}")
            return np.load(file_path, allow_pickle=True)
        except Exception as e:
            logger.error(f"NPY dosya okuma hatası {file_path}: {str(e)}")
            raise RuntimeError(f"NPY dosya okuma hatası: {e}")
