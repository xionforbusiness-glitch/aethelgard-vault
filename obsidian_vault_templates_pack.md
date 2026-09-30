---
aliases: [Vault Templates, Templater Blueprints]
tags: [templates, meta, system]
created: 2026-09-19
---

# 📋 Vault Templates & Structural Blueprints

Save each section below into your `Templates/` folder in Obsidian to standardize your daily tracking, project developments, and literature reviews.

---

## 1. Daily Tracking Template (`Templates/Daily_Note_Template.md`)

```markdown
---
tags: [daily, log]
date: {{date:YYYY-MM-DD}}
day: {{date:dddd}}
---

# 📅 {{date:YYYY-MM-DD}} ({{date:dddd}})

## 🎯 Priority Objectives
- [ ] 1. 
- [ ] 2. 
- [ ] 3. 

## ⏱️ Focus Log & Deep Work
- **09:00 - 11:00:** 
- **11:30 - 13:00:** 
- **14:00 - 16:30:** 

## 🧩 Speedcubing Training Log
- **Focus:** [[Personal/Speedcubing_CFOP_Playbook|CFOP Drills]]
- **Session Average (ao12 / ao50):** 
- **Target Algorithms Practiced:** 

## 💡 Quick Thoughts & Fleeting Notes
- 

## 🔄 Daily Closeout
- **What went well today?**
- **Blockers / Friction points:**
- **Tomorrow's lead task:**
```

---

## 2. Project Execution Template (`Templates/Project_Card_Template.md`)

```markdown
---
tags: [project/active, build]
started: {{date:YYYY-MM-DD}}
status: [In Progress / Testing / Complete]
up: "[[00_Index]]"
related: []
---

# 🚀 Project Name

### 1. Problem Statement & Scope
- **Objective:** What specific problem does this project solve?
- **Deliverables:** Tangible outputs upon completion.

### 2. Architecture & Hardware Bill of Materials
- **Tech Stack:** 
- **Hardware Components:** 

### 3. Development Milestones
- [ ] Phase 1: Schematic / Architecture definition
- [ ] Phase 2: Prototype implementation
- [ ] Phase 3: Benchmarking and validation
- [ ] Phase 4: Final documentation and vault capture

### 4. Technical Hurdles & Key Learnings
- **Challenge:** 
  - **Resolution:** 
```

---

## 3. Academic Concept Note Template (`Templates/Academic_Note_Template.md`)

```markdown
---
tags: [academics, computer-science, theory]
course: "[[About/Omar_Elnemr_Bio#Education|UoPeople / SVU]]"
status: Reviewed
---

# 📖 Topic / Concept Name

### Core Definition
Provide a concise, formal definition of the theorem, algorithm, or system.

### Mathematical / Algorithmic Formulation
$$

$$

### Code Implementation or Pseudocode
```

### Practical Implications & Edge Cases
- **Time Complexity:** 
- **Space Complexity:** 
```