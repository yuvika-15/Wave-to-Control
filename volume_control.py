import os
import time
import urllib.request
from enum import Enum

import cv2
import numpy as np
import comtypes
import screen_brightness_control as sbc
from mediapipe import Image, ImageFormat
from mediapipe.tasks import python as mp_python
from mediapipe.tasks.python import vision as mp_vision
from pycaw.pycaw import AudioUtilities

# Hand landmark connections (21 points)
HAND_CONNECTIONS = [
    (0, 1), (1, 2), (2, 3), (3, 4),
    (0, 5), (5, 6), (6, 7), (7, 8),
    (5, 9), (9, 10), (10, 11), (11, 12),
    (9, 13), (13, 14), (14, 15), (15, 16),
    (13, 17), (17, 18), (18, 19), (19, 20),
    (0, 17), (5, 9), (9, 13), (13, 17),
]

MODEL_URL = (
    "https://storage.googleapis.com/mediapipe-models/hand_landmarker/"
    "hand_landmarker/float16/1/hand_landmarker.task"
)
MODEL_PATH = os.path.join(os.path.dirname(__file__), "hand_landmarker.task")

class AppMode(Enum):
    MAIN_MENU = 0
    VOLUME_MODE = 1
    BRIGHTNESS_MODE = 2
    SCREENSHOT_MODE = 3

def ensure_model() -> None:
    """Download the model file if it is not present locally."""
    if os.path.exists(MODEL_PATH):
        return
    print("Downloading MediaPipe hand_landmarker.task ...")
    urllib.request.urlretrieve(MODEL_URL, MODEL_PATH)

def create_hand_landmarker() -> mp_vision.HandLandmarker:
    ensure_model()
    base_opts = mp_python.BaseOptions(model_asset_path=MODEL_PATH)
    options = mp_vision.HandLandmarkerOptions(
        base_options=base_opts,
        num_hands=2,
        min_hand_detection_confidence=0.6,
        min_hand_presence_confidence=0.5,
        min_tracking_confidence=0.6,
        running_mode=mp_vision.RunningMode.VIDEO,
    )
    return mp_vision.HandLandmarker.create_from_options(options)

def get_volume_interface():
    comtypes.CoInitialize()
    device = AudioUtilities.GetSpeakers()
    return device.EndpointVolume

def open_preferred_camera() -> cv2.VideoCapture:
    """Use the laptop webcam (index 0)."""
    cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    if cap.isOpened():
        print("Using camera index 0")
    return cap

def draw_connections(frame, landmarks, width: int, height: int) -> None:
    """Render the landmark connection segments onto the frame."""
    for a_idx, b_idx in HAND_CONNECTIONS:
        a = landmarks[a_idx]
        b = landmarks[b_idx]
        cv2.line(
            frame,
            (int(a.x * width), int(a.y * height)),
            (int(b.x * width), int(b.y * height)),
            (0, 255, 0),
            2,
        )

def count_extended_fingers(lm) -> int:
    """Returns the number of extended fingers (0-5)."""
    count = 0
    wrist = 0
    
    # Non-thumb fingers
    tips = [8, 12, 16, 20]
    pips = [6, 10, 14, 18]
    for tip, pip in zip(tips, pips):
        dtip = (lm[tip].x - lm[wrist].x)**2 + (lm[tip].y - lm[wrist].y)**2
        dpip = (lm[pip].x - lm[wrist].x)**2 + (lm[pip].y - lm[wrist].y)**2
        if dtip > dpip:
            count += 1
            
    # Thumb (Using x-coordinate depending on which way the hand is facing)
    # If the index base is to the left of the pinky base, the thumb should extend to the left.
    is_left_side = lm[5].x < lm[17].x
    if is_left_side:
        if lm[4].x < lm[3].x:
            count += 1
    else:
        if lm[4].x > lm[3].x:
            count += 1
            
    return count

def is_fist_closed(lm) -> bool:
    return count_extended_fingers(lm) == 0

class GestureApp:
    def __init__(self):
        self.landmarker = create_hand_landmarker()
        self.cap = open_preferred_camera()
        self.mode = AppMode.MAIN_MENU
        
        # Audio
        self.volume = get_volume_interface()
        if self.volume is not None:
            self.vol_min, self.vol_max, _ = self.volume.GetVolumeRange()
            self.smooth_vol = self.volume.GetMasterVolumeLevel()
        else:
            self.vol_min = self.vol_max = self.smooth_vol = 0
            
        # Brightness
        try:
            self.smooth_brightness = sbc.get_brightness(display=0)[0]
        except Exception:
            self.smooth_brightness = 50
            
        self.dist_min, self.dist_max = 25, 220
        
        # Debounce tracking
        self.held_finger_count = -1
        self.held_finger_time = 0
        self.debounce_duration = 0.8  # Wait 0.8 seconds to confirm mode switch
        
        # Screenshot Tracking
        self.last_screenshot_time = 0
        self.screenshot_msg_until = 0

    def run(self):
        if not self.cap.isOpened():
            print("Error: Cannot access camera.")
            return

        start_time = time.perf_counter()
        
        try:
            while True:
                ok, frame = self.cap.read()
                if not ok:
                    print("Warning: Frame grab failed.")
                    break
                
                frame = cv2.flip(frame, 1)
                height, width, _ = frame.shape
                
                rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                mp_image = Image(image_format=ImageFormat.SRGB, data=rgb)
                timestamp_ms = int((time.perf_counter() - start_time) * 1000)
                result = self.landmarker.detect_for_video(mp_image, timestamp_ms)
                
                if result.hand_landmarks:
                    lm = result.hand_landmarks[0] # Act on the primary hand
                    self.process_hand(lm, width, height, frame)
                    draw_connections(frame, lm, width, height)
                else:
                    # Reset debounce timer if hand is lost
                    self.held_finger_count = -1
                    self.held_finger_time = 0
                    
                self.draw_ui(frame, width, height)
                
                cv2.imshow("Volume Control", frame)
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
        finally:
            self.cleanup()

    def process_hand(self, lm, width, height, frame):
        fingers = count_extended_fingers(lm)
        now = time.perf_counter()
        
        # Manage debouncing for mode transitions
        if fingers in [1, 2, 3, 5]:
            if fingers == self.held_finger_count:
                if now - self.held_finger_time > self.debounce_duration:
                    # Trigger state change
                    if fingers == 5 and self.mode != AppMode.MAIN_MENU:
                        self.mode = AppMode.MAIN_MENU
                    elif self.mode == AppMode.MAIN_MENU:
                        if fingers == 1:
                            self.mode = AppMode.VOLUME_MODE
                        elif fingers == 2:
                            self.mode = AppMode.BRIGHTNESS_MODE
                        elif fingers == 3:
                            self.mode = AppMode.SCREENSHOT_MODE
                    
                    # Refresh debounce state after change
                    self.held_finger_time = now
            else:
                self.held_finger_count = fingers
                self.held_finger_time = now
        else:
            self.held_finger_count = -1
            self.held_finger_time = now

        # Execute current mode specific logic
        if self.mode == AppMode.VOLUME_MODE:
            self.handle_volume(lm, width, height, frame)
        elif self.mode == AppMode.BRIGHTNESS_MODE:
            self.handle_brightness(lm, width, height, frame)
        elif self.mode == AppMode.SCREENSHOT_MODE:
            self.handle_screenshot(lm, now, frame)

    def handle_volume(self, lm, width, height, frame):
        p1 = np.array([lm[4].x * width, lm[4].y * height])
        p2 = np.array([lm[8].x * width, lm[8].y * height])
        
        dist = np.linalg.norm(p1 - p2)
        dist = np.clip(dist, self.dist_min, self.dist_max)
        
        if self.volume is not None:
            target_vol = np.interp(dist, [self.dist_min, self.dist_max], [self.vol_min, self.vol_max])
            self.smooth_vol = 0.8 * self.smooth_vol + 0.2 * target_vol
            self.volume.SetMasterVolumeLevel(float(self.smooth_vol), None)
            
        cv2.circle(frame, tuple(p1.astype(int)), 8, (255, 0, 255), -1)
        cv2.circle(frame, tuple(p2.astype(int)), 8, (255, 0, 255), -1)
        cv2.line(frame, tuple(p1.astype(int)), tuple(p2.astype(int)), (255, 0, 255), 3)

    def handle_brightness(self, lm, width, height, frame):
        p1 = np.array([lm[4].x * width, lm[4].y * height])
        p2 = np.array([lm[8].x * width, lm[8].y * height])
        
        dist = np.linalg.norm(p1 - p2)
        dist = np.clip(dist, self.dist_min, self.dist_max)
        
        target_bright = np.interp(dist, [self.dist_min, self.dist_max], [0, 100])
        self.smooth_brightness = 0.8 * self.smooth_brightness + 0.2 * target_bright
        try:
            sbc.set_brightness(int(self.smooth_brightness), display=0)
        except Exception:
            pass
            
        cv2.circle(frame, tuple(p1.astype(int)), 8, (255, 0, 255), -1)
        cv2.circle(frame, tuple(p2.astype(int)), 8, (255, 0, 255), -1)
        cv2.line(frame, tuple(p1.astype(int)), tuple(p2.astype(int)), (255, 0, 255), 3)

    def handle_screenshot(self, lm, now, frame):
        if is_fist_closed(lm):
            if now - self.last_screenshot_time > 3.0:
                filename = f"screenshot_{int(time.time())}.png"
                try:
                    from PIL import ImageGrab
                    ImageGrab.grab().save(filename)
                    print(f"Screenshot saved as {filename}")
                except ImportError:
                    cv2.imwrite(filename, frame)
                    print(f"Webcam screenshot saved as {filename}")
                self.last_screenshot_time = now
                self.screenshot_msg_until = now + 1.5

    def draw_ui(self, frame, width, height):
        # Header - Active Mode
        mode_text = self.mode.name.replace("_", " ")
        cv2.putText(frame, f"Mode: {mode_text}", (20, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2)
        
        if self.mode == AppMode.MAIN_MENU:
            instructions = [
                "Select Mode Options:",
                "1 Finger: Volume",
                "2 Fingers: Brightness",
                "3 Fingers: Screenshot",
                "5 Fingers: Return to Main Menu"
            ]
            y = 100
            for row in instructions:
                cv2.putText(frame, row, (20, y), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 0), 2)
                y += 35
                
        elif self.mode == AppMode.VOLUME_MODE:
            pct_vol = np.interp(self.smooth_vol, [self.vol_min, self.vol_max], [0, 100]) if self.volume is not None else 0
            bar_y = int(np.interp(pct_vol, [0, 100], [400, 150]))
            cv2.rectangle(frame, (30, 150), (60, 400), (0, 255, 0), 2)
            cv2.rectangle(frame, (30, bar_y), (60, 400), (0, 255, 0), -1)
            cv2.putText(frame, f"Vol:{pct_vol:3.0f}%", (15, 430), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 0), 2)
            
        elif self.mode == AppMode.BRIGHTNESS_MODE:
            pct_bright = np.interp(self.smooth_brightness, [0, 100], [0, 100])
            bar_y = int(np.interp(pct_bright, [0, 100], [400, 150]))
            cv2.rectangle(frame, (30, 150), (60, 400), (0, 255, 255), 2)
            cv2.rectangle(frame, (30, bar_y), (60, 400), (0, 255, 255), -1)
            cv2.putText(frame, f"Bri:{pct_bright:3.0f}%", (15, 430), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 0), 2)
            
        elif self.mode == AppMode.SCREENSHOT_MODE:
            cv2.putText(frame, "Make a fist to capture", (30, 100), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 0), 2)
            
        # Optional: Debounce visualizer, indicates progress of holding a selection
        if self.held_finger_count in [1, 2, 3, 5] and self.held_finger_time > 0:
            elapsed = time.perf_counter() - self.held_finger_time
            if 0.1 < elapsed < self.debounce_duration:
                prog = min(1.0, elapsed / self.debounce_duration)
                cv2.circle(frame, (width - 50, 50), 30, (50, 50, 50), 2)
                cv2.circle(frame, (width - 50, 50), int(30 * prog), (0, 255, 0), -1)

        # Draw Screenshot Confirmation overlay on top
        if time.perf_counter() < self.screenshot_msg_until:
            cv2.putText(frame, "Screenshot Taken!", (width // 2 - 200, height // 2),
                        cv2.FONT_HERSHEY_SIMPLEX, 1.3, (0, 0, 0), 4)

    def cleanup(self):
        self.landmarker.close()
        self.cap.release()
        cv2.destroyAllWindows()

def main():
    app = GestureApp()
    app.run()

if __name__ == "__main__":
    main()