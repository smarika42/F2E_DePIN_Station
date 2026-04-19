# Snitch_It

**A Focus-to-Earn DePIN Station** – A hardware-software hybrid that monitors your productivity, enforces good posture, and rewards you with Solana for deep work sessions.

[![Demo Video](https://img.shields.io/badge/Demo-YouTube-red?logo=youtube)](https://youtu.be/9O2SoQGajC4)
[![License](https://img.shields.io/badge/license-MIT-blue)](LICENSE)
[![Python](https://img.shields.io/badge/python-3.8+-blue?logo=python)](https://python.org)
[![Arduino](https://img.shields.io/badge/Arduino-Compatible-blue?logo=arduino)](https://www.arduino.cc/)

## 📋 Table of Contents

- [Overview](#overview)
- [How It Works](#how-it-works)
- [Features](#features)
- [Hardware Requirements](#hardware-requirements)
- [Software Requirements](#software-requirements)
- [Hardware Setup](#hardware-setup)
- [Installation](#installation)
- [Quick Start](#quick-start)
- [Configuration](#configuration)
- [Troubleshooting](#troubleshooting)
- [Project Structure](#project-structure)
- [Contributing](#contributing)
- [License](#license)


## Overview

Snitch_It is an innovative productivity enforcement system that combines:

- **Computer Vision** (Python + MediaPipe) for real-time posture tracking
- **IoT Hardware** (Arduino + Grove Shield) for physical presence detection
- **Web3/Solana Integration** (DePIN) for token-based rewards

The system monitors whether you're actually working while sitting at your desk with proper posture. When you complete a focused work session successfully, you earn Solana tokens – literally getting paid for staying focused!

**[Watch the Demo →](https://youtu.be/9O2SoQGajC4)**


## ⚙️ How It Works

┌─────────────────────────────────────────────────────────────┐
│                    Snitch_It System Flow                    │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  🧠 THE BRAIN (Laptop/Python)                              │
│  ├─ Captures webcam feed in real-time                       │
│  ├─ Uses MediaPipe for skeleton/posture tracking            │
│  ├─ Detects: slouching, head tilt, phone distraction        │
│  └─ Sends status to Arduino via Serial                      │
│                                                              │
│  💪 THE BODY (Arduino/Hardware)                             │
│  ├─ Ultrasonic sensor checks desk proximity                 │
│  ├─ RGB LCD displays focus status & earnings                │
│  ├─ Buzzer alerts on posture violations                     │
│  └─ Syncs focus state with Python brain                     │
│                                                              │
│  💰 THE REWARD (Web3/Solana)                                │
│  ├─ Session completed successfully?                         │
│  ├─ Mint Solana tokens to your wallet                       │
│  └─ Track earnings in real-time                             │
│                                                              │
└─────────────────────────────────────────────────────────────┘

### System Components

**The Brain (Laptop/Python)**
- Uses your webcam and AI (MediaPipe) to track posture in real-time
- Monitors for slouching, head tilt, and phone distractions
- Flags "distracted" moments and communicates with Arduino hardware
- Handles all Web3/Solana transaction logic

**The Body (Arduino/Hardware)**
- Acts as your physical command center and human feedback interface
- Ultrasonic sensor constantly monitors if you're actually sitting at your desk
- RGB LCD screen provides instant visual feedback (focus status, session timer, earnings)
- Buzzer alerts for posture violations to keep you accountable

**The Reward (Web3/Solana)**
- DePIN (Decentralized Physical Infrastructure) model
- Complete a successful focused work session → earn Solana tokens
- Smart contract validates completion and mints rewards
- Track your earnings in real-time on the LCD display


## Features

- ✅ **Real-time Posture Tracking** – Computer vision monitors slouching, head tilt, and distractions
- ✅ **Physical Presence Detection** – Ultrasonic sensor verifies you're actually at your desk
- ✅ **Live Feedback** – RGB LCD display shows focus status, timer, and earnings
- ✅ **Audio Alerts** – Buzzer notifies you of posture violations
- ✅ **Solana Integration** – Earn crypto tokens for completed focus sessions
- ✅ **Hardware Modular Design** – Grove Shield standardization makes assembly simple
- ✅ **Configurable Thresholds** – Adjust sensitivity and session durations to your needs
- ✅ **Session Analytics** – Track focus metrics and earnings over time


## 🛠️ Hardware Requirements

| Component | Quantity | Notes |
|-----------|----------|-------|
| Arduino Board (MKR WiFi 1010 or compatible) | 1 | Must support Grove Shield v2.0 |
| Grove Shield v2.0 | 1 | Modular pinout management |
| JHD1313M1 LCD Display (16x2 RGB) | 1 | I2C connection for status display |
| Grove Ultrasonic Sensor | 1 | Distance detection (desk proximity) |
| Grove Buzzer | 1 | Audio feedback for alerts |
| Laptop/PC with Webcam | 1 | Python 3.8+ for vision processing |
| USB Cable (USB-A to Arduino) | 1 | Serial communication |
| USB Cable (USB-A to USB-C for laptop) | 1 | Power and data transfer |

## Software Requirements

### Python (Laptop)
- Python 3.8 or higher
- OpenCV
- MediaPipe
- PySerial (for Arduino communication)
- Solana Python SDK
- Requests library

### Arduino
- Arduino IDE 1.8.19+ or Arduino CLI
- Grove LCD library
- Grove Sensor libraries

## Hardware Setup

### Wiring Diagram

Using the Grove Shield v2.0, connections follow this standard pinout:

| Component | Port Type | Pin(s) | Function |
|-----------|-----------|--------|----------|
| JHD1313M1 LCD | I2C | I2C Header (SDA/SCL) | Displays focus status, timer, earnings |
| Ultrasonic Sensor | Digital | D7 | Detects physical presence at desk |
| Buzzer | Digital | D8 | Provides audio feedback on violations |
| Status LED (Optional) | Digital | D6 | Visual indicator of focus state |

### Assembly Steps

1. **Insert Grove Shield v2.0** onto your Arduino board
2. **Connect I2C LCD** to the I2C port on the shield
3. **Connect Ultrasonic Sensor** to Digital port D7
4. **Connect Buzzer** to Digital port D8
5. **Connect Arduino to laptop** via USB cable
6. **Position ultrasonic sensor** ~1-2 feet away from your desk chair

## Installation

### Clone the Repository

```bash
git clone https://github.com/smarika42/Snitch_It.git
cd Snitch_It
```

### Python Setup

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### Arduino Setup

1. Open Arduino IDE
2. Install required libraries via Library Manager:
   - `Grove LCD RGB Backlight`
   - `Grove Sensor`
3. Upload the Arduino sketch:
   - Open `arduino/snitch_it/snitch_it.ino`
   - Select your board and COM port
   - Click Upload

### Solana Configuration

1. Create a Solana wallet (or use existing)
2. Set up your Solana environment variables:

```bash
export SOLANA_PRIVATE_KEY="your_private_key_here"
export SOLANA_CLUSTER="devnet"  # or mainnet-beta
```
##  Quick Start

### 1. Start the Arduino
- Upload the sketch to your Arduino board
- Open Serial Monitor to verify connection (9600 baud)

### 2. Run the Python Application

```bash
python main.py
```

### 3. Configure Your Session

When the app starts, you'll be prompted to set:
- Work session duration (e.g., 25 minutes for Pomodoro)
- Posture sensitivity (1-10 scale)
- Reward amount per session (in Lamports)

### 4. Start Focusing!

1. Position yourself at your desk
2. The ultrasonic sensor will confirm you're seated
3. Your posture will be monitored via webcam
4. Complete the session without slouching or leaving → **Earn Solana!**

## ⚙️ Configuration

### Python Configuration File (`config.json`)

```json
{
  "session": {
    "duration_minutes": 25,
    "break_minutes": 5,
    "break_after_sessions": 4
  },
  "posture": {
    "slouch_sensitivity": 7,
    "head_tilt_threshold": 15,
    "phone_detection_enabled": true
  },
  "hardware": {
    "com_port": "/dev/ttyACM0",
    "baud_rate": 9600,
    "ultrasonic_distance_threshold": 100
  },
  "solana": {
    "cluster": "devnet",
    "reward_amount_lamports": 100000,
    "rpc_endpoint": "https://api.devnet.solana.com"
  }
}
```

### Adjusting Sensitivity

Edit the thresholds in `config.json`:
- **Posture Sensitivity (1-10)**: Higher = stricter posture enforcement
- **Head Tilt Threshold (degrees)**: Angle at which system flags a violation
- **Ultrasonic Distance (cm)**: Distance at which you're considered "seated"

---

## 🐛 Troubleshooting

### Issue: Arduino Not Detected

```bash
# Check available COM ports
python -c "import serial; print(serial.tools.list_ports.comports())"

# Update config.json with correct port
```

### Issue: Webcam Feed Not Showing

- Ensure camera permissions are granted to Python
- Try: `python -c "import cv2; print(cv2.VideoCapture(0).isOpened())"`
- If False, check camera is not in use by another app

### Issue: LCD Display Not Updating

- Verify I2C connection: `i2cdetect -y 1` (on Raspberry Pi or Linux)
- Check Grove LCD library is installed in Arduino IDE
- Try re-uploading Arduino sketch

### Issue: Solana Transactions Failing

- Verify private key is correct in environment variables
- Check account has sufficient SOL for gas fees
- Ensure you're on correct cluster (devnet vs mainnet-beta)
- Check network connectivity: `ping api.devnet.solana.com`

### Issue: False Posture Violations

- Lower `slouch_sensitivity` in config.json
- Adjust `head_tilt_threshold` to higher value
- Ensure adequate lighting for webcam
- Position camera at eye level

---

## 📁 Project Structure

```
Snitch_It/
├── README.md
├── requirements.txt
├── config.json
├── main.py                 # Main Python application entry point
├── arduino/
│   └── snitch_it/
│       └── snitch_it.ino   # Arduino sketch
├── src/
│   ├── vision/
│   │   ├── posture_tracker.py
│   │   └── mediapipe_utils.py
│   ├── hardware/
│   │   ├── arduino_controller.py
│   │   └── sensors.py
│   ├── blockchain/
│   │   └── solana_integration.py
│   └── utils/
│       └── logger.py
└── tests/
    ├── test_posture.py
    └── test_arduino.py
```

## Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/amazing-feature`
3. Commit changes: `git commit -m 'Add amazing feature'`
4. Push to branch: `git push origin feature/amazing-feature`
5. Open a Pull Request

### Development Setup

```bash
pip install -r requirements-dev.txt
pytest tests/
```

## License

This project is licensed under the MIT License – see the [LICENSE](LICENSE) file for details.

## 📞 Support & Feedback

- 🎬 [Watch the Demo](https://youtu.be/9O2SoQGajC4)
- 🐛 [Report Issues](https://github.com/smarika42/Snitch_It/issues)
- 💬 [Discussions](https://github.com/smarika42/Snitch_It/discussions)

**Made with 💪 and focus by [@smarika42](https://github.com/smarika42)**
