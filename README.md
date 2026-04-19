# Snitch_It
Leverages Computer Vision (via a laptop) to monitor productivity and uses Arduino hardware to act as a physical command center that tracks progress and enforces focus.

Project Visual: https://youtu.be/9O2SoQGajC4

Description:
This project is a "Focus-to-Earn" (F2E) DePIN Station, a hardware-software hybrid designed to monitor your productivity, enforce good posture, and reward you for deep work.

Here is the quick breakdown of how it operates:

The Brain (Laptop/Python): Uses your webcam and AI (MediaPipe) to track your posture in real-time. If you slouch, tilt your head, or look away at your phone, it flags you as "distracted."

The Body (Arduino/Hardware): Acts as your physical command center. An Ultrasonic sensor constantly checks if you are actually sitting at your desk. The RGB LCD screen provides instant visual feedback on your status: Blue (Idle/Waiting), Green (Working & Focused), or Red (Slouching or Walked Away).

The Reward (Web3/Solana): Once you successfully complete your timed work session without leaving the desk or breaking posture, the system acts as a DePIN (Decentralized Physical Infrastructure) node. It triggers a blockchain transaction on the Solana network to reward you with digital assets for your verified focus.


Hardware Mapping & Pinouts:

Using the Grove Shield v2.0, the wiring follows a modular, standardized approach. 

Component         Port Type       Pin(s) Used            Function 

JHD1313M3 LCD     I2C             I2C Header (SDA/SCL)   Displays "Focus Status," "Goal Time," and "Earnings." 

Ultrasonic Sensor Digital         D7                     Measures proximity to detect if you are physically present at the desk. 
