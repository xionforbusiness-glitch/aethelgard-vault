---
aliases: [AI Evaluation, RLHF Guidelines, Annotation Handbook]
tags: [work, ai, rlhf, annotation, methodology]
created: 2026-09-19
up: "[[Work/Experience_and_Roles]]"
---

# 🤖 AI Evaluation & Annotation Methodology Handbook

A standardized evaluation rubric and best practices guide based on data annotation projects across **Alignerr**, **Outlier**, **TaskVerse**, **DataForce**, and **RWS**.

---

## 1. Core Evaluation Dimensions

```
                                  [ MODEL RESPONSE ]
                                           │
         ┌───────────────────┬─────────────┴─────────────┬──────────────────┐
         ▼                   ▼                           ▼                  ▼
    [ Truthfulness ]   [ Instruction ]               [ Safety & ]        [ Code & ]
     & Factuality        Following                    Harmlessness        Execution
         │                   │                           │                  │
   Verified via        Every explicit               No dangerous,      Free of syntax
  Primary Sources      constraint met               PII, or toxic      errors & logic
   & Valid Data       (format/length)                 material              bugs
```

---

## 2. The 4-Tier Assessment Rubric

### 1. Instruction Following
- **Negative Constraints:** Did the model follow negative rules (e.g., *"Do not include bullet points"*, *"Do not use the word 'therefore'"*)?
- **Format Compliance:** Markdown headers, valid JSON schemas, tables, or character limits.
- **Tone & Persona:** Adherence to requested audience calibrations (e.g., beginner-friendly vs. senior software engineer).

### 2. Truthfulness & Factuality
- **Hallucination Detection:** Verification of libraries, functions, named entities, historical dates, or scientific values.
- **Source Verification:** Cross-referencing technical API assertions directly against official documentation (e.g., Python docs, MDN, PyTorch/Ultralytics docs).

### 3. Code Correctness & Engineering Standards
- **Syntactic Validity:** Does the code run without syntax errors?
- **Edge-Case Resilience:** Are null inputs, division by zero, empty arrays, and connection dropouts handled gracefully?
- **Security Best Practices:** Absence of SQL injection vulnerabilities, hardcoded API secrets, or deprecated cryptographic methods.

---

## 3. Arabic NLP & Localization Nuances

When annotating Arabic LLM outputs, generic machine translation rules fail. Critical linguistic considerations include:

### Modern Standard Arabic (MSA) vs. Dialects (Ammiya)
- Identify prompt context: Academic and professional prompts require strict MSA (**الفصحى**).
- Regional conversational queries (Levantine, Egyptian, Gulf) require dialectal nuance without incorrect grammatical corrections that distort user intent.

### Grammatical Agreement & Morphology
- Dual forms (**المثنى**) and sound feminine vs. broken plurals (**جمع التكسير**).
- Accurate handling of diacritics (**التشكيل**) when resolving homographs (words spelled identically that have different meanings and pronunciations).
- Technical terms: Prioritize standardized contemporary terminology over awkward literal translations (e.g., use **واجهة برمجة التطبيقات** for API or keep international abbreviations intact).