from processor.file_processor import FileProcessor
import logging

logger = logging.getLogger(__name__)

def main():
    """
    Ana program fonksiyonu
    """
    print("Dosya İçerik Birleştirici")
    print("-" * 30)
    
    try:
        # Kullanıcıdan girdi al
        path = input("Dosya veya klasör yolu giriniz: ").strip()
        
        if not path:
            print("Yol belirtilmedi!")
            return
            
        # Maksimum dosya boyutunu iste (opsiyonel)
        max_size = input("Maksimum dosya boyutu (MB) [varsayılan: 5.0]: ").strip()
        max_size = float(max_size) if max_size else 5.0
        
        # Çıktı dosyası adını iste (opsiyonel)
        output_file = input("Çıktı dosyası adı [varsayılan: content.txt]: ").strip()
        output_file = output_file if output_file else "content.txt"
        
        # İşlemciyi başlat ve çalıştır
        processor = FileProcessor(max_file_size_mb=max_size, output_file=output_file)
        processor.process(path)

    except KeyboardInterrupt:
        print("\nProgram kullanıcı tarafından sonlandırıldı.")
    except ValueError as e:
        print(f"Geçersiz değer: {str(e)}")
    except Exception as e:
        print(f"Beklenmeyen bir hata oluştu: {str(e)}")

if __name__ == "__main__":
    main()