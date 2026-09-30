---
aliases: [Projects, Builds, Portfolio]
tags: [projects, portfolio, dev, hardware, llm, ai]
created: 2026-09-19
updated: 2026-09-30
---

# 🚀 Portfolio Projects & Engineering Builds

Comprehensive documentation of completed builds, software pipelines, and robotics platforms.

---

## 1. Educational Arabic Alphabet Tracing Game

An interactive browser-based educational web app engineered to teach young learners stroke order and phonetics.

### Technical Architecture
- **Rendering Layer:** HTML5 Canvas element configured to track cursor coordinates and touch events seamlessly across both desktop and mobile viewports.
- **Tracing Validation:** Compares user input coordinates against pre-calculated vector boundaries for each Arabic character.
- **Audio Synthesis Engine:** Integrates speech synthesis triggered upon completed letter verification, reinforcing phoneme retention.
- **Stack:** HTML5, CSS3, JavaScript, Python backend utilities.
- **Reference:** [[arabic_tracing_engine_architecture]]

```
[User Input: Touch/Mouse] 
       ↓
[HTML5 Canvas Tracking] → [Boundary Tolerance Algorithm]
       ↓
[Success Validation] → [Phonetic Audio Trigger + Visual Reward]
```

---

## 2. Real-Time Computer Vision & Detection Pipeline

A live multi-stage video inference pipeline engineered for face alignment, identity verification, and object localization.

### Architecture & Data Flow
1. **Frame Capture:** OpenCV pulls raw frames from an active camera feed.
2. **Object Detection:** YOLOv8 detects general scene objects and bounding boxes.
3. **Face Localization:** MTCNN runs cascaded networks to detect faces and extract facial landmarks (eyes, nose, mouth corners).
4. **Feature Embedding:** ArcFace maps aligned crops into normalized feature vectors.
5. **Comparison:** Euclidean / Cosine distance calculates match threshold against database vectors.
6. **Reference:** [[computer_vision_deep_learning_pipelines]]

---

## 3. Arduino Multi-Axis Servomechanism

A physical mechatronics platform built for sensor positioning, pan-tilt tracking, and robotic articulation.

### Hardware Bill of Materials (BOM)
- Arduino Development Board
- 2x SG90 Micro Servos (Pan and Tilt axes)
- 1x HW-504 Dual-Axis Joystick Module
- 1x 28BYJ-48 Geared Stepper Motor with ULN2003 Driver
- Custom 3D Printed Chassis (radar-style mounting base, articulated brackets)
- **Reference:** [[arduino_embedded_systems_reference]]

### Control Logic
- The analog voltages from the HW-504 potentiometers ($0 - 1023$) are mapped dynamically using Arduino's `map()` function to servo angle constraints ($0^\circ - 180^\circ$).
- Stepper motor runs continuous rotational scans or stepped increments based on trigger states.

---

## 4. LEGO SPIKE Prime Robotics Curriculum

Educational robotics modules engineered to teach structured logic, computational thinking, and physics principles.

### Key Instructional Modules
- **Algorithmic Path Planning:** Navigating physical mazes using ultrasonic and color distance sensors.
- **Kinematics & Gear Ratios:** Demonstrating mechanical advantage, torque, and velocity changes through gear assemblies.
- **State Machines:** Programming robots to transition between searching, obstacle avoidance, and task execution states.
- **Reference:** [[lego_spike_prime_robotics_curriculum]]

---

## 5. Kaggle Remote LLM Backend & Reverse Proxy Tunnel

A high-performance, cost-free cloud inference engine powering the [[00 Profile|Hermes Agent]] Telegram bot and Aethelgard Vault knowledge custodian workflows.

### Architectural Stack & Data Flow
- **Hosting Environment:** Kaggle Notebook running dual NVIDIA Tesla T4 GPUs (~29 GB total VRAM).
- **Inference Runtime:** Ollama serving `qwen2.5:14b` on port `11434` with open CORS/Origins (`0.0.0.0:11434`, `OLLAMA_ORIGINS=*`).
- **Tunneling & Ingress:** `pyngrok` establishing a secure public HTTPS reverse proxy tunnel with custom header bypass (`ngrok-skip-browser-warning: true`).
- **Integration Endpoints:** Native Ollama API and OpenAI-compatible `/v1` endpoint consumed by Hermes Agent and PowerShell verification scripts.
- **Reference Guide:** [[kaggle-llm-backend-deployment]]

```
[Telegram User] ◄──► [Hermes Agent @ Local/VPS] ──(HTTPS/REST)──► [Ngrok Tunnel] ──► [Kaggle Dual T4: Ollama Qwen 2.5 14B]
```
