---
title: "LLM Council: Multi-Agent Adversarial Deliberation & Decision Architecture"
created: 2026-10-25
updated: 2026-10-25
type: concept
tags: [ai-agents, decision-making, llm-council, karpathy, consensus, peer-review, sycophancy, strategy, wargame]
sources: [Andrej Karpathy (LLM Council), Ole Lehmann / aiwithremy, Abdallah Reel 1740366650357923]
confidence: high
contested: false
contradictions: []
---

# 🏛️ LLM Council (مجلس الذكاء الاصطناعي): Karpathy's Multi-Agent Decision Framework

> **"A single LLM will tell you what you want to hear. The LLM Council forces 5 adversarial AI advisors to argue your decision, anonymously peer-review each other's blind spots, and hand you a battle-tested verdict you can actually trust."**  
> Operational breakdown of the **LLM Council** methodology, designed to eliminate LLM sycophancy, confirmation bias, and shallow reasoning on high-stakes business, technical, and life decisions.

---

## ⚡ The Sycophancy Problem in Single-Prompt LLMs

When facing hard tradeoffs (e.g., *"Should I buy this $650 laptop or save for my wedding?"*, *"Which career path should I prioritize?"*, *"Should I build a custom bot or use an off-the-shelf tool?"*), standard LLMs default to:
1. **Sycophancy:** Subconsciously validating whatever premise you introduce in the prompt.
2. **Surface Agreement:** Offering generic pros and cons without taking a definitive stance.
3. **Monolithic Blind Spots:** Looking at the problem from only one statistical perspective.

**The Council Methodology:** Pits 5 distinct, unhedged thinking lenses against each other in parallel, forces an anonymous peer-review audit, and culminates in a decisive Chairman verdict.

---

## 👥 The 5 Council Advisors

```
                              ┌─────────────────────────┐
                              │     FRAMED DECISION     │
                              └────────────┬────────────┘
                                           │
         ┌───────────────┬─────────────────┼─────────────────┬───────────────┐
         ▼               ▼                 ▼                 ▼               ▼
  ┌─────────────┐ ┌───────────────┐ ┌───────────────┐ ┌─────────────┐ ┌─────────────┐
  │ CONTRARIAN  │ │FIRST PRINCIPLE│ │  EXPANSIONIST │ │  OUTSIDER   │ │  EXECUTOR   │
  ├─────────────┤ ├───────────────┤ ├───────────────┤ ├─────────────┤ ├─────────────┤
  │ Hunts fatal │ │ Strips false  │ │ Asymmetric    │ │ Zero curse  │ │ "What do we │
  │ flaws &     │ │ assumptions;  │ │ upside &      │ │ of knowledge│ │ do Monday   │
  │ downside    │ │ root causes   │ │ scale levers  │ │ fresh eyes  │ │ morning?"   │
  └──────┬──────┘ └───────┬───────┘ └───────┬───────┘ └──────┬──────┘ └──────┬──────┘
         │                │                 │                │               │
         └────────────────┴────────┬────────┴────────────────┴───────────────┘
                                   │
                                   ▼
                   ┌───────────────────────────────┐
                   │    ANONYMOUS PEER REVIEW      │
                   │ (Blind-spot & strength audit) │
                   └───────────────┬───────────────┘
                                   │
                                   ▼
                   ┌───────────────────────────────┐
                   │       CHAIRMAN VERDICT        │
                   │ (Consensus, Tension, Verdict) │
                   └───────────────────────────────┘
```

### 1. The Contrarian (صوت المعارضة والمخاطر)
* **Objective:** Find why this idea will fail.
* Assumes the plan has a hidden, fatal flaw. Hunts down worst-case scenarios, legal liabilities, burnout risks, and money traps.

### 2. The First Principles Thinker (المبادئ الأولى)
* **Objective:** Strip away conventional wisdom and industry jargon.
* Asks: *"What is the actual physics or economic bottleneck here?"* Frequently reveals that the user is agonizing over the completely wrong question.

### 3. The Expansionist (التوسع والفرص غير المرئية)
* **Objective:** Uncap the upside.
* Disregards downside risks to ask: *"What if this works 10x better than expected? What adjacent leverage are we leaving on the table?"*

### 4. The Outsider (عين الغريب المحايدة)
* **Objective:** Cut through insider jargon and emotional baggage.
* Evaluates the situation with zero historical bias. Identifies what sounds obvious to the user but completely incoherent to everyone else.

### 5. The Executor (التنفيذي الواقعي)
* **Objective:** Turn strategy into tactical steps.
* Disregards philosophy and asks: *"Can this realistically be accomplished? What is the literal first action required on Monday morning?"*

---

## 🏛️ The 4-Stage Protocol

1. **Phase 1: Workspace Context Enrichment:**  
   The agent scans relevant vault notes (`00 Profile`, `work_attendance_and_shift_roster`, project blueprints) to ground the question with exact dates, finances, and constraints.
2. **Phase 2: Unhedged Independent Takes (Parallel):**  
   Each advisor generates a 150–250 word uncompromised analysis. Zero polite diplomatic middle ground.
3. **Phase 3: Blind Peer Review:**  
   Takes are anonymized as `Response A` through `E`. Advisors evaluate which argument has the strongest thesis and what all 5 missed.
4. **Phase 4: Chairman Verdict:**  
   Delivers the final output categorized into:
   - 🤝 **Unanimous Consensus** (Universal truths)
   - ⚔️ **Core Strategic Tension** (The non-negotiable tradeoff)
   - 🎯 **Actionable Monday Morning Verdict**

---

## 🔗 Related Notes & Vault Assets

* [[concepts/claude-code-boris-cherny-power-user-playbook|Claude Code Boris Cherny Playbook]]
* [[concepts/unlazy-anti-laziness-agent-skill|Unlazy: Completion Discipline Skill]]
* [[00 Profile|Omar Elnemr Profile & Life Architecture]]
* [[01 Technical Skills|Technical Skills Knowledge Base]]
* [[log|Operational Log]]
