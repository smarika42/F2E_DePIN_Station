"""
F2E Focus Monitor — Python side (MediaPipe Tasks API, compatible with 0.10.x+)
================================================================================
Install:
    pip install opencv-python mediapipe pyserial

Run:
    python focus_monitor.py

Controls (click the webcam window first):
    S  ->  Start session
    E  ->  End session
    Q  ->  Quit
"""

import cv2
import mediapipe as mp
from mediapipe.tasks import python as mp_python
from mediapipe.tasks.python import vision as mp_vision
import serial
import serial.tools.list_ports
import time
import sys
import urllib.request
import os

# --- Configuration -----------------------------------------------------------
SERIAL_BAUD       = 9600
CAMERA_INDEX      = 0

SLOUCH_NOSE_Y     = 0.60   # nose Y > this -> slouching (0=top, 1=bottom)
BAD_FRAME_THRESH  = 8      # consecutive bad frames before sending B
GOOD_FRAME_THRESH = 5      # consecutive good frames before sending G
RESEND_INTERVAL   = 2.0    # seconds between re-sends even if state unchanged

MODEL_PATH = "face_landmarker.task"
MODEL_URL  = (
    "https://storage.googleapis.com/mediapipe-models/"
    "face_landmarker/face_landmarker/float16/1/face_landmarker.task"
)

# --- Download model if needed ------------------------------------------------
def ensure_model():
    if not os.path.exists(MODEL_PATH):
        print("[INFO] Downloading face landmarker model (~30 MB), please wait...")
        urllib.request.urlretrieve(MODEL_URL, MODEL_PATH)
        print("[INFO] Model downloaded.")

# --- Auto-detect Arduino COM port --------------------------------------------
def find_arduino_port():
    for p in serial.tools.list_ports.comports():
        desc = (p.description or "").lower()
        hwid = (p.hwid or "").lower()
        if any(x in desc + hwid for x in ["arduino", "ch340", "2341", "usbserial", "usbmodem"]):
            return p.device
    ports = serial.tools.list_ports.comports()
    return ports[0].device if ports else None

# --- Main --------------------------------------------------------------------
def main():
    ensure_model()

    # Serial
    port = find_arduino_port()
    if port is None:
        print("[ERROR] Arduino not found. Plug it in and try again.")
        sys.exit(1)
    print(f"[INFO] Arduino found on {port}")

    try:
        ser = serial.Serial(port, SERIAL_BAUD, timeout=1)
    except serial.SerialException as e:
        print(f"[ERROR] Cannot open {port}: {e}")
        sys.exit(1)

    time.sleep(2)
    ser.reset_input_buffer()
    ser.write(b"READY\n")
    print("[INFO] Sent READY to Arduino.")

    # MediaPipe Face Landmarker (Tasks API - works with 0.10.x)
    base_opts = mp_python.BaseOptions(model_asset_path=MODEL_PATH)
    face_opts = mp_vision.FaceLandmarkerOptions(
        base_options=base_opts,
        num_faces=1,
        min_face_detection_confidence=0.5,
        min_face_presence_confidence=0.5,
        min_tracking_confidence=0.5,
    )
    face_landmarker = mp_vision.FaceLandmarker.create_from_options(face_opts)

    # Webcam
    cap = cv2.VideoCapture(CAMERA_INDEX)
    if not cap.isOpened():
        print(f"[ERROR] Cannot open camera {CAMERA_INDEX}.")
        ser.close()
        sys.exit(1)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH,  640)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

    print("[INFO] Running.  Click the window then press:")
    print("       S = Start session    E = End session    Q = Quit")

    # State
    session_active = False
    current_state  = 'B'
    last_state     = None
    last_send_time = 0.0
    bad_frames     = 0
    good_frames    = 0
    reason         = "Waiting..."

    def send_cmd(cmd):
        ser.write((cmd + "\n").encode())
        print(f"[SERIAL ->] {cmd}")

    while True:
        ret, frame = cap.read()
        if not ret:
            time.sleep(0.05)
            continue

        frame = cv2.flip(frame, 1)
        h, w  = frame.shape[:2]

        rgb      = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb)

        result    = face_landmarker.detect(mp_image)
        frame_bad = False
        reason    = ""

        if not result.face_landmarks:
            frame_bad = True
            reason    = "No face detected"
        else:
            lms       = result.face_landmarks[0]
            nose      = lms[1]
            left_ear  = lms[234]
            right_ear = lms[454]
            left_eye  = lms[33]
            right_eye = lms[263]

            if nose.y > SLOUCH_NOSE_Y:
                frame_bad = True
                reason    = "Slouching"
            elif abs(left_ear.z - right_ear.z) > 0.15:
                frame_bad = True
                reason    = "Looking away / phone"
            elif abs(left_eye.y - right_eye.y) > 0.07:
                frame_bad = True
                reason    = "Head tilted"

        # Hysteresis counters
        if frame_bad:
            bad_frames  += 1
            good_frames  = 0
        else:
            good_frames += 1
            bad_frames   = 0

        if bad_frames  >= BAD_FRAME_THRESH:
            current_state = 'B'
        if good_frames >= GOOD_FRAME_THRESH:
            current_state = 'G'

        # Send to Arduino
        now = time.time()
        if session_active and (current_state != last_state or
                               now - last_send_time >= RESEND_INTERVAL):
            send_cmd(current_state)
            last_state     = current_state
            last_send_time = now

        # Read from Arduino
        if ser.in_waiting:
            line = ser.readline().decode(errors='ignore').strip()
            if line:
                print(f"[SERIAL <-] {line}")
                if line == "GOAL_REACHED":
                    print("[INFO] *** GOAL REACHED - trigger Solana reward here ***")

        # Draw face dots
        if result.face_landmarks:
            for lm in result.face_landmarks[0]:
                cv2.circle(frame, (int(lm.x * w), int(lm.y * h)), 1, (0, 255, 180), -1)

        # Status overlay
        color = (0, 200, 80) if current_state == 'G' else (0, 60, 220)
        label = "FOCUSED" if current_state == 'G' else f"DISTRACTED: {reason}"
        hint  = ("SESSION ACTIVE  [E]=End  [Q]=Quit"
                 if session_active else "[S]=Start Session  [Q]=Quit")

        cv2.rectangle(frame, (0, 0), (w, 55), (20, 20, 20), -1)
        cv2.putText(frame, label, (10, 28), cv2.FONT_HERSHEY_SIMPLEX, 0.75, color, 2)
        cv2.putText(frame, hint,  (10, 48), cv2.FONT_HERSHEY_SIMPLEX, 0.38, (160, 160, 160), 1)

        sy = int(SLOUCH_NOSE_Y * h)
        cv2.line(frame, (0, sy), (w, sy), (80, 80, 255), 1)
        cv2.putText(frame, "slouch line", (5, sy - 5),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.35, (80, 80, 255), 1)

        cv2.imshow("F2E Focus Monitor", frame)

        key = cv2.waitKey(1) & 0xFF
        if key in (ord('s'), ord('S')) and not session_active:
            session_active = True
            last_state     = None
            send_cmd("START")
        elif key in (ord('e'), ord('E')) and session_active:
            session_active = False
            send_cmd("STOP")
        elif key in (ord('q'), ord('Q')):
            break

    if session_active:
        send_cmd("STOP")
    face_landmarker.close()
    cap.release()
    cv2.destroyAllWindows()
    ser.close()
    print("[INFO] Done.")


if __name__ == "__main__":
    main()
