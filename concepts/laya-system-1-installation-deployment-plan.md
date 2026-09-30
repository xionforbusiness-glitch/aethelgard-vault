---
title: Laya System 1 Decision Engine — Installation & Deployment Plan
created: 2026-09-21
updated: 2026-09-21
type: concept
tags: [ai, ml, python, open-source, hermes-agent]
sources: [raw/articles/2026-09-21-laya-system1-decision-model-open-source.md]
confidence: high
contested: false
contradictions: []
---

# Laya System 1 Decision Engine — Installation & Deployment Plan

## 1. Executive Summary & Objective
This implementation plan establishes the environment, dependencies, verification scripts, and architectural integration points for deploying **Laya**—the open-source (Apache 2.0) non-autoregressive **System 1 Decision Engine**—on local infrastructure.

### Why Deploy Laya?
1. **Sub-35ms Local Decision Speed:** Replaces slow (500–2500ms) generative LLM calls for structured classifications, guardrails, and intent routing.
2. **Zero Marginal Inference Cost:** Runs locally on CPU or NVIDIA GPU with modest memory requirements (~1.5 GB VRAM).
3. **Multilingual Ingestion:** Handles 100+ languages natively with the `mmBERT-base` (322M) checkpoint.
4. **Deterministic Schema Safety:** Directly outputs calibrated categorical probabilities and scores without verbal hallucinations or JSON parsing errors.

---

## 2. Hardware & Environment Specifications

### Minimum Requirements:
- **OS:** Windows 11 / Linux (Ubuntu 22.04+)
- **Python:** Python 3.10 – 3.12 (Virtual Environment recommended via `uv` or `venv`)
- **RAM:** Minimum 8 GB system RAM
- **GPU (Optional but Recommended):** NVIDIA GPU with CUDA 12+ (e.g., RTX 3060/4060 or Tesla T4). Runs in CPU mode via `onnxruntime` if no GPU is available.
- **Disk Storage:** ~3.5 GB free space (for caching PyTorch dependencies and all 3 model checkpoints: ~808 MB English, ~647 MB Multilingual, ~808 MB Typed-Decisions).

---

## 3. Step-by-Step Installation Guide

### Step 3.1: Create an Isolated Python Environment
Using `uv` (recommended for speed and PEP 668 compliance) or `python -m venv`:

```bash
# Using uv:
uv venv .venv-laya --python 3.11
source .venv-laya/Scripts/activate   # Windows (Git Bash)
# or: .venv-laya\Scripts\activate   # Windows (cmd/PowerShell)

# Alternatively, standard venv:
python -m venv .venv-laya
source .venv-laya/Scripts/activate
```

### Step 3.2: Install PyTorch & Laya Package
```bash
# Install PyTorch with CUDA 12.x support (or CPU build if no GPU):
pip install torch --index-url https://download.pytorch.org/whl/cu121

# Install Laya Core SDK and Hugging Face dependencies:
pip install "laya>=0.3.3" transformers huggingface_hub onnxruntime
```

### Step 3.3 (Optional): Node.js / TypeScript Setup
For JavaScript/TypeScript microservices or desktop wrappers:
```bash
npm install @receptron/laya onnxruntime-node
```

---

## 4. Checkpoint Selection & Download Strategy

| Checkpoint Identifier | Backbone | Weights Size | Primary Use Case |
| :--- | :--- | :--- | :--- |
| `convaiinnovations/laya` | ModernBERT-large (421M) | ~808 MB | English text triage, prompt guardrails, moderation |
| `convaiinnovations/laya-multilingual` | mmBERT-base (322M) | ~647 MB | 100+ languages, Arabic/multilingual routing, fast CPU inference |
| `convaiinnovations/laya-typed-decisions` | ModernBERT-large (421M) | ~808 MB | Structured 4-workflow tasks (0.766 accuracy) |

*(Note: The Laya SDK automatically downloads checkpoints from Hugging Face on first call and caches them in `~/.cache/huggingface/hub/`)*.

---

## 5. Verification & Testing Scripts

### Test Script 1: Single Checkpoint Direct Inference (`verify_laya_basic.py`)
```python
import laya

def test_basic_inference():
    print("Loading Laya English Base Model...")
    agent = laya.load("convaiinnovations/laya")
    
    state = {
        "source": "vault_ingest",
        "title": "Camera Calibration with OpenCV",
        "snippet": "We implement intrinsic camera matrix computation using checkerboard patterns and cv2.calibrateCamera()."
    }
    
    questions = {
        "domain": {
            "type": "choice",
            "instructions": "What technical domain does this note belong to?",
            "criteria": {
                "computer_vision": "OpenCV, image processing, object detection, camera calibration",
                "embedded_systems": "Arduino, microcontrollers, robotics, sensors",
                "networking": "Wireshark, VPN, packet capture, DNS",
                "general_notes": "everything else"
            }
        },
        "urgency_score": {
            "type": "score",
            "instructions": "Rate priority for indexing",
            "criteria": ["low", "normal", "high", "critical"]
        },
        "requires_hardware": {
            "type": "noul",
            "instructions": "Does this topic require physical hardware testing?"
        }
    }
    
    result = agent.predict(state, questions)
    answers = result["answers"]
    
    print("\n--- Inference Results ---")
    print(f"Domain Selected : {answers['domain']['choice']} (Confidence: {answers['domain']['confidence']:.2f})")
    print(f"Urgency Score   : {answers['urgency_score']['score']:.2f} / 3.0")
    print(f"Needs Hardware  : {answers['requires_hardware']['noul']:.1%}")

if __name__ == "__main__":
    test_basic_inference()
```

### Test Script 2: Intelligent Multilingual Router (`verify_laya_router.py`)
```python
import laya
from laya import Router

def test_router_multilingual():
    print("Initializing Laya Multilingual Router (Preloaded)...")
    router = Router(preload=True)
    
    # Arabic / Multilingual State Example
    arabic_state = {
        "text": "تم استلام طلب استرداد الأموال الخاص بالفاتورة رقم 9022، يرجى المتابعة فوراً"
    }
    
    questions = {
        "department": {
            "type": "choice",
            "instructions": "Which department owns this message?",
            "criteria": {
                "billing": "refunds, invoices, subscriptions, payments",
                "technical_support": "bugs, crashes, hardware failures",
                "general": "general inquiries"
            }
        },
        "is_refund": {
            "type": "noul",
            "instructions": "Is the user requesting money back?"
        }
    }
    
    res = router.predict(arabic_state, questions)
    print("\n--- Arabic Routing Result ---")
    print(f"Routed Engine : {res['routing']['model']}")
    print(f"Department    : {res['answers']['department']['choice']}")
    print(f"Is Refund     : {res['answers']['is_refund']['noul']:.1%}")

if __name__ == "__main__":
    test_router_multilingual()
```

---

## 6. Integration Architecture with Aethelgard Vault & Hermes Agent

```
Incoming User Input / Telegram / Web Clipping
                     │
                     ▼
  ┌─────────────────────────────────────┐
  │      Laya System 1 Router           │  <-- Sub-35ms Fast Pass
  │  (ModernBERT / mmBERT-base 322M)    │
  └──────────────────┬──────────────────┘
                     │
         ┌───────────┴───────────┐
         ▼                       ▼
 [Simple Reflex Task]   [Complex Reasoning / Synthesis]
 - Category Classification       - Deep Research / Code Generation
 - Guardrail / Safe Prompt       - Vault Synthesis & Essay Writing
 - Vault Routing Triage          │
         │                       ▼
         │             ┌─────────────────────────────────────┐
         │             │  Hermes Agent + OmniRoute LLM       │
         │             │  (FIRST-TIME / best-coding / o3/etc)│
         │             └─────────────────┬───────────────────┘
         │                               │
         └───────────────┬───────────────┘
                         ▼
        Vault Files Updated & Telegram Feedback
```

### Key Integration Points:
1. **Vault Ingest Fast-Classifier:** Automatically classify incoming clippings into `raw/articles/`, `raw/papers/`, or specific vault domains (`computer_vision`, `embedded_systems`, `networking`, `personal`) before writing files.
2. **Telegram Message Intent Triage:** Instant zero-cost triage of whether an incoming prompt is a quick status check, vault search, code generation, or casual chat.
3. **Agent Prompt Guardrails:** High-speed filter for prompt injections or malicious inputs before passing to frontier models.

---

## 7. Calibration & Fine-Tuning Guidelines

1. **Zero-Shot Limitation Warning:**
   Laya's zero-shot baseline on arbitrary new tasks is modest (~0.35). Do not expect out-of-the-box accuracy on complex schemas without providing explicit criteria or fine-tuning.
2. **Temperature Scaling (ECE Repair):**
   To repair Expected Calibration Error (ECE) from 0.46 down to 0.08, fit a scalar temperature parameter $T > 0$ on a small validation set (50–100 samples) using negative log-likelihood:
   $$p_{\text{calibrated}} = \sigma(z / T)$$
3. **Domain Fine-Tuning:**
   Fine-tuning ModernBERT-large on 500–1,000 domain examples takes <15 minutes on a single GPU and brings accuracy up to >0.76+.

---

## 8. Rollout Checklist

- [ ] Create dedicated virtual environment `.venv-laya`
- [ ] Install `torch`, `transformers`, and `laya>=0.3.3`
- [ ] Download and cache `convaiinnovations/laya` and `laya-multilingual`
- [ ] Run `verify_laya_basic.py` and measure latency on local hardware
- [ ] Run `verify_laya_router.py` with Arabic and English test samples
- [ ] Benchmark local inference latency (CPU vs CUDA)
- [ ] Implement vault fast-routing script (`scripts/laya_vault_router.py`)

---

## 9. Cross-References
- [[laya-system-1-decision-engine]] — Laya architecture, mechanisms, and background.
- [[typesafe-ai-jev]] — Proprietary counterpart profile.
- [[laya-vs-typesafe-jev]] — Side-by-side performance scorecard.
- [[01 Technical Skills]] — Machine learning and Python skill profiles.
