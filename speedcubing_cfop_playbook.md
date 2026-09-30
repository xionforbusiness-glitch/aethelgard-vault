---
aliases: [CFOP, Cubing Guide, Speedcubing, RS3M]
tags: [personal, hobbies, cubing, math]
created: 2026-09-19
up: "[[Personal/Gear_and_Interests]]"
---

# 🧊 Speedcubing CFOP Playbook

A dedicated reference manual for 3x3 speedsolving using the **CFOP Method** (Cross, First Two Layers, Orientation of the Last Layer, Permutation of the Last Layer).

---

## 1. CFOP Solving Stages

$$\text{Solve Flow:}\quad \text{Cross} \longrightarrow \text{F2L (4 Pairs)} \longrightarrow \text{OLL (57 Cases)} \longrightarrow \text{PLL (21 Cases)}$$

1. **Cross:** Solve 4 bottom edges directly connected to center pieces (target: $\le 8$ moves, full inspection planning).
2. **F2L (First Two Layers):** Concurrently pair up and insert 4 corner-edge pairs into their respective slots.
3. **OLL (Orientation of the Last Layer):** Orient all top-layer stickers to face upward (yellow face complete).
4. **PLL (Permutation of the Last Layer):** Permute pieces in the top layer to finish the solve.

---

## 2. Key OLL Algorithm Reference

### OLL 23 (Headlights Case)
- **State:** All 4 corners oriented incorrectly, with 2 headlights pointing forward and 2 facing backward.
- **Algorithm:**
  $$R2 \cdot D \cdot (R' \cdot U2 \cdot R) \cdot D' \cdot (R' \cdot U2 \cdot R')$$

### OLL 21 (Cross Case - Double Sune)
- **Algorithm:**
  $$(R \cdot U \cdot R' \cdot U) \cdot (R \cdot U' \cdot R' \cdot U) \cdot (R \cdot U2 \cdot R')$$

### OLL 24 (T-Shape Orientation)
- **Algorithm:**
  $$(r \cdot U \cdot R' \cdot U') \cdot (r' \cdot F \cdot R \cdot F')$$

---

## 3. Essential PLL Cases

### T-Permutation (Adjacent Corner & Edge Swap)
- **Algorithm:**
  $$(R \cdot U \cdot R' \cdot U') \cdot (R' \cdot F \cdot R2 \cdot U') \cdot (R' \cdot U' \cdot R \cdot U) \cdot (R' \cdot F')$$

### Y-Permutation (Diagonal Corner Swap)
- **Algorithm:**
  $$F \cdot (R \cdot U' \cdot R' \cdot U') \cdot (R \cdot U \cdot R' \cdot F') \cdot (R \cdot U \cdot R' \cdot U') \cdot (R' \cdot F \cdot R \cdot F')$$

### U-Permutations (3-Edge Cycle)
- **Ua-Perm (Counter-clockwise):**
  $$R \cdot U' \cdot (R \cdot U \cdot R \cdot U) \cdot (R \cdot U') \cdot R' \cdot U' \cdot R2$$
- **Ub-Perm (Clockwise):**
  $$R2 \cdot U \cdot (R \cdot U \cdot R' \cdot U') \cdot R' \cdot U' \cdot (R' \cdot U \cdot R')$$

---

## 4. Hardware Maintenance: MoYu RS3M MagLev Setup

```
                     ┌─────────────────────────┐
                     │    Center Cap Removed   │
                     └────────────┬────────────┘
                                  │
                                  ▼
                     [ Screw Tension Adjustment ]
                     (Sets baseline corner-cutting)
                                  │
                                  ▼
                   [ Dual Magnetic Ring (MagLev) ]
                 (Adjusts spring-compression feel)
```

- **MagLev Principle:** Replaces traditional steel springs with two repelling neodymium ring magnets, completely eliminating spring noise and mechanical friction.
- **Lubrication Protocol:**
  - **Core/Tracks:** Apply high-viscosity silicone lube (e.g., Weight 5) along track contact points to introduce controllable dampening.
  - **Piece Surfaces:** Apply 1-2 drops of low-viscosity, speed-enhancing lubricant to maintain quick slice turns.