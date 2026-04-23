import mediapipe as mp
import os

print(f"MediaPipe version: {mp.__version__}")
print(f"MediaPipe file: {mp.__file__}")
print("MediaPipe dir attributes:", dir(mp))

try:
    import mediapipe.solutions
    print("mediapipe.solutions found")
except ImportError as e:
    print(f"mediapipe.solutions not found: {e}")

try:
    import mediapipe.python.solutions
    print("mediapipe.python.solutions found")
except ImportError as e:
    print(f"mediapipe.python.solutions not found: {e}")

package_path = os.path.dirname(mp.__file__)
print(f"Contents of {package_path}:")
for item in os.listdir(package_path):
    print(f" - {item}")

if os.path.exists(os.path.join(package_path, 'python')):
    print(f"Contents of {os.path.join(package_path, 'python')}:")
    for item in os.listdir(os.path.join(package_path, 'python')):
        print(f"   - {item}")
