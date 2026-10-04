---
aliases: [LEGO Robotics, SPIKE Prime, STEM Curriculum, Robotics Pedagogy]
tags: [robotics, education, stem, python, hardware]
created: 2026-09-19
up: "[[02 Projects]]"
---

# 🤖 LEGO SPIKE Prime Curriculum & Robotics Engineering

Instructional modules, mechanical kinematics, and algorithmic sensor loops engineered for educational robotics courses.

---

## 1. Mechanical Kinematics & Gear Ratios

Understanding the trade-off between angular velocity ($\omega$) and output torque ($\tau$):

$$\text{Gear Ratio (GR)} = \frac{N_{\text{driven}}}{N_{\text{driving}}}$$

- **Speed Multiplier ($GR < 1$):** Large gear drives small gear. Increases rotational speed at the cost of torque.
- **Torque Multiplier ($GR > 1$):** Small gear drives large gear. Increases output push force, essential for climbing ramps or heavy lifting attachments.

---

## 2. Sensor Integration: Proportional Line Tracking

A binary (bang-bang) line tracker causes continuous oscillation and mechanical jitter. A **Proportional (P) Controller** calculates smooth steering adjustments based on error magnitude:

```
[ Light Sensor Reading ] ────> [ Compute Error = Reading - Target ]
                                                │
                                                ▼
                                [ Steering = Error * Kp ]
                                                │
                                                ▼
                                [ Drive Left / Right Motors ]
```

### MicroPython Implementation for SPIKE Prime

```python
from spike import PrimeHub, ColorSensor, MotorPair
from spike.control import wait_for_seconds

hub = PrimeHub()
sensor = ColorSensor('A')
motors = MotorPair('B', 'C')

# Target light reflection value (edge between black line and white surface)
TARGET_REFLECTION = 50  
KP = 1.2  # Proportional gain constant

while True:
    current_reflection = sensor.get_reflected_light()
    error = current_reflection - TARGET_REFLECTION
    
    # Steering value is proportional to error
    steering = int(error * KP)
    
    # Limit steering bounds between -100 and 100
    steering = max(-100, min(100, steering))
    
    motors.start(steering=steering, speed=30)
```

---

## 3. Finite State Machine (FSM) Autonomous Logic

For maze navigation and obstacle management, robots transition through distinct operational states:

```
      ┌──────────────┐   Obstacle < 15cm    ┌──────────────┐
      │ STATE_SEARCH │ ───────────────────> │ STATE_AVOID  │
      └──────────────┘                      └──────────────┘
             ▲                                     │
             │           Turn Complete             │
             └─────────────────────────────────────┘
```

1. **`STATE_SEARCH`:** Robot moves forward following line or dead reckoning while monitoring ultrasonic sensors.
2. **`STATE_AVOID`:** When distance $< 15\text{ cm}$, motors brake, reverse $5\text{ cm}$, rotate $90^\circ$, and transition back to search.