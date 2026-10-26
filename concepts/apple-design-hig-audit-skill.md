---
title: "Apple Design Skill: Human Interface Guidelines (HIG) & Luxury UI/UX Audit Engine"
created: 2026-10-26
updated: 2026-10-26
type: concept
tags: [apple-design, ui-ux, hig, design-system, claude-skill, typography, micro-interactions, webdev, mobile-design]
sources: [dickwu/apple-design-skill (GitHub, 2k+ stars), Abdallah Reel 1141750415066607, Apple Human Interface Guidelines]
confidence: high
contested: false
contradictions: []
---

# 🍏 Apple Design Skill: Human Interface Guidelines (HIG) & Luxury UI/UX Audit

> **"You aren't asking AI to copy Apple's website; you are equipping it with the foundational design principles behind the elegance of Apple products—typography hierarchy, breathing whitespace, tactile squircle radiuses, and physical micro-animations—to elevate your own apps."**  
> Technical breakdown of the viral **Apple Design Skill** (`dickwu/apple-design-skill`), an agent skill with 123+ indexed Apple HIG reference specifications that audits, critiques, and refactors UI code across web, iOS, Flutter, React, Tauri, and Electron.

---

## ⚡ The Core Philosophy: Platform Rigor + Boutique Craft

Generic AI-generated web apps (vibe coding) suffer from a distinct "cheap" look:
* Inconsistent padding and cramped margin hierarchy.
* Overly harsh drop shadows and neon gradient clashes.
* Mismatched border radiuses (e.g. sharp concentric padding clashes).
* Chaotic scroll animations that lack momentum physics.

**The Apple Design Skill operates under two personas simultaneously:**
1. **The Senior Platform Reviewer:** Strict adherence to Apple's **Human Interface Guidelines (HIG)** across typography scales, touch targets (minimum 44×44pt), contrast ratios, and dark mode dynamics.
2. **The Boutique Studio Lead:** Pushes for distinct, premium visual restraint—using intentional negative space, continuous curvature (squircles), and subtle glassmorphic depth (`Liquid Glass`).

---

## 📐 The 6 Pillars of Apple-Level Polish

```
┌────────────────────────────────────────────────────────────────────────┐
│                   APPLE-GRADE DESIGN CRITIQUE MATRIX                   │
├─────────────────────┬──────────────────────────────────────────────────┤
│ 1. Visual Hierarchy │ Single clear hero focal point; 3:1 content scale │
│ 2. Intentional Space│ Generous padding; breathing room over density    │
│ 3. Typographic Lead │ Dynamic Type ratios, SF Pro / clean sans balance │
│ 4. Tactile Radii    │ Continuous curvature (squircles), concentric nested│
│ 5. Physical Motion  │ Spring curves (0.3s–0.5s), zero linear animations│
│ 6. Depth & Glass    │ Subtle background blur (backdrop-filter: blur),  │
│                     │ translucent materials over opaque flat solids    │
└─────────────────────┴──────────────────────────────────────────────────┘
```

---

## 🛠️ How to Use It in Hermes & Claude

The full skill is installed in your profile at:  
`~/.hermes/profiles/llm-wiki/skills/design/apple-design/`

### 1. The Design Audit Workflow
Feed your HTML/CSS, Tailwind code, React component, or a screenshot of your app, and ask:
> *"Audit this UI against Apple HIG and design craft principles. What makes it look generic or unrefined, and how do we fix it?"*

### 2. What the Skill Inspects:
* **Typography:** Line height (leading), tracking (letter spacing), and strict weight contrast (Headline Bold vs Body Regular).
* **Concentric Radii:** Ensuring inner container radius equals `outer_radius - padding` so borders don't look warped.
* **Micro-interactions:** Replacing jarring fades with spring-damped transforms (`cubic-bezier(0.16, 1, 0.3, 1)`).
* **Color Restraint:** Eliminating rainbow palettes; restricting to 1 primary accent color with neutral monochromatic grays.

---

## 🔗 Related Notes & Vault Assets

* [[concepts/ui-ux-design-tools-ecosystem|UI/UX Design Tools Ecosystem]]
* [[concepts/ai-motion-graphics-code-design-styles|AI Motion Graphics Code Design Styles]]
* [[concepts/vibe-coder-legal-compliance-checklist|Vibe Coder Compliance Checklist]]
* [[01 Technical Skills|Technical Skills Knowledge Base]]
* [[log|Operational Log]]
