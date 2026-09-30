---
aliases: [CV Pipeline, YOLO, ArcFace, MTCNN]
tags: [technical, ai, computervision, python]
created: 2026-09-19
up: "[[Technical/Skills_and_Stack]]"
related: ["[[Projects/Portfolio_Projects]]"]
---

# 👁️ Computer Vision & Deep Learning Pipelines

A technical architecture reference for real-time video processing, facial recognition, and object localization pipelines.

---

## 1. Multi-Stage Inference Pipeline Architecture

In a composite edge-AI system, raw video frames pass sequentially through detection, alignment, and biometric feature extraction layers:

```
[ Camera Stream / Video Feed ]
              │
              ▼
   [ OpenCV VideoCapture ]
              │
              ├──────────────────────────────────┐
              ▼                                  ▼
     [ YOLOv8 Inference ]               [ MTCNN Face Detector ]
   (General Object Detection)           (Face Detection & Landmarks)
              │                                  │
              ▼                                  ▼
   [ Bounding Box Filter ]              [ 5-Point Affine Warp ]
                                                 │
                                                 ▼
                                       [ ArcFace Embedder ]
                                       (512-D Feature Vector)
                                                 │
                                                 ▼
                                       [ Cosine Similarity ]
                                      (Gallery Identity Match)
```

---

## 2. Facial Biometrics: MTCNN + ArcFace

### MTCNN (Cascaded Network)
MTCNN decomposes face detection into three distinct deep convolutional subnetworks:
1. **P-Net (Proposal Network):** Scans the image at multiple scales (image pyramid) to produce candidate bounding boxes and calibration vectors.
2. **R-Net (Refine Network):** Filters out non-face candidates using a more complex CNN and performs candidate bounding box regression.
3. **O-Net (Output Network):** Identifies final bounding boxes and pinpoints five facial landmark coordinates:
   - Left Eye $(x_1, y_1)$
   - Right Eye $(x_2, y_2)$
   - Nose Tip $(x_3, y_3)$
   - Left Mouth Corner $(x_4, y_4)$
   - Right Mouth Corner $(x_5, y_5)$

### Facial Alignment & Normalization
Detected faces are aligned using a 2D affine transformation to set the inter-pupillary line parallel to the horizontal axis prior to embedding extraction.

### ArcFace (Additive Angular Margin Loss)
ArcFace enforces intra-class compactness and inter-class discrepancy on a hypersphere. The loss function adds an angular margin penalty $m$ directly to the angle $\theta_{y_i}$:

$$L_{\text{ArcFace}} = -\log \frac{e^{s(\cos(\theta_{y_i} + m))}}{e^{s(\cos(\theta_{y_i} + m))} + \sum_{j \neq y_i} e^{s \cos \theta_j}}$$

Where:
- $s$ is the hypersphere radius scale factor.
- $m$ is the angular additive margin.

### Cosine Similarity Thresholding
To compare two 512-dimensional feature vectors $\mathbf{u}$ and $\mathbf{v}$:

$$\text{Similarity}(\mathbf{u}, \mathbf{v}) = \frac{\mathbf{u} \cdot \mathbf{v}}{\|\mathbf{u}\|_2 \|\mathbf{v}\|_2}$$

- **Threshold $\ge 0.65$:** Verified match (Same identity).
- **Threshold $< 0.65$:** Non-match / Impostor.

---

## 3. Minimal Live Inference Loop Template (Python)

```python
import cv2
from ultralytics import YOLO

# Initialize video capture and YOLOv8 model
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

model = YOLO("yolov8n.pt")  # Lightweight nano variant for low latency

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    # Perform inference
    results = model(frame, stream=True, conf=0.45)

    for r in results:
        boxes = r.boxes
        for box in boxes:
            # Bounding box coordinates
            x1, y1, x2, y2 = map(int, box.xyxy[0])
            confidence = float(box.conf[0])
            cls_id = int(box.cls[0])
            label = f"{model.names[cls_id]}: {confidence:.2f}"

            # Visual overlay
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
            cv2.putText(frame, label, (x1, y1 - 10), 
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

    cv2.imshow("CV Pipeline Stream", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
```