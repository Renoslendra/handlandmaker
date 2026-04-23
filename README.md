# Hand Gesture to Speech (Bahasa Indonesia)

Proyek ini mendeteksi jumlah jari dari kamera webcam menggunakan MediaPipe, lalu menampilkan teks dan memutar audio Bahasa Indonesia sesuai gesture tangan.

## Fitur

- Deteksi tangan real-time dengan MediaPipe Tasks API.
- Menghitung jumlah jari terbuka (0 sampai 5).
- Menampilkan teks hasil gesture di jendela kamera.
- Memutar audio hasil mapping gesture.
- Auto-generate file audio `.mp3` dengan gTTS jika file belum ada.

## Mapping Gesture

| Jumlah Jari | Teks         | Audio              |
|-------------|--------------|--------------------|
| 0           | Halo         | halo.mp3           |
| 1           | Perkenalkan  | perkenalkan.mp3    |
| 2           | Nama         | nama.mp3           |
| 3           | Saya         | saya.mp3           |
| 4           | Reno         | reno.mp3           |
| 5           | Syaelendra   | syaelendra.mp3     |

## Struktur Proyek

- `main.py` : Aplikasi utama deteksi gesture + audio.
- `test_camera.py` : Tes cepat apakah kamera bisa dibuka dari OpenCV.
- `debug_mp.py` : Script debug instalasi dan struktur package MediaPipe.
- `hand_landmarker.task` : Model MediaPipe Hand Landmarker.
- File `.mp3` : Audio untuk tiap kata pada mapping gesture.

## Prasyarat

- Python 3.9+ (disarankan)
- Webcam aktif
- Koneksi internet saat pertama kali generate audio via gTTS (jika file `.mp3` belum tersedia)

## Instalasi

1. Masuk ke folder proyek.
2. (Opsional) Buat virtual environment.
3. Install dependency.

Contoh (Windows PowerShell):

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install opencv-python mediapipe pygame gTTS
```

Contoh (CMD):

```bat
python -m venv .venv
.\.venv\Scripts\activate.bat
pip install opencv-python mediapipe pygame gTTS
```

## Menjalankan Aplikasi

```bash
python main.py
```

- Jendela kamera akan terbuka.
- Tunjukkan gesture tangan (0-5 jari).
- Tekan `q` untuk keluar.

## Script Tambahan

Tes kamera:

```bash
python test_camera.py
```

Debug MediaPipe:

```bash
python debug_mp.py
```

## Troubleshooting

- Kamera tidak terbuka:
  - Tutup aplikasi lain yang memakai kamera (Zoom, Teams, browser).
  - Jalankan `python test_camera.py` untuk verifikasi kamera.

- Error model tidak ditemukan:
  - Pastikan `hand_landmarker.task` ada di folder proyek yang sama dengan `main.py`.

- Audio tidak keluar:
  - Cek output speaker perangkat.
  - Pastikan dependency `pygame` terpasang.
  - Pastikan file `.mp3` tersedia atau gTTS bisa mengunduh saat pertama kali run.

## Catatan

- Untuk mengubah kata atau audio, edit dictionary `FINGER_MAPPING` di `main.py`.
- Cooldown audio diatur pada konstanta `AUDIO_COOLDOWN` di `main.py`.
