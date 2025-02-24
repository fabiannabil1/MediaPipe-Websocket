# README - Hand Gesture Control for Robot Movement

## Overview
This project utilizes **MediaPipe** for hand detection and **asyncio** with **aiohttp** to send commands to a server based on hand gestures. The system captures hand gestures through a webcam and translates them into movement commands for a robot or another device connected to a server.

This project created to control this project : https://github.com/fabiannabil1/ESP8266-Websocket-Car.git


There are two main Python scripts:
1. **`controlling.py`** - Uses finger count to control movement.
2. **`Gerakan senam.py`** - Uses hand position and spacing for control.

---

## Requirements
Ensure you have the following dependencies installed before running the scripts:

```bash
pip install opencv-python mediapipe aiohttp asyncio
```

---

## `controlling.py` - Finger Count Control
This script detects the number of fingers raised and sends movement commands accordingly.

### Controls:
| Finger Count | Command | Description       |
|-------------|---------|-------------------|
| 1           | `S`     | Stop              |
| 2           | `F`     | Move Forward      |
| 3           | `B`     | Move Backward     |
| 4           | `R`     | Turn Left         |
| 5           | `L`     | Turn Right        |

### How It Works:
- Detects a hand using **MediaPipe**.
- Counts the number of raised fingers.
- Sends an HTTP request with the corresponding command to the server at `http://192.168.4.1/`.
- Displays the video feed with hand landmarks.
- Stops execution when 'q' is pressed.

### Running the Script:
```bash
python controlling.py
```

---

## `Gerakan senam.py` - Hand Position Control
This script controls movement based on hand position and spacing between two hands.

### Controls:
| Condition | Command | Description         |
|-----------|---------|---------------------|
| Hand above a certain height | `F` | Move Forward   |
| Right hand to the right side | `L` | Turn Left     |
| Left hand to the left side | `R` | Turn Right    |
| Both hands far apart | `B` | Move Backward  |
| No hands detected | `S` | Stop            |

### How It Works:
- Detects one or two hands using **MediaPipe**.
- Checks hand position relative to the screen.
- Determines movement direction based on hand placement.
- Sends an HTTP request to `http://192.168.4.1/` with the movement command.
- Displays video feed with quadrant gridlines and hand landmarks.
- Stops execution when 'q' is pressed.

### Running the Script:
```bash
python "Gerakan senam.py"
```

---

## Notes
- Ensure your webcam is connected and accessible before running the scripts.
- The server receiving movement commands should be set up at `192.168.4.1`.
- If using a different IP, modify `BASE_URL` in both scripts accordingly.

---

## Author
This project is developed to experiment with hand gesture-based control systems using computer vision and IoT integration.

---

## License
This project is open-source and free to use for educational purposes.
