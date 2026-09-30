## aliases: \[Sea of Conquest, Naval Strategy, Maritime Mechanics\]
tags: \[personal, gaming, strategy, naval\]
created: 2026-09-19
up: "\[\[Personal/Gear_and_Interests\]\]"
related: ["\[\[Personal/Media_Analysis_and_Worldbuilding\]\]"]

# ⚓ Sea of Conquest: Fleet Strategy & Naval Combat Operations

A tactical mechanics reference covering flagship internal deck engineering, naval combat damage calculations, and maritime trade arbitrage loops.

## 1. Flagship Room Architecture & Compartmentalization

The Flagship serves as both mobile base and primary combat unit. Internal room layout directly alters operational stats:

```
                      [ Upper Gun Deck ]
                  (Artillery & Broadside Reload)
                               │
               ┌───────────────┴───────────────┐
               ▼                               ▼
       [ Navigation Room ]             [ Medical Bay ]
     (Rudder Turning Speed)           (Crew Recovery Rate)
               │                               │
               └───────────────┬───────────────┘
                               ▼
                        [ Cargo Hold ]
                   (Trade Arbitrage Capacity)
```

### Optimal Room Upgrades Priority
1. **Gun Deck & Turrets:** Directly increases reload velocity and raw broadside damage output.
2. **Galley & Crew Quarters:** Boosts overall ship morale, lowering the degradation rate of combat effectiveness during prolonged naval engagements.
3. **Storage / Cargo Hold:** Expands maximum cargo weight, allowing larger cargo hauls when running regional trade routes.

---

## 2. Naval Combat Mechanics & Damage Formulas

Naval battles in *Sea of Conquest* involve distance decay, armor mitigation, and elemental status triggers:

### Effective Damage Equation
The damage dealt by an artillery salvo is modeled by:

$$\text{Damage} = \frac{\text{Base Artillery Attack} \times (1 + \text{Crit Multiplier})}{\left(1 + \frac{\text{Target Armor}}{k}\right)} \times \left(1 - \text{Decay}_{\text{distance}}\right)$$

Where:
- $k$ is the ship armor scaling constant.
- $\text{Decay}_{\text{distance}}$ applies when firing outside optimal cannon range.

### Elemental Status Synergy
- **Blazing (Fire):** Stacks continuous damage-over-time (DoT); when fire stacks reach maximum, triggers a ship explosion dealing percentage hull damage.
- **Drowning (Water):** Slows the enemy vessel's turning speed, locking them into your broadside firing cone.
- **Armor Piercing:** Reduces effective target armor rating, increasing incoming damage from auxiliary escort ships.

---

## 3. Maritime Economic Arbitrage Loop

Wealth generation relies on regional price differentials for commodities across maritime ports.

```
       [ Buy Port A Surplus ] ──────────> [ Sail High-Speed Trade Route ]
       (e.g., Cheap Tobacco/Rum)                     │
                                                     ▼
       [ High Port Investment ] <───────── [ Sell Port B Deficit ]
       (Unlocks Rare Blueprints)            (Maximize Profit Margin)
```

- **Trading Protocol:**
  1. Inspect the port trade ledger for items marked **Surplus (Green)**.
  2. Map transit to neighboring ports listing those commodities as **In Demand (Red)**.
  3. Reinvest trade profits into Port Reputation to unlock high-tier flagship components and rare cannon blueprints.