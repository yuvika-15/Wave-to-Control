# Gesture-Controlled System Utility

A real-time hand gesture recognition system that allows users to control system volume, screen brightness, and capture screenshots using simple hand gestures through a webcam.

Built using Python, OpenCV, MediaPipe, and system-level control libraries for a touchless desktop interaction experience.

---

## Features

- Real-time hand tracking using MediaPipe
- Gesture-based system volume control
- Gesture-based screen brightness control
- Hands-free screenshot capture
- Smooth control using gesture interpolation
- Real-time visual feedback
- Lightweight and CPU-friendly implementation

---

## Technologies Used

### Language

- Python

### Libraries

- OpenCV
- MediaPipe
- NumPy
- Pycaw
- Screen Brightness Control
- Pillow
- Comtypes

### Concepts

- Computer Vision
- Hand Tracking
- Human-Computer Interaction
- Real-Time Video Processing
- Gesture Recognition

---

## Installation

Clone the repository:

```bash
git clone https://github.com/YOUR_USERNAME/Gesture-Controlled-System-Utility.git

cd Gesture-Controlled-System-Utility
```

Create a virtual environment:

```bash
python -m venv venv
```

Activate it:

### Windows

```bash
venv\Scripts\activate
```

### Linux / macOS

```bash
source venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

---

## Run the Application

```bash
python gesture_control.py
```

Press:

```text
q
```

to exit the application.

---

## Gesture Controls

### Main Menu

Hold the gesture for approximately 0.8 seconds to switch modes.

| Gesture | Mode |
|----------|----------|
| ☝️ 1 Finger | Volume Control |
| ✌️ 2 Fingers | Brightness Control |
| 🤟 3 Fingers | Screenshot Mode |
| 🖐️ 5 Fingers | Return to Main Menu |

---

### Volume Control Mode

- Select using **1 Finger**
- Adjust distance between:
  - Thumb Tip
  - Index Finger Tip

| Distance | Action |
|----------|----------|
| Fingers Close | Lower Volume |
| Fingers Apart | Increase Volume |

---

### Brightness Control Mode

- Select using **2 Fingers**
- Adjust distance between:
  - Thumb Tip
  - Index Finger Tip

| Distance | Action |
|----------|----------|
| Fingers Close | Lower Brightness |
| Fingers Apart | Increase Brightness |

---

### Screenshot Mode

- Select using **3 Fingers**
- Make a closed fist

| Gesture | Action |
|----------|----------|
| ✊ Fist | Capture Screenshot |

Screenshots are automatically saved with timestamped filenames:

```text
screenshot_123456789.png
```

---

## How It Works

1. Webcam captures live video frames.
2. MediaPipe detects hand landmarks.
3. Finger positions are analyzed.
4. Gesture is classified based on finger states.
5. Selected mode is activated.
6. Thumb-index distance controls volume or brightness.
7. Closed fist triggers screenshot capture.

---

## Project Structure

```text
Gesture-Controlled-System-Utility/
│
├── gesture_control.py
├── requirements.txt
├── README.md
└── screenshots/
```

---

## Performance

- Real-time webcam processing
- Multi-mode gesture control
- Smooth volume and brightness transitions
- Automatic gesture debouncing
- Supports tracking up to 2 hands

---

## Future Improvements

- Application launcher using gestures
- Media playback controls
- Mouse cursor control
- Custom gesture training
- Voice + Gesture hybrid control
- Cross-platform support

---

## Author

Yuvika Agrawal and Tanvi Sharma

---

## License

This project is intended for educational and demonstration purposes.
