import os #Dosya ve klasör işlemleri yapmak için 
from pydub import AudioSegment # Ses işleme ve dönüştürme işlemleri,FFmpeg yazılımı

# Kodun Fonksiyonları
def process_wav_file(input_file, train_patches_folder, patch_duration_ms=5000, gap_duration_ms=1000, sample_size=None):
    if not os.path.exists(train_patches_folder):
        os.makedirs(train_patches_folder)
        # Çıkış klasörü (patches klasörü) yoksa oluşturur.

    split_audio_to_patches(input_file, train_patches_folder, patch_duration_ms, gap_duration_ms, sample_size)
    # Asıl işleme yapılacak olan fonksiyonu çağırır.

def split_audio_to_patches(audio_file, output_folder, patch_duration_ms=5000, gap_duration_ms=1000, sample_size=None):
    #ses dosyasını yükler
    audio = AudioSegment.from_file(audio_file,format="wav")

    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # giriş dosyasının adını uzantı olmadan çıkarır
    base_name = os.path.splitext(os.path.basename(audio_file))[0]
    
    # ile ses dosyasının toplam süresi (milisaniye) alınır
    total_duration = len(audio)

    # Ses dosyasını parçalara böler
    patches = []
    start = 0
    while start + patch_duration_ms <= total_duration:
        patch = audio[start:start + patch_duration_ms]
        patches.append(patch)
        start += patch_duration_ms + gap_duration_ms  #her bir patch_duration_ms (ör. 5000ms) uzunluğundaki kısmı alınır,bir boşluk (gap_duration_ms) eklenir,Parçalar bir listeye (patches) eklenir

    # sample_size belirtilmişse örneklemeyi uygular
    if sample_size and sample_size < len(patches):
        patches = patches[:sample_size]

    # parçalar kaydedilir
    for i, patch in enumerate(patches):
        patch_file_name = os.path.join(output_folder, f"{base_name}_patch_{i+1}.wav")
        patch.export(patch_file_name, format="wav")
        print(f"Saved patch: {patch_file_name}")


# main kod parçası
if __name__ == "__main__":
    # Kullanıcıdan bir ses dosyasının yolunu isteme
    input_file = input("Enter the path to the WAV file: ").strip().strip('"')

    # Giriş dosyasının adını temel alarak bir klasör adı oluşturma
    base_name = os.path.splitext(os.path.basename(input_file))[0]
    train_patches_folder = f"{base_name}_train_patches"

    # Default değişkenler
    default_patch_duration = 5000  # 5 seconds
    default_gap_duration = 1000    # 1 second
    default_sample_size = 100      # Limit patches to 100 for sampling (None for all)

    #Kullanıcıdan, her bir parçanın uzunluğu, parçalar arasındaki boşluk süresi ve örnekleme için bir sayı isteyeme veya default değer kullanma
    patch_duration_ms = int(input(f"Enter patch duration in milliseconds (default {default_patch_duration}): ") or default_patch_duration)
    gap_duration_ms = int(input(f"Enter gap duration in milliseconds between patches (default {default_gap_duration}): ") or default_gap_duration)
    sample_size = input(f"Enter sample size (number of patches, default {default_sample_size}): ")
    sample_size = int(sample_size) if sample_size else default_sample_size

    # Fonksiyonları çağırıp,bitiş mesajını yazdırma
    process_wav_file(input_file, train_patches_folder, patch_duration_ms, gap_duration_ms, sample_size)
    print("Processing complete!")
