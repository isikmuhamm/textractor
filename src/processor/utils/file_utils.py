import os
from typing import Set, Dict
import mimetypes 

class FileUtils:
    # Binary dosya imzaları
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
        """Dosyanın MIME type'ını döndürür"""
        try:
            # Önce dosya uzantısına göre MIME type'ı belirle
            mime_type, _ = mimetypes.guess_type(file_path)

            if mime_type is None:
                # Uzantıya göre belirlenemezse binary kontrolü yap
                if FileUtils.is_binary_file(file_path):
                    return 'application/octet-stream'
                return 'text/plain'

            return mime_type
            
            # Dosya uzantısına göre basit kontrol
            ext = os.path.splitext(file_path)[1].lower()
            return MIME_TYPES.get(ext, 'application/octet-stream')
            
        except Exception as e:
            print(f"MIME type belirlenirken hata oluştu: {str(e)}")
            return "application/octet-stream"

    @staticmethod
    def is_binary_file(file_path: str) -> bool:
        """Dosyanın binary olup olmadığını kontrol eder"""
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
                
                # Text olmayan karakter kontrolü
                try:
                    initial_bytes.decode('utf-8')
                    return False
                except UnicodeDecodeError:
                    return True
                
        except Exception as e:
            print(f"Dosya kontrolü sırasında hata oluştu: {str(e)}")
            return True
        
        return False

    @staticmethod
    def get_file_size_mb(file_path: str) -> float:
        """Dosya boyutunu MB cinsinden döndürür"""
        try:
            return os.path.getsize(file_path) / (1024 * 1024)
        except Exception as e:
            print(f"Dosya boyutu hesaplanırken hata oluştu: {str(e)}")
            return 0.0