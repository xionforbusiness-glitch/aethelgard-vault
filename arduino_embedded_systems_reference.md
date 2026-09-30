---
aliases: [Arduino Guide, Embedded Systems, Hardware Schematics]
tags: [hardware, arduino, electronics, robotics]
created: 2026-09-19
up: "[[Technical/Skills_and_Stack]]"
related: ["[[Projects/Portfolio_Projects]]"]
---

# ⚡ Arduino & Embedded Systems Reference

Detailed hardware specifications, pin configurations, stepping sequences, and driver code for microcontrollers and actuators.

---

## 1. Actuator & Sensor Pinouts

### HW-504 Dual-Axis Joystick
The joystick module contains two $10\text{ k}\Omega$ potentiometers placed orthogonally and a momentary tactile push button.

```
       HW-504 Module Pinout
   ┌──────────────────────────┐
   │  [VCC]  ──>  +5V Rail    │
   │  [GND]  ──>  Ground      │
   │  [VRx]  ──>  Analog A0   │
   │  [VRy]  ──>  Analog A1   │
   │  [SW]   ──>  Digital D2  │ (Enable INPUT_PULLUP)
   └──────────────────────────┘
```

### SG90 Micro Servo Specifications
- **Operating Voltage:** $4.8\text{V} - 6.0\text{V}$
- **PWM Modulation:** $50\text{ Hz}$ ($T = 20\text{ ms}$ total period)
  - $1.0\text{ ms}$ pulse width $\approx 0^\circ$
  - $1.5\text{ ms}$ pulse width $\approx 90^\circ$ (Neutral center)
  - $2.0\text{ ms}$ pulse width $\approx 180^\circ$
- **Pin Assignment:**
  - **Brown:** GND
  - **Red:** $+5\text{V}$ (Dedicated external source recommended)
  - **Orange:** PWM Signal pin (e.g., Pin 9 or 10)

---

## 2. 28BYJ-48 Stepper & ULN2003 Driver

The 28BYJ-48 is a 5-wire unipolar permanent magnet stepper motor with an internal gear reduction of approximately $64:1$.

### Stepping Sequence (Half-Step Mode for Smooth Rotation)

| Step Index | IN1 (Coil A) | IN2 (Coil B) | IN3 (Coil C) | IN4 (Coil D) |
| :---: | :---: | :---: | :---: | :---: |
| **1** | HIGH | LOW | LOW | LOW |
| **2** | HIGH | HIGH | LOW | LOW |
| **3** | LOW | HIGH | LOW | LOW |
| **4** | LOW | HIGH | HIGH | LOW |
| **5** | LOW | LOW | HIGH | LOW |
| **6** | LOW | LOW | HIGH | HIGH |
| **7** | LOW | LOW | LOW | HIGH |
| **8** | HIGH | LOW | LOW | HIGH |

---

## 3. Joystick Pan-Tilt Control Sketch

```cpp
#include <Servo.h>

// Servo instances
Servo panServo;
Servo tiltServo;

// Pin assignments
const int PIN_JOY_X = A0;
const int PIN_JOY_Y = A1;
const int PIN_PAN_SERVO = 9;
const int PIN_TILT_SERVO = 10;

// Internal variables
int joyXVal = 0;
int joyYVal = 0;
int panAngle = 90;
int tiltAngle = 90;

void setup() {
  panServo.attach(PIN_PAN_SERVO);
  tiltServo.attach(PIN_TILT_SERVO);
  
  // Center servos on initialization
  panServo.write(panAngle);
  tiltServo.write(tiltAngle);
}

void loop() {
  // Read analog voltages (0 - 1023)
  joyXVal = analogRead(PIN_JOY_X);
  joyYVal = analogRead(PIN_JOY_Y);

  // Deadzone filter around center position (~512)
  if (abs(joyXVal - 512) > 50) {
    // Proportional increment/decrement
    int deltaPan = map(joyXVal, 0, 1023, -3, 3);
    panAngle = constrain(panAngle + deltaPan, 0, 180);
    panServo.write(panAngle);
  }

  if (abs(joyYVal - 512) > 50) {
    int deltaTilt = map(joyYVal, 0, 1023, -3, 3);
    tiltAngle = constrain(tiltAngle + deltaTilt, 15, 165); // Avoid mechanical binding
    tiltServo.write(tiltAngle);
  }

  delay(20); // Maintain stability and servo update rates
}
```

---

## 4. Mathematical Mapping Reference
The standard Arduino `map()` function follows linear interpolation:

$$\text{Output} = (x - \text{in\_min}) \times \frac{\text{out\_max} - \text{out\_min}}{\text{in\_max} - \text{in\_min}} + \text{out\_min}$$