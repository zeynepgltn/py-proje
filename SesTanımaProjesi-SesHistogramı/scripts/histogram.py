import librosa  # Ses işleme kütüphanesi
import numpy as np  # Sayısal işlemler kütüphanesi
import matplotlib.pyplot as plt  # Grafiklerin çizimi için
import librosa.display  # Librosa'ya özel görselleştirme fonksiyonları için
from pydub import AudioSegment
import io  # Bellekte veri akışı için

# Kullanıcıdan bir ses dosyasının yolunu isteme
input_file = input("Enter the path to the WAV file: ").strip().strip('"')

# Ses dosyasını pydub ile yükleme
audio = AudioSegment.from_file(input_file, format="wav")

# AudioSegment nesnesini NumPy dizisine dönüştürme
samples = np.array(audio.get_array_of_samples(), dtype=np.float32)

# Kanal sayısını kontrol et (stereo ise bir kanala indir)
if audio.channels > 1:
    samples = samples.reshape((-1, audio.channels))
    samples = samples.mean(axis=1)  # Stereo'yu mono'ya çevir

# Ornekleme hızını al
ornekleme_hizi = audio.frame_rate

# NumPy dizisini normalize et (-1 ile 1 arasında)
data = samples / np.max(np.abs(samples))

# Ses dalgasını görselleştirme
plt.figure(figsize=(10, 6))
plt.subplot(2, 1, 1)
plt.plot(data)
plt.title('Ses Dalgası')
plt.xlabel('Zaman (örnek)')
plt.ylabel('Genlik')

# Spektrogram görselleştirme
plt.subplot(2, 1, 2)
D = librosa.amplitude_to_db(np.abs(librosa.stft(data)), ref=np.max)
librosa.display.specshow(D, sr=ornekleme_hizi, x_axis='time', y_axis='log')
plt.colorbar(format='%+2.0f dB')
plt.title('Spektrogram')
plt.xlabel('Zaman (saniye)')
plt.ylabel('Frekans (Hz)')

# Grafiklerin gösterilmesi
plt.tight_layout()
plt.show()
