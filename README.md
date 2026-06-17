# Wave to Control: Real-Time Hand Gesture Recognition System

![Python](https://img.shields.io/badge/Python-3.9+-blue)
![TensorFlow](https://img.shields.io/badge/TensorFlow-DeepLearning-orange)
![OpenCV](https://img.shields.io/badge/OpenCV-ComputerVision-green)
![MediaPipe](https://img.shields.io/badge/MediaPipe-HandTracking-purple)
![IEEE](https://img.shields.io/badge/Research-IEEE%20Conference-red)

A real-time hand gesture recognition system that enables touchless control of desktop applications using Computer Vision and Deep Learning.

---

## Overview

Wave to Control is a real-time hand gesture recognition system that allows users to interact with desktop applications through intuitive hand gestures captured by a standard webcam. The system leverages MediaPipe for hand landmark detection, TensorFlow for gesture classification, and OpenCV for real-time video processing.

The project was developed as part of an academic research initiative and formed the basis of a research paper accepted for presentation at the **IEEE-sponsored IGNITE 2026 International Conference on Innovation & Growth in Next-Gen Intelligent Technology & Engineering**.

---

## Demo

Add screenshots or GIFs here:

```text
screenshots/demo.gif
screenshots/interface.png
```

Or include a demo video link:

```text
https://your-demo-video-link
```

---

## Features

* Real-time hand gesture detection and recognition
* Touchless control of desktop applications
* Gesture classification accuracy of **97.5%**
* Real-time performance of **25–30 FPS**
* MediaPipe-based hand landmark extraction
* TensorFlow-powered gesture classification
* OpenCV integration for video processing and visualization
* Lightweight deployment using a standard webcam

---

## Tech Stack

### Programming Language

* Python

### Libraries & Frameworks

* TensorFlow
* MediaPipe
* OpenCV
* NumPy

### Core Concepts

* Computer Vision
* Deep Learning
* Human-Computer Interaction (HCI)
* Gesture Recognition
* Real-Time Video Processing

---

## System Workflow

1. Capture live video feed from a webcam.
2. Detect hand landmarks using MediaPipe.
3. Extract landmark coordinates as feature vectors.
4. Preprocess and normalize gesture data.
5. Classify gestures using a TensorFlow-based model.
6. Map recognized gestures to predefined application commands.
7. Execute actions in real time.

---

## Installation

### Clone the Repository

```bash
git clone https://github.com/YOUR_USERNAME/Wave-to-Control.git
cd Wave-to-Control
```

### Create a Virtual Environment (Recommended)

```bash
python -m venv venv
```

Activate the environment:

**Windows**

```bash
venv\Scripts\activate
```

**Linux / macOS**

```bash
source venv/bin/activate
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

Or install manually:

```bash
pip install tensorflow opencv-python mediapipe numpy
```

---

## Running the Application

Launch the application:

```bash
python main.py
```

Before running, ensure:

* A webcam is connected and accessible.
* Adequate lighting is available.
* Your hand remains visible within the camera frame.

---

## Gesture Controls

| Gesture     | Action                           |
| ----------- | -------------------------------- |
| Open Palm   | Activate Tracking                |
| Swipe Left  | Previous Slide / Previous Action |
| Swipe Right | Next Slide / Next Action         |
| Thumbs Up   | Confirm / Select                 |
| Fist        | Pause / Stop Tracking            |

> Update this table according to the exact gestures implemented in your project.

---

## Performance

| Metric                       | Result                  |
| ---------------------------- | ----------------------- |
| Gesture Recognition Accuracy | **97.5%**               |
| Processing Speed             | **25–30 FPS**           |
| Input Device                 | Standard Webcam         |
| Detection Method             | MediaPipe Hand Tracking |

---

## Applications

* Presentation Control
* Touchless User Interfaces
* Smart Workstations
* Accessibility Solutions
* Human-Computer Interaction Research
* Gesture-Based Automation Systems

---

## Research Contribution

This project served as the foundation for a research paper accepted for presentation at:

**IGNITE 2026 – 1st International Conference on Innovation & Growth in Next-Gen Intelligent Technology & Engineering**

**Technical Sponsor:** IEEE

The paper presents the design, implementation, and evaluation of a real-time hand gesture recognition system for touchless desktop application control.

---

## Project Structure

```text
Wave-to-Control/
│
├── dataset/
│   └── gesture_images/
│
├── models/
│   └── trained_model.h5
│
├── src/
│   ├── hand_tracking.py
│   ├── gesture_classifier.py
│   ├── application_control.py
│   └── main.py
│
├── screenshots/
│
├── requirements.txt
├── README.md
└── LICENSE
```

---

## Troubleshooting

### Webcam Not Detected

* Ensure no other application is currently using the webcam.
* Verify camera permissions are enabled.

### Poor Gesture Recognition

* Improve lighting conditions.
* Keep the hand fully visible.
* Maintain a consistent distance from the camera.

### Low FPS

* Close unnecessary background applications.
* Reduce camera resolution if supported.
* Use GPU acceleration when available.

---

## Future Enhancements

* Dynamic gesture sequence recognition
* Multi-hand gesture support
* Custom gesture training interface
* Voice and gesture hybrid interaction
* Cross-platform desktop integration
* Edge-device deployment optimization

---

## Authors

**Yuvika Agrawal**
Computer Science Student | AI & Machine Learning Enthusiast

**Tanvi Sharma**

---

## License

This project is intended for educational, research, and demonstration purposes only.
