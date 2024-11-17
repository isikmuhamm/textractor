import os
import mimetypes
from typing import Set, Dict
import string

class FileUtils:
    # Binary dosya imzaları genişletilmiş liste
    BINARY_SIGNATURES: Set[bytes] = {
        # Images
        b'\x89PNG',           # PNG
        b'GIF8',             # GIF
        b'\xFF\xD8\xFF',     # JPEG
        b'BM',               # BMP
        b'\x00\x00\x01\x00', # ICO
        b'\x00\x00\x02\x00', # CUR
        b'II*\x00',          # TIFF
        b'MM\x00*',          # TIFF
        
        # Archives
        b'PK\x03\x04',       # ZIP, JAR, APK, DOCX, XLSX, PPTX
        b'Rar!\x1a\x07',     # RAR
        b'7z\xbc\xaf\x27',   # 7Z
        b'\x1f\x8b',         # GZ, TGZ
        b'BZh',              # BZ2
        
        # Documents
        b'%PDF',             # PDF
        b'{\\rtf',           # RTF
        b'\xD0\xCF\x11\xE0', # MS Office legacy (doc, xls, ppt)
        
        # Executables
        b'MZ',               # EXE, DLL
        b'\x7FELF',          # ELF (Linux executables)
        b'\xca\xfe\xba\xbe', # Mach-O (MacOS executables)
        b'\xfe\xed\xfa\xce', # Mach-O 32-bit
        b'\xfe\xed\xfa\xcf', # Mach-O 64-bit
        
        # Media
        b'ID3',              # MP3
        b'\x00\x00\x00\x20', # MP4
        b'RIFF',             # WAV, AVI
        b'OggS',             # OGG
        b'\x1a\x45\xdf\xa3', # WEBM, MKV
        
        # Database
        b'SQLite',           # SQLite
        b'\x53\x51\x4c',     # SQL dump
        
        # Other
        b'\x28\xb5\x2f\xfd', # ZST (Zstandard)
        b'\x04\x22\x4d\x18', # LZ4
    }

    # Kapsamlı MIME type haritası
    MIME_TYPES: Dict[str, str] = {
        # Programlama Dilleri
        '.h': 'text/x-c',
        '.c': 'text/x-c',
        '.cpp': 'text/x-c++',
        '.hpp': 'text/x-c++',
        '.cc': 'text/x-c++',
        '.cxx': 'text/x-c++',
        '.c++': 'text/x-c++',
        '.hxx': 'text/x-c++',
        '.h++': 'text/x-c++',
        '.py': 'text/x-python',
        '.pyw': 'text/x-python',
        '.java': 'text/x-java',
        '.js': 'text/javascript',
        '.ts': 'text/typescript',
        '.php': 'application/x-php',
        '.rb': 'text/x-ruby',
        '.go': 'text/x-go',
        '.rs': 'text/x-rust',
        '.swift': 'text/x-swift',
        '.kt': 'text/x-kotlin',
        '.kts': 'text/x-kotlin',
        '.scala': 'text/x-scala',
        '.pl': 'text/x-perl',
        '.sh': 'text/x-shellscript',
        '.bash': 'text/x-shellscript',
        '.zsh': 'text/x-shellscript',
        '.fish': 'text/x-shellscript',
        '.lua': 'text/x-lua',
        '.r': 'text/x-r',
        '.dart': 'text/x-dart',
        '.f': 'text/x-fortran',
        '.f90': 'text/x-fortran',
        '.cs': 'text/x-csharp',
        '.vb': 'text/x-vbnet',
        '.m': 'text/x-matlab',
        
        # Web teknolojileri
        '.html': 'text/html',
        '.htm': 'text/html',
        '.css': 'text/css',
        '.scss': 'text/x-scss',
        '.sass': 'text/x-sass',
        '.less': 'text/x-less',
        '.jsx': 'text/jsx',
        '.tsx': 'text/tsx',
        '.vue': 'text/vue',
        '.svelte': 'text/svelte',
        '.wasm': 'application/wasm',
        
        # Veri formatları
        '.json': 'application/json',
        '.xml': 'application/xml',
        '.yaml': 'text/yaml',
        '.yml': 'text/yaml',
        '.toml': 'text/toml',
        '.ini': 'text/plain',
        '.conf': 'text/plain',
        '.cfg': 'text/plain',
        '.csv': 'text/csv',
        '.tsv': 'text/tab-separated-values',
        '.md': 'text/markdown',
        '.markdown': 'text/markdown',
        '.rst': 'text/x-rst',
        '.txt': 'text/plain',
        '.log': 'text/plain',
        
        # Derleme ve yapılandırma
        '.o': 'application/x-object',
        '.ko': 'application/x-object',
        '.obj': 'application/x-object',
        '.lib': 'application/x-library',
        '.dll': 'application/x-msdownload',
        '.so': 'application/x-sharedlib',
        '.dylib': 'application/x-sharedlib',
        '.a': 'application/x-archive',
        '.cmake': 'text/x-cmake',
        '.makefile': 'text/x-makefile',
        '.mk': 'text/x-makefile',
        '.gradle': 'text/x-gradle',
        '.pom': 'text/xml',
        
        # IDE ve editör dosyaları
        '.project': 'text/xml',
        '.classpath': 'text/xml',
        '.sln': 'text/plain',
        '.vcxproj': 'text/xml',
        '.xcodeproj': 'text/plain',
        '.iml': 'text/xml',
        '.sublime-project': 'application/json',
        '.vscode': 'application/json',
        
        # Belgeler
        '.pdf': 'application/pdf',
        '.doc': 'application/msword',
        '.docx': 'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
        '.xls': 'application/vnd.ms-excel',
        '.xlsx': 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
        '.ppt': 'application/vnd.ms-powerpoint',
        '.pptx': 'application/vnd.openxmlformats-officedocument.presentationml.presentation',
        '.odt': 'application/vnd.oasis.opendocument.text',
        '.ods': 'application/vnd.oasis.opendocument.spreadsheet',
        '.odp': 'application/vnd.oasis.opendocument.presentation',
        '.pages': 'application/x-iwork-pages-sffpages',
        '.numbers': 'application/x-iwork-numbers-sffnumbers',
        '.key': 'application/x-iwork-keynote-sffkey',
        
        # Görüntüler
        '.jpg': 'image/jpeg',
        '.jpeg': 'image/jpeg',
        '.png': 'image/png',
        '.gif': 'image/gif',
        '.bmp': 'image/bmp',
        '.ico': 'image/x-icon',
        '.tiff': 'image/tiff',
        '.tif': 'image/tiff',
        '.svg': 'image/svg+xml',
        '.webp': 'image/webp',
        '.psd': 'image/vnd.adobe.photoshop',
        '.ai': 'application/postscript',
        '.eps': 'application/postscript',
        
        # Ses
        '.mp3': 'audio/mpeg',
        '.wav': 'audio/wav',
        '.ogg': 'audio/ogg',
        '.m4a': 'audio/mp4',
        '.wma': 'audio/x-ms-wma',
        '.flac': 'audio/flac',
        '.aac': 'audio/aac',
        '.mid': 'audio/midi',
        '.midi': 'audio/midi',
        
        # Video
        '.mp4': 'video/mp4',
        '.avi': 'video/x-msvideo',
        '.wmv': 'video/x-ms-wmv',
        '.mov': 'video/quicktime',
        '.mkv': 'video/x-matroska',
        '.webm': 'video/webm',
        '.flv': 'video/x-flv',
        '.mpeg': 'video/mpeg',
        '.mpg': 'video/mpeg',
        '.m4v': 'video/mp4',
        '.3gp': 'video/3gpp',
        
        # Sıkıştırılmış
        '.zip': 'application/zip',
        '.rar': 'application/x-rar-compressed',
        '.7z': 'application/x-7z-compressed',
        '.tar': 'application/x-tar',
        '.gz': 'application/gzip',
        '.bz2': 'application/x-bzip2',
        '.xz': 'application/x-xz',
        '.tgz': 'application/gzip',
        
        # Çizim ve CAD
        '.dwg': 'application/x-dwg',
        '.dxf': 'application/x-dxf',
        '.stl': 'model/stl',
        '.obj': 'model/obj',
        '.blend': 'application/x-blender',
        '.fbx': 'application/octet-stream',
        
        # Font
        '.ttf': 'font/ttf',
        '.otf': 'font/otf',
        '.woff': 'font/woff',
        '.woff2': 'font/woff2',
        '.eot': 'application/vnd.ms-fontobject',
        
        # Veritabanı
        '.db': 'application/x-sqlite3',
        '.sqlite': 'application/x-sqlite3',
        '.mdb': 'application/x-msaccess',
        '.accdb': 'application/x-msaccess',
        '.sql': 'application/sql',
        
        # Diğer
        '.bak': 'application/x-trash',
        '.tmp': 'application/x-trash',
        '.swp': 'application/x-trash',
        '.DS_Store': 'application/x-trash',
        '.class': 'application/java-vm',
        '.pyc': 'application/x-python-code',
        '.pyo': 'application/x-python-code',
    }

    def __init__(self):
        # MIME types için ek uzantıları kaydet
        mimetypes.init()
        self._add_custom_mimetypes()

    def _add_custom_mimetypes(self):
        """Özel MIME type'larını sisteme ekler"""
        for ext, mime_type in self.MIME_TYPES.items():
            mimetypes.add_type(mime_type, ext)

    @staticmethod
    def get_mime_type(file_path: str) -> str:
        """
        Dosyanın MIME type'ını döndürür
        
        Args:
            file_path (str): Dosya yolu
            
        Returns:
            str: MIME type
        """
        try:
            # Önce dosya uzantısına göre MIME type'ı belirle
            mime_type, _ = mimetypes.guess_type(file_path)
            
            if mime_type is None:
                # Uzantıya göre belirlenemezse binary kontrolü yap
                if FileUtils.is_binary_file(file_path):
                    return 'application/octet-stream'
                return 'text/plain'
                
            return mime_type
            
        except Exception as e:
            print(f"MIME type belirlenirken hata oluştu: {str(e)}")
            return "application/octet-stream"

    @staticmethod
    def is_binary_file(file_path: str) -> bool:
        """
        Dosyanın binary olup olmadığını kontrol eder
        
        Args:
            file_path (str): Dosya yolu
            
        Returns:
            bool: Binary ise True, değilse False
        """
        try:
            with open(file_path, 'rb') as f:
                initial_bytes = f.read(8192)
                
                # Binary imza kontrolü
                for signature in FileUtils.BINARY_SIGNATURES:
                    if initial_bytes.startswith(signature):
                        return True
                
                # Null byte kontrolü
                if b'\x00' in initial_bytes:
                    return True
                
                # Metin kontrolü
                text_chars = bytearray({7, 8, 9, 10, 12, 13, 27} | set(range(0x20, 0x100)) - {0x7f})
                non_text = initial_bytes.translate(None, text_chars)
                return bool(non_text)
                
        except Exception as e:
            print(f"Dosya kontrolü sırasında hata oluştu: {str(e)}")
            return True

    @staticmethod
    def get_file_size_mb(file_path: str) -> float:
        """
        Dosya boyutunu MB cinsinden döndürür
        
        Args:
            file_path (str): Dosya yolu
            
        Returns:
            float: Dosya boyutu (MB)
        """
        try:
            return os.path.getsize(file_path) / (1024 * 1024)
        except Exception as e:
            print(f"Dosya boyutu hesaplanırken hata oluştu: {str(e)}")
            return 0.0

    @staticmethod
    def is_text_file(file_path: str) -> bool:
        """
        Dosyanın text dosyası olup olmadığını kontrol eder
        
        Args:
            file_path (str): Dosya yolu
            
        Returns:
            bool: Text dosyası ise True, değilse False
        """
        return not FileUtils.is_binary_file(file_path)

    @staticmethod
    def get_file_extension(file_path: str) -> str:
        """
        Dosya uzantısını döndürür (nokta dahil)
        
        Args:
            file_path (str): Dosya yolu
            
        Returns:
            str: Dosya uzantısı (örn: '.txt')
        """
        try:
            return os.path.splitext(file_path)[1].lower()
        except Exception as e:
            print(f"Dosya uzantısı alınırken hata oluştu: {str(e)}")
            return ""

    @staticmethod
    def get_file_category(file_path: str) -> str:
        """
        Dosyanın kategorisini döndürür
        
        Args:
            file_path (str): Dosya yolu
            
        Returns:
            str: Dosya kategorisi
        """
        mime_type = FileUtils.get_mime_type(file_path)
        
        # Ana MIME type'a göre kategori belirleme
        main_type = mime_type.split('/')[0]
        
        categories = {
            'text': 'Text',
            'image': 'Image',
            'video': 'Video',
            'audio': 'Audio',
            'application': 'Application',
            'font': 'Font',
            'model': '3D Model'
        }
        
        # Özel durumlar için alt kategoriler
        if mime_type in ['text/x-c', 'text/x-c++', 'text/x-java', 'text/x-python']:
            return 'Source Code'
        elif mime_type in ['application/pdf', 'application/msword', 'application/vnd.openxmlformats-officedocument.wordprocessingml.document']:
            return 'Document'
        elif mime_type in ['application/zip', 'application/x-rar-compressed', 'application/x-7z-compressed']:
            return 'Archive'
        elif mime_type in ['application/x-executable', 'application/x-msdownload']:
            return 'Executable'
        
        return categories.get(main_type, 'Other')

    @staticmethod
    def is_code_file(file_path: str) -> bool:
        """
        Dosyanın kaynak kodu dosyası olup olmadığını kontrol eder
        
        Args:
            file_path (str): Dosya yolu
            
        Returns:
            bool: Kaynak kodu dosyası ise True, değilse False
        """
        code_extensions = {
            '.py', '.java', '.cpp', '.c', '.h', '.hpp', '.cs', '.js', '.php',
            '.rb', '.go', '.rs', '.swift', '.kt', '.scala', '.m', '.mm',
            '.pl', '.sh', '.bash', '.ts', '.jsx', '.tsx', '.vue', '.r',
            '.lua', '.sql', '.f90', '.f95', '.f03', '.f08', '.dart'
        }
        return FileUtils.get_file_extension(file_path).lower() in code_extensions

    @staticmethod
    def is_compressed_file(file_path: str) -> bool:
        """
        Dosyanın sıkıştırılmış dosya olup olmadığını kontrol eder
        
        Args:
            file_path (str): Dosya yolu
            
        Returns:
            bool: Sıkıştırılmış dosya ise True, değilse False
        """
        compressed_extensions = {
            '.zip', '.rar', '.7z', '.gz', '.bz2', '.tar', '.xz',
            '.tgz', '.tbz2', '.z', '.lz', '.lzma', '.zst', '.lz4'
        }
        return FileUtils.get_file_extension(file_path).lower() in compressed_extensions

    @staticmethod
    def is_media_file(file_path: str) -> bool:
        """
        Dosyanın medya dosyası (ses, video, resim) olup olmadığını kontrol eder
        
        Args:
            file_path (str): Dosya yolu
            
        Returns:
            bool: Medya dosyası ise True, değilse False
        """
        mime_type = FileUtils.get_mime_type(file_path)
        return mime_type.startswith(('audio/', 'video/', 'image/'))

    @staticmethod
    def get_encoding(file_path: str) -> str:
        """
        Metin dosyasının karakter kodlamasını tespit eder
        
        Args:
            file_path (str): Dosya yolu
            
        Returns:
            str: Tespit edilen kodlama (utf-8, ascii, vb.)
        """
        try:
            with open(file_path, 'rb') as f:
                raw = f.read(4096)
                
            # BOM kontrolü
            if raw.startswith(b'\xef\xbb\xbf'):
                return 'utf-8-sig'
            elif raw.startswith(b'\xff\xfe') or raw.startswith(b'\xfe\xff'):
                return 'utf-16'
            elif raw.startswith(b'\xff\xfe\x00\x00') or raw.startswith(b'\x00\x00\xfe\xff'):
                return 'utf-32'
            
            # UTF-8 kontrolü
            try:
                raw.decode('utf-8')
                return 'utf-8'
            except UnicodeDecodeError:
                pass
            
            # ASCII kontrolü
            try:
                raw.decode('ascii')
                return 'ascii'
            except UnicodeDecodeError:
                pass
            
            # Diğer kodlamalar için varsayılan
            return 'unknown'
            
        except Exception as e:
            print(f"Dosya kodlaması belirlenirken hata oluştu: {str(e)}")
            return 'unknown'

    @staticmethod
    def safe_read_text(file_path: str, chunk_size: int = 8192) -> str:
        """
        Dosyayı güvenli bir şekilde okur ve içeriğini döndürür
        
        Args:
            file_path (str): Dosya yolu
            chunk_size (int): Okunacak parça boyutu
            
        Returns:
            str: Dosya içeriği
        """
        try:
            if FileUtils.is_binary_file(file_path):
                return ""
                
            encoding = FileUtils.get_encoding(file_path)
            if encoding == 'unknown':
                encoding = 'utf-8'
                
            with open(file_path, 'r', encoding=encoding) as f:
                return f.read(chunk_size)
                
        except Exception as e:
            print(f"Dosya okunurken hata oluştu: {str(e)}")
            return ""

    @staticmethod
    def get_file_info(file_path: str) -> dict:
        """
        Dosya hakkında kapsamlı bilgi döndürür
        
        Args:
            file_path (str): Dosya yolu
            
        Returns:
            dict: Dosya bilgileri
        """
        try:
            stat = os.stat(file_path)
            return {
                'name': os.path.basename(file_path),
                'extension': FileUtils.get_file_extension(file_path),
                'path': os.path.abspath(file_path),
                'size': FileUtils.get_file_size_mb(file_path),
                'mime_type': FileUtils.get_mime_type(file_path),
                'category': FileUtils.get_file_category(file_path),
                'is_binary': FileUtils.is_binary_file(file_path),
                'is_text': FileUtils.is_text_file(file_path),
                'is_code': FileUtils.is_code_file(file_path),
                'is_compressed': FileUtils.is_compressed_file(file_path),
                'is_media': FileUtils.is_media_file(file_path),
                'encoding': FileUtils.get_encoding(file_path) if not FileUtils.is_binary_file(file_path) else None,
                'created_time': stat.st_ctime,
                'modified_time': stat.st_mtime,
                'accessed_time': stat.st_atime,
            }
        except Exception as e:
            print(f"Dosya bilgileri alınırken hata oluştu: {str(e)}")
            return {}

    @staticmethod
    def is_system_file(file_path: str) -> bool:
        """
        Dosyanın sistem dosyası olup olmadığını kontrol eder
        
        Args:
            file_path (str): Dosya yolu
            
        Returns:
            bool: Sistem dosyası ise True, değilse False
        """
        system_patterns = {
            '.sys', '.dll', '.exe', '.tmp', '.temp', '.bak',
            'thumbs.db', '.ds_store', '$recycle.bin', 'system volume information'
        }
        name = os.path.basename(file_path).lower()
        ext = FileUtils.get_file_extension(file_path).lower()
        return ext in system_patterns or name in system_patterns 