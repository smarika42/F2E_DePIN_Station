/*
  F2E_Station.ino
  Hardware:
    RGB LCD (JHD1313M3)  -> I2C (SDA/SCL)
    Ultrasonic           -> Trig D9 / Echo D10
*/

#include <Wire.h>
#include "rgb_lcd.h"

rgb_lcd lcd;

const uint8_t TRIG_PIN = 9;
const uint8_t ECHO_PIN = 10;
const int     FAR_CM   = 100; // 100cm (1 meter) threshold

bool sessionActive = false;
bool isFocused     = false;
bool personPresent = false;

// To prevent "spamming" the LCD with color commands
enum State { NONE, IDLE, FOCUSED, AWAY };
State currentState = NONE;
State lastState    = NONE;

unsigned long focusSeconds   = 0; 
unsigned long lastSecondTick = 0;
unsigned long lastLCDUpdate  = 0;
unsigned long lastSerialSend = 0;

// Distance Function
long readDistanceCM() {
  digitalWrite(TRIG_PIN, LOW);
  delayMicroseconds(2);
  digitalWrite(TRIG_PIN, HIGH);
  delayMicroseconds(10);
  digitalWrite(TRIG_PIN, LOW);
  
  // 30000ms timeout (~500cm max range). 
  long duration = pulseIn(ECHO_PIN, HIGH, 30000UL); 
  
  // If it times out (error), it returns 0. 
  // We change 0 to 999 so the math naturally sees it as "Too Far/Away".
  if (duration == 0) {
    return 999; 
  }
  return duration / 58L;
}

// COLOR LOGIC 
void updateScreenColor() {
  if (!sessionActive) {
    currentState = IDLE;
  } else if (personPresent && isFocused) {
    currentState = FOCUSED;
  } else {
    currentState = AWAY;
  }

  // ONLY change the LCD color if the state just changed
  if (currentState != lastState) {
    if (currentState == IDLE) {
      lcd.setRGB(0, 0, 255); // BLUE - Stopped/Waiting
    } else if (currentState == FOCUSED) {
      lcd.setRGB(0, 255, 0); // GREEN - Working
    } else if (currentState == AWAY) {
      lcd.setRGB(255, 0, 0); // RED - Slouching or Left the desk
    }
    lastState = currentState; 
  }
}

void lcdRow(uint8_t row, String text) {
  lcd.setCursor(0, row);
  while (text.length() < 16) text += ' ';
  lcd.print(text.substring(0, 16));
}

String formatTime(unsigned long totalSeconds) {
  unsigned long h = totalSeconds / 3600;
  unsigned long m = (totalSeconds % 3600) / 60;
  unsigned long s = totalSeconds % 60;
  char buf[9];
  sprintf(buf, "%02lu:%02lu:%02lu", h, m, s);
  return String(buf);
}

void handleSerial() {
  if (!Serial.available()) return;
  String cmd = Serial.readStringUntil('\n');
  cmd.trim();
  if (cmd.length() == 0) return;

  if (cmd == "READY") {
    lcd.clear();
    lcdRow(0, "F2E Station");
    lcdRow(1, "Press S to start");
    updateScreenColor();
  }
  else if (cmd == "START") {
    sessionActive  = true;
    isFocused      = true; // Assume focused until Python says B
    lastSecondTick = millis();
    lcd.clear();
    updateScreenColor();
  }
  else if (cmd == "STOP") {
    sessionActive = false;
    isFocused     = false;
    lcd.clear();
    lcdRow(0, "Paused. Total:");
    lcdRow(1, formatTime(focusSeconds));
    updateScreenColor();
  }
  else if (cmd == "G") {
    isFocused = true;
    updateScreenColor();
  }
  else if (cmd == "B") {
    isFocused = false;
    updateScreenColor();
  }
}

void setup() {
  Serial.begin(9600);
  pinMode(TRIG_PIN, OUTPUT);
  pinMode(ECHO_PIN, INPUT);
  
  lcd.begin(16, 2);
  updateScreenColor(); // Set initial Blue
  lcdRow(0, "F2E Station");
  lcdRow(1, "Waiting for PC..");
}

void loop() {
  unsigned long now = millis();

  handleSerial();

  // 1. Read Distance 
  long dist = readDistanceCM();
  personPresent = (dist < FAR_CM); 

  updateScreenColor(); // Will only trigger if state changed based on distance

  // 2. Focus Timer 
  if (sessionActive && personPresent && isFocused) {
    if (now - lastSecondTick >= 1000UL) {
      lastSecondTick += 1000UL;
      focusSeconds++;
      if (focusSeconds > 0 && focusSeconds % 60 == 0) {
        Serial.println("GOAL_REACHED");
      }
    }
  } else {
    lastSecondTick = now; // Prevent time jumping when returning
  }

  // 3. Update LCD Text every 1 second
  if (now - lastLCDUpdate >= 1000UL) {
    lastLCDUpdate = now;
    if (sessionActive) {
      String row0 = "Dist:";
      if (dist == 999) row0 += "--- cm";
      else { row0 += dist; row0 += " cm"; }
      while (row0.length() < 11) row0 += ' ';
      
      if      (!personPresent) row0 += " FAR";
      else if (!isFocused)     row0 += " BAD";
      else                     row0 += "  OK";
      
      lcdRow(0, row0);
      lcdRow(1, formatTime(focusSeconds));
    }
  }

  // 4. Send Serial to Python every 1 second
  if (now - lastSerialSend >= 1000UL) {
    lastSerialSend = now;
    Serial.print("DIST:"); Serial.print(dist == 999 ? 0 : dist); 
    Serial.print(" FOCUS:"); Serial.println(formatTime(focusSeconds));
  }
}
