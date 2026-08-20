# HandyDrive

Control browser racing games (e.g. Turbo Moto Racer) using hand gestures in front of your webcam — no keyboard touch needed. The script watches your hand via your webcam and simulates real arrow-key presses (`up`, `down`, `left`, `right`) based on what your hand is doing.

## Tech Stack

- Python
- OpenCV (`opencv-python`) — webcam capture & frame processing
- MediaPipe (Tasks API — `HandLandmarker`) — hand detection & landmark tracking
- `pydirectinput` — simulates real keyboard key holds (regular `pyautogui` key events didn't register reliably in-game)

## Controls

| Gesture | Action | Key |
|---|---|---|
| Any hand open (fingers straight) | Accelerate | `up` (held) |
| Fist | Brake / Reverse | `down` (held) |
| No hand visible | Brake / Reverse (default) | `down` (held) |
| **Right hand**, 1 finger extended (index) | Turn right | `right` (held) |
| **Right hand**, 2 fingers extended (index + middle) | Turn left | `left` (held) |
| Left hand, or any other finger count | No turn | — |

**Notes:**
- Only the **right hand** controls turning. Accelerate/brake works with **either hand**.
- Turn detection only counts 4 fingers (index, middle, ring, pinky) — thumb is excluded since detecting its up/down state is unreliable.
- Because the camera feed is mirrored (`cv2.flip`), MediaPipe's handedness label is reversed — in the code, a detected `"Left"` label actually corresponds to your real right hand.

## Setup

1. Install Python.
2. Create and activate a virtual environment in the project folder:
   ```
   python -m venv venv
   venv\Scripts\activate
   ```
3. Install dependencies:
   ```
   pip install opencv-python mediapipe pydirectinput
   ```
4. Make sure `hand_landmarker.task` (MediaPipe's hand landmark model file) is present in the same folder as `main.py`.

## Running

1. Activate the venv, then run:
   ```
   python main.py
   ```
2. A small camera preview window opens in the top-left corner — **don't click on it**.
3. Click on the game/browser window so it stays focused.
4. Start gesturing in front of your webcam.
5. Press `q` (with the camera window focused) to quit.

If key presses aren't reaching the game, try running the terminal **as Administrator**.

## Files

- `main.py` — main control script
- `hand_landmarker.task` — MediaPipe hand landmark model (required, must sit next to `main.py`)
