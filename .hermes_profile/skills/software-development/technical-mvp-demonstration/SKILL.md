---
name: technical-mvp-demonstration
description: Use when creating technical MVP simulations for investors.
---

# Technical MVP Demonstration Workflow

Use this skill when tasked with building an "MVP" or "interactive demo" for a technical product study or investor pitch.

## Core Principle: Functional Simulation > Static Mockup

Investors judge technical products by the fidelity of their "system view." A shallow UI shell that looks like a static webpage is often perceived as unprofessional or vaporware. The demonstration must highlight the system's *intelligence* and *autonomous orchestration*.

## Workflow Steps

1. **Understand the System Architecture:**
   - Review the provided technical documentation (architecture, agent roles, data flow).
   - Identify the "Magic" factor (the core autonomous process to simulate).
2. **Design for Architectural Depth:**
   - Do not just build a front-end shell.
   - Design the simulation to reflect the underlying logic described in documentation.
3. **Visualize Data Flow & State:**
   - The cockpit/dashboard must visualize:
     - Real-time state transitions (e.g., Intake → Research → Generation).
     - Data hand-offs between agent modules (displaying representative JSON/event objects).
     - Closed-loop feedback mechanisms (the "Magic" factor of the system).
4. **Implement Functional Simulation:**
   - Build a lightweight event-stream processor or state machine in JavaScript.
   - UI should reflect the technical "cockpit" of the system, showcasing agent states (Thinking, Processing, Error Correction, Scheduled), not just dummy graphics.
5. **Verify Fidelity:**
   - Does it show how the system works, not just how it looks?
   - Does it capture the "autonomous intelligence" of the backend?
