import cv2
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
import pygame
import time
import os
from gtts import gTTS

# ==========================================
# KONFIGURASI DAN KONSTANTA
# ==========================================
AUDIO_COOLDOWN = 1.5
TEXT_POSITION = (50, 100)
TEXT_COLOR = (0, 255, 0)  # Hijau
TEXT_SCALE = 2
TEXT_THICKNESS = 3
MODEL_PATH = "hand_landmarker.task"

FINGER_MAPPING = {
    0: {"text": "Halo", "audio": "halo.mp3"},
    1: {"text": "Perkenalkan", "audio": "perkenalkan.mp3"},
    2: {"text": "Nama", "audio": "nama.mp3"},
    3: {"text": "Saya", "audio": "saya.mp3"},
    4: {"text": "Reno", "audio": "reno.mp3"},
    5: {"text": "Syaelendra", "audio": "syaelendra.mp3"}
}

class AudioManager:
    """Mengelola pembuatan dan pemutaran file audio."""
    def __init__(self):
        pygame.mixer.init()
        self._prepare_audio_files()

    def _prepare_audio_files(self):
        print("Memeriksa file audio...")
        for data in FINGER_MAPPING.values():
            self._create_audio_if_not_exists(data["audio"], data["text"])
        print("File audio siap!")

    def _create_audio_if_not_exists(self, filename, text):
        if not os.path.exists(filename):
            print(f"Membuat {filename}...")
            tts = gTTS(text=text, lang='id')
            tts.save(filename)

    def play(self, audio_file):
        """Memutar file audio jika musik tidak sedang sibuk."""
        if not pygame.mixer.music.get_busy():
            pygame.mixer.music.load(audio_file)
            pygame.mixer.music.play()

class HandTracker:
    """Mengelola deteksi tangan menggunakan MediaPipe Tasks API."""
    def __init__(self):
        base_options = python.BaseOptions(model_asset_path=MODEL_PATH)
        options = vision.HandLandmarkerOptions(
            base_options=base_options,
            num_hands=1,
            min_hand_detection_confidence=0.5,
            min_hand_presence_confidence=0.5,
            min_tracking_confidence=0.5
        )
        self.detector = vision.HandLandmarker.create_from_options(options)

    def process_frame(self, frame):
        """Memproses frame dan mengembalikan hasil deteksi."""
        mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=frame)
        return self.detector.detect(mp_image)

    def draw_landmarks(self, frame, hand_landmarks):
        """Menggambar landmark tangan secara manual (pengganti drawing_utils)."""
        height, width, _ = frame.shape
        for landmark in hand_landmarks:
            x = int(landmark.x * width)
            y = int(landmark.y * height)
            cv2.circle(frame, (x, y), 5, (0, 255, 0), -1)

    def get_fingers_count(self, hand_landmarks):
        """Menghitung jumlah jari yang terbuka."""
        # Indeks untuk ujung jari (tip) dan sendi bawah (pip/mcp)
        finger_tips = [8, 12, 16, 20]
        finger_pips = [6, 10, 14, 18]
        thumb_tip, thumb_ip = 4, 3
        
        fingers = []
        # Jempol (posisi horizontal relatif terhadap sendi)
        fingers.append(1 if hand_landmarks[thumb_tip].x < hand_landmarks[thumb_ip].x else 0)
        
        # 4 Jari lainnya (posisi vertikal relatif terhadap sendi)
        for i in range(4):
            fingers.append(1 if hand_landmarks[finger_tips[i]].y < hand_landmarks[finger_pips[i]].y else 0)
            
        return sum(fingers)

def main():
    # Inisialisasi Komponen
    audio_manager = AudioManager()
    tracker = HandTracker()
    cap = cv2.VideoCapture(0)
    
    last_audio_time = 0
    print("Kamera aktif. Tekan 'q' untuk berhenti.")

    while cap.isOpened():
        success, frame = cap.read()
        if not success: continue

        frame = cv2.flip(frame, 1)
        results = tracker.process_frame(frame)
        current_text = ""

        if results.hand_landmarks:
            for hand_landmarks in results.hand_landmarks:
                tracker.draw_landmarks(frame, hand_landmarks)
                count = tracker.get_fingers_count(hand_landmarks)
                
                if count in FINGER_MAPPING:
                    data = FINGER_MAPPING[count]
                    current_text = data["text"]
                    
                    if time.time() - float(last_audio_time) > AUDIO_COOLDOWN:
                        audio_manager.play(data["audio"])
                        last_audio_time = time.time()

                cv2.putText(frame, current_text, TEXT_POSITION, cv2.FONT_HERSHEY_SIMPLEX, 
                            TEXT_SCALE, TEXT_COLOR, TEXT_THICKNESS, cv2.LINE_AA)

        cv2.imshow('Hand Recognition - Clean Code', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Cleanup
    cap.release()
    cv2.destroyAllWindows()
    pygame.mixer.quit()

if __name__ == "__main__":
    main()