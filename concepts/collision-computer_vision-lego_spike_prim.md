TITLE: Edge-Vision Visual Servoing for Modular Kinematics
FILENAME: edge-vision-visual-servoing-spike-kinematics.md
TAGS: [computervision, robotics, visual-servoing, edge-ai, spike-prime, kinematics]
CONTENT:
---
aliases: [Vision-Guided SPIKE Kinematics, IBVS Edge Robotics, CV-Spike Mechatronics]
tags: [computervision, robotics, visual-servoing, edge-ai, spike-prime, kinematics]
created: 2026-09-20
up: "[[01 Technical Skills]]"
related: ["[[computer_vision_deep_learning_pipelines]]", "[[lego_spike_prime_robotics_curriculum]]", "[[detailed_project_documentation]]"]
---

# 👁️🤖 Edge-Vision Visual Servoing for Modular Kinematics (EV-VSMK)

A hybrid mechatronics architecture bridging deep learning multi-stage inference pipelines with closed-loop proportional kinematic controls on modular educational hardware (LEGO SPIKE Prime).

---

## 1. Executive Collision Concept

Standard educational robotics relies on primitive low-dimensional sensors (e.g., 1D reflection phototransistors for line tracking), while modern computer vision pipelines often terminate at passive UI bounding boxes. 

**The Collision:** Replace phototransistor-driven proportional line tracking with **Image-Based Visual Servoing (IBVS)**. By streaming low-latency edge inference detections (YOLOv8 object coordinates or MTCNN biometric gaze vectors) into a real-time MicroPython state machine on the SPIKE Prime hub, we map pixel-domain spatial errors directly to kinematic motor controllers with dynamic gear-ratio torque compensation.

```
       PIXEL DOMAIN (Edge Inference)              PHYSICAL DOMAIN (Kinematics)
 ┌──────────────────────────────────────┐     ┌───────────────────────────────────┐
 │ Frame Error: e_x = (x_target - x_img)│ ──> │ Motor Angular Velocity: ω = K_p·e │
 └──────────────────────────────────────┘     └───────────────────────────────────┘
```

---

## 2. System Architecture

```mermaid
flowchart TD
    subgraph Host_Compute ["Host Edge Engine (Nvidia Jetson / High-Perf Host)"]
        Cam[Wide-Angle USB Stream] --> Cap[OpenCV VideoCapture]
        Cap --> DL_Pipe{Multi-Stage Pipeline}
        DL_Pipe -->|General Object| YOLO[YOLOv8 Edge-TensorRT]
        DL_Pipe -->|Biometric Gaze| MTCNN[MTCNN Landmark Extractor]
        YOLO --> Centroid[Spatial Error Extractor: e_x, e_y, e_area]
        MTCNN --> Centroid
        Centroid --> KinMapper[IBVS Proportional Kinematics Resolver]
    end

    subgraph Telemetry ["Serial / BLE Transport (Pybricks JSON-RPC)"]
        KinMapper -->|Target Vector: [ω_left, ω_right, τ_aux]| Pipe[(Serial /dev/ttyACM0)]
    end

    subgraph SPIKE_Hardware ["LEGO SPIKE Prime Physical Plant"]
        Pipe --> Hub[SPIKE Prime MicroPython Hub]
        Hub --> MotorA[Port A: Drive Motor Left]
        Hub --> MotorB[Port B: Drive Motor Right]
        Hub --> MotorC[Port C: Gear-Reduced Gripper / Pan-Tilt]
        MotorA & MotorB --> DiffDrive[Differential Kinematic Platform]
        MotorC --> Manipulator[Torque-Multiplied End-Effector]
    end
```

---

## 3. Mathematical Formulation: IBVS to Kinematic Gear-Train

### 3.1 Pixel Error Formulation
Let $(x_c, y_c)$ be the centroid of the detected target bounding box $B = [x_{min}, y_{min}, x_{max}, y_{max}]$ in normalized image coordinates $I \in [-1.0, 1.0]$. The center of the camera optical axis is $(0, 0)$.

$$e_x = x_c - 0 = \frac{x_{min} + x_{max}}{2 \cdot W_{frame}} - 0.5$$

$$e_{scale} = A_{target} - \frac{(x_{max} - x_{min})(y_{max} - y_{min})}{W_{frame} \cdot H_{frame}}$$

### 3.2 Proportional Kinematic Controller with Gear Ratio Compensation
Instead of an arbitrary constant, the steering differential $\Delta \omega$ and forward velocity $v$ factor in the physical gear ratio $GR = \frac{N_{\text{driven}}}{N_{\text{driving}}}$:

$$v = K_{p,v} \cdot e_{scale} \cdot \frac{1}{GR_{drive}}$$

$$\Delta \omega = K_{p,\omega} \cdot e_x$$

Left and right angular velocities applied directly to the drive hub:

$$\omega_L = v - \frac{\Delta \omega \cdot L}{2 \cdot r}, \quad \omega_R = v + \frac{\Delta \omega \cdot L}{2 \cdot r}$$

*(where $L$ is track width, and $r$ is the wheel radius).*

If the multi-stage pipeline identifies an authorized user via [[computer_vision_deep_learning_pipelines#ArcFace]], an auxiliary attachment (Port C) actuated with a **Torque Multiplier** ($GR = 3.0$) activates to lift/manipulate a payload:

$$\tau_{output} = \tau_{motor} \cdot GR = 3.0 \cdot \tau_{motor}$$

---

## 4. Implementation Blueprint

### 4.1 Host Edge-Worker (Python + OpenCV + YOLOv8)

```python
# edge_vision_servoing.py
import cv2
import json
import serial
import time
from ultralytics import YOLO

class VisualServoEngine:
    def __init__(self, port="/dev/ttyACM0", baud=115200):
        self.ser = serial.Serial(port, baud, timeout=0.01)
        self.model = YOLO("yolov8n.pt")  # Lightweight export for edge FPS
        self.cap = cv2.VideoCapture(0)
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
        self.kp_steer = 140.0
        self.kp_forward = 90.0
        self.target_area = 0.12  # Optimal target distance coverage (12% of frame)

    def process_stream(self):
        while self.cap.isOpened():
            ret, frame = self.cap.read()
            if not ret:
                break

            h, w, _ = frame.shape
            results = self.model(frame, verbose=False, conf=0.5)[0]
            
            target_cmd = {"v_L": 0, "v_R": 0, "aux_deg": 0}
            
            for box in results.boxes:
                # Class 0: Person (or swap with custom tracking target)
                if int(box.cls[0]) == 0:
                    xyxy = box.xyxy[0].cpu().numpy()
                    
                    # Compute normalized error
                    cx = ((xyxy[0] + xyxy[2]) / 2.0) / w - 0.5
                    area = ((xyxy[2] - xyxy[0]) * (xyxy[3] - xyxy[1])) / (w * h)
                    err_scale = self.target_area - area

                    # Proportional closed-loop mapping
                    delta_omega = self.kp_steer * cx
                    fwd_velocity = self.kp_forward * err_scale

                    target_cmd["v_L"] = int(fwd_velocity + delta_omega)
                    target_cmd["v_R"] = int(fwd_velocity - delta_omega)
                    target_cmd["aux_deg"] = 45 if area > 0.10 else 0
                    break

            # Transmit structured payload to SPIKE Prime
            msg = f"{json.dumps(target_cmd)}\n"
            self.ser.write(msg.encode('utf-8'))
            time.sleep(0.033)  # Maintain ~30Hz control cycle

    def close(self):
        self.cap.release()
        self.ser.close()

if __name__ == "__main__":
    node = VisualServoEngine()
    try:
        node.process_stream()
    except KeyboardInterrupt:
        node.close()
```

### 4.2 SPIKE Prime MicroPython Kinematic Receiver

Run locally on the LEGO SPIKE Prime hub (flashed via Pybricks or native hub OS serial listener):

```python
# spike_kinematics_node.py
import hub
import sys
import json

# Setup hardware ports
# Port A: Left Drive Motor | Port B: Right Drive Motor | Port C: Torque Gripper (GR 3:1)
motor_l = hub.port.A.motor
motor_r = hub.port.B.motor
motor_aux = hub.port.C.motor

# Configure drive motors for speed control
motor_l.mode(hub.port.A.motor.MODE_SPEED)
motor_r.mode(hub.port.B.motor.MODE_SPEED)

def clamp(val, min_val, max_val):
    return max(min_val, min(max_val, val))

while True:
    line = sys.stdin.readline().strip()
    if line:
        try:
            cmd = json.loads(line)
            vl = clamp(cmd.get("v_L", 0), -100, 100)
            vr = clamp(cmd.get("v_R", 0), -100, 100)
            aux = clamp(cmd.get("aux_deg", 0), 0, 90)

            # Motor kinematics execution (Inverted for mirrored chassis mounting)
            motor_l.run_at_speed(-vl)
            motor_r.run_at_speed(vr)
            
            # Position-target actuation for torque-multiplied gear assembly
            motor_aux.run_to_position(aux, speed=40)
        except Exception:
            pass
```

---

## 5. Pedagogical & Technical Evolution Pathways

1. **Latent Space Steering:** Instead of explicit bounding boxes, feed latent vector embeddings from [[computer_vision_deep_learning_pipelines#ArcFace]] to match specific authorized team personnel, enabling autonomous follow-me robotics in educational workshops.
2. **Kinematic Decoupling:** Demonstrate mechanical efficiency tradeoffs by shifting mechanical complexity between software (PID gain tuning) and hardware (compound planetary gear reduction vs. simple spur gearing from [[lego_spike_prime_robotics_curriculum#Mechanical Kinematics & Gear Ratios]]).
3. **Dead-Reckoning Odometry Fusion:** Combine SPIKE Prime internal motor tachometers with visual optical flow to mitigate slip when high-torque gear configurations overcome physical wheel-ground friction.