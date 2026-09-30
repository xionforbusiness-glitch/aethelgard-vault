---
aliases: [Tech Stack, Skills, Cheatsheets]
tags: [technical, programming, systems, hardware, llm, ai]
created: 2026-09-19
updated: 2026-09-30
---

# 🛠️ Technical Skills & Knowledge Base

This note serves as the reference guide for your daily toolset, programming languages, operational environments, and engineering practices.

---

## 1. Programming & Software Development

### Python
- **Use Cases:** Automation scripts, data manipulation, computer vision pipelines, backend logic, daemon process orchestration.
- **Key Libraries:** `OpenCV` (`cv2`), `NumPy`, `Ultralytics` (YOLO), `Flask`, `Requests`, `pyngrok`.
- **Strengths:** Rapid prototyping, handling image tensors, scriptable automation, REST API integrations.

### Web Stack: JavaScript, HTML5, CSS3, PHP & Node.js
- **Frontend:** Canvas manipulation (`getContext('2d')`), dynamic DOM updates, responsive layouts, touch/mouse event normalization.
- **Backend & Scripting:** Node.js script execution, PHP server scripting for dynamic forms and data persistence.

---

## 2. Systems, Networking & Security

### Linux Environment & Shell Scripting
- **Command Line Mastery:** Process monitoring (`top`, `htop`, `ps`, `pkill`), user permissions (`chmod`, `chown`), text manipulation (`grep`, `awk`, `sed`, `find`).
- **Administration & Daemons:** SSH key management, systemd service setup, package management (`apt`), headless process backgrounding (`subprocess.Popen`).
- **Playbook:** [[linux_cli_bash_automation_reference]]

### Networking, Proxies & Packet Analysis
- **Wireshark:**
  - Filtering packet captures (`http`, `dns`, `tcp.flags.reset == 1`).
  - Analyzing handshakes, round-trip time (RTT), latency spikes, and payload anomalies.
  - Playbook: [[networking_wireshark_playbook]]
- **OpenVPN & Tunnels:**
  - Configuration of client `.ovpn` profiles, routing gateway traffic, TLS authentication certificates, and secure tunnel maintenance ([[openvpn_network_tunneling_architecture]]).
- **Ngrok Reverse Proxy Tunneling:**
  - Exposing local / cloud compute ports (e.g. Ollama `11434`) securely over HTTPS with custom bypass headers (`ngrok-skip-browser-warning: true`).

---

## 3. Computer Vision, Machine Learning & LLM Infrastructure

### Cloud LLM Inference & Agent Backends
- **[[kaggle-llm-backend-deployment|Kaggle Dual Tesla T4 Ollama Backend]]:** Serving `qwen2.5:14b` with ~29 GB total VRAM over Ngrok HTTPS tunnels. Provides zero-cost, high-throughput OpenAI-compatible endpoints (`/v1`) for [[00 Profile|Hermes Agent]] and Telegram automation.
- **System 1 Decision Engines:** [[laya-system-1-decision-engine|Laya]] (ModernBERT-large, mmBERT-base) for sub-35ms non-autoregressive decision routing and guardrails.

### Object Detection & Processing
- **YOLOv8 (Ultralytics):** Real-time object classification and bounding box localization. Optimization for inference speed on live video frames.
- **OpenCV:** Image pre-processing (grayscale conversion, blurring, thresholding, Canny edge detection, perspective transformation).
- **Playbook:** [[computer_vision_deep_learning_pipelines]]

### Biometric & Facial Analysis
- **MTCNN (Multi-task Cascaded Convolutional Networks):** Three-stage detection (P-Net, R-Net, O-Net) for robust facial boundary localization and 5-point facial landmark alignment.
- **ArcFace (Additive Angular Margin Loss):** Extracting high-dimensional facial feature embeddings to compute cosine similarity against target identity galleries.

---

## 4. Hardware, Microcontrollers & Prototyping

| Component | Functionality | Interface / Pinout Notes |
| :--- | :--- | :--- |
| **Arduino (Uno/Nano)** | Microcontroller logic hub | Digital I/O, PWM pins for motor signals, ADC for analog inputs ([[arduino_embedded_systems_reference]]) |
| **SG90 Micro Servos** | Position control ($0^\circ - 180^\circ$) | PWM signal ($50\text{ Hz}$), $5\text{V}$, Ground |
| **HW-504 Joystick** | Dual-axis analog coordinate input | X-Axis (A0), Y-Axis (A1), Pushbutton (Digital Pin) |
| **28BYJ-48 Stepper + ULN2003** | High-precision rotational positioning | 4-phase sequence driven via Darlington transistor array |
| **LEGO SPIKE Prime** | Educational modular robotics | Motor controllers, ultrasonic distance sensors, color sensors ([[lego_spike_prime_robotics_curriculum]]) |
| **3D CAD Modeling** | Mechanical bracket design | Parametric modeling of motor mounts, radar pans, and enclosures |
