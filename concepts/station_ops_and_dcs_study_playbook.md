---
title: Station Operations & Amadeus Altéa DCS Master Study Playbook
created: 2026-10-10
updated: 2026-10-10
type: concept
tags: [aviation, station-ops, dcs, amadeus-altea, iata-codes, etihad, leadership, damascus-airport]
sources: [concepts/etihad-igs-training-curriculum.md, aviation_ground_operations_dcs_guide.md]
confidence: high
contested: false
---

# ✈️ Damascus Station Operations & Amadeus Altéa DCS Master Study Playbook

> **Purpose:** Comprehensive operational study guide, IATA SSR/SPML code reference, Amadeus Altéa DCS command cheatsheet, and Executive Station Leadership Protocol for [[03 Work Experience|Omar Elnemr]] at Damascus International Airport (`DAM / OSDI`).

---

## 🏛️ Part 1: The Executive Station Leadership Protocol

### 1. The Operational Shift Strategy
* **Isolate Your Excellence:** Stop representing unmotivated peers. Focus 100% on being the most disciplined, precise, and knowledgeable Ground Operations Specialist at Damascus Station.
* **Direct Management Visibility:** Communicate concise, high-value station observations directly to station supervisors and airline station managers.
* **Refusal of Informal Mediation:** When peers ask you to cover or argue on their behalf, respond calmly:
  > *"Management assigned supervisors for each airline station. You need to report directly to your supervisor."*

---

## ♿ Part 2: IATA Special Service Request (SSR) Codes

| SSR Code | Full Description | Station Handling Protocol |
| :---: | :--- | :--- |
| **WCHR** | Wheelchair - Ramp / Distance | Passenger can walk up/down stairs and to seat, but needs wheelchair for long concourse distance. |
| **WCHS** | Wheelchair - Steps | Passenger cannot negotiate stairs, but can walk slowly to aircraft seat. Needs stair-chair assistance. |
| **WCHC** | Wheelchair - Cabin / Carry-on | Passenger completely immobile. Requires aisle-chair transfer into aircraft seat. |
| **UMNR** | Unaccompanied Minor (Ages 5–11) | Hand-delivered to Cabin Crew Lead with UM pouch, passport, visas, and declaration forms. Never left unattended. |
| **MEDA** | Medical Clearance Required | Requires airline MEDIF medical form approval before check-in and boarding clearance. |
| **STCR** | Stretcher Passenger | Occupies multiple seat rows (usually 6 seats). Requires medical team and ramp elevator lift (ambulift). |
| **MAAS** | Meet and Assist | VIP, elderly, or non-English/Arabic speaking guest requiring staff escort through terminal. |
| **INAD** | Inadmissible Passenger | Passenger refused entry by border immigration. Must be returned on next available carrier flight. |
| **DEPA** | Deportee - Accompanied | Deportee escorted by armed security / law enforcement officers. |
| **DEPU** | Deportee - Unaccompanied | Unescorted deportee. Documentation held by Station Captain / Lead. |
| **PETC** | Pet in Cabin | Small animal in approved container under forward seat (weight limit ~8kg including carrier). |
| **AVIH** | Animal in Hold | Live animal transported in temperature-controlled bulk cargo hold. |
| **BSCT** | Baby Bassinet | Infant seat allocation at bulkhead wall rows equipped with bassinet attachments. |

---

## 🥗 Part 3: IATA Special Meal (SPML) Codes

| SPML Code | Meal Type | Description & Dietary Rules |
| :---: | :--- | :--- |
| **MOML** | Muslim Meal | Prepared in strict accordance with Islamic Halal dietary laws (No pork, alcohol, or non-halal meat). |
| **KSML** | Kosher Meal | Sealed & certified Kosher meal prepared under Rabbinical supervision. Unsealed only in front of guest. |
| **HNML** | Hindu Meal | Non-vegetarian meal containing no beef or pork. Contains poultry, mutton, or fish. |
| **DBML** | Diabetic Meal | Low sugar, high complex carbohydrates, lean protein, and high fiber. |
| **GFML** | Gluten-Intolerant Meal | Strictly excludes wheat, rye, barley, oats, and gluten-derived ingredients. |
| **VGML** | Vegetarian Vegan Meal | Strictly plant-based meal. No meat, fish, dairy, eggs, milk, or honey. |
| **VOML** | Vegetarian Oriental Meal | Chinese-style vegetarian meal prepared with vegetables, tofu, and rice (no dairy/eggs). |
| **CHML** | Child Meal (Ages 2–11) | Easily identifiable child-friendly meal (burgers, nuggets, pasta, juice box). |
| **BBML** | Baby Meal (Under 2 years) | Strained commercial baby food jars and formula. |

---

## 🖥️ Part 4: Amadeus Altéa DCS Commands & Gate Operations

### 1. Customer Management (Altéa CM) Essentials
* **Passenger Search:** `PD` (Passenger Display) / `PD/NAME-ELNEMR/OMAR`
* **Display Flight Manifest:** `FDL` (Flight Details List) / `FDL/EY065/10OCT`
* **Customer Check-In:** `CK` (Check-In) / `CK/SEAT-12A/BAG-1`
* **Boarding Pass Issuance:** `BP` (Boarding Pass)
* **Baggage Tag Printing:** `BT` (Bag Tag) / `BT/WEIGHT-23KG`
* **Seat Map Display:** `SM` (Seat Map) / `SM/EY065/10OCT/C` (Business Class)
* **Standby List Reconciliation:** `GOS` (Gate Accept Standby) / `GOS/STBY-1`

### 2. Mandatory Document Audits (TIMATIC)
1. **Passport Validity:** Minimum **6 months** remaining validity from return date for most international destinations.
2. **Transit Visas:** Audit transit visa rules for Abu Dhabi (`AUH`), Jeddah (`JED`), and Riyadh (`RUH`) stops.
3. **Ok To Board (OTB):** Required for Syrian passport holders traveling to specific GCC stations. Ensure verified electronic visa is attached to PNR.

---

## 📊 Part 5: Station Lead Daily Operations Checklist

```
[01] ✈️ Pre-Flight Briefing: Review flight load sheet, seat capacity, SSR counts (WCHR, UMNR, MEDA).
[02] 🖥️ System Check-In: Verify Amadeus Altéa / Airline DCS connectivity at check-in counters.
[03] 🎫 Passenger Handling: Verify passports, visas, TIMATIC clearance, and SSR special requests.
[04] 🧳 Baggage Security: Audit bag tags, heavy bag stickers (>23kg / >32kg limit), and fragile items.
[05] 🚪 Gate Departure: Manage priority boarding (Business/Gold members), final head count, and door closure.
```

---

## 🔗 Related Vault Notes
- [[aviation_ground_operations_dcs_guide]] — Core DCS Amadeus Altéa reference guide.
- [[entities/etihad-airways-station-operations]] — Etihad Airways Abu Dhabi transit & station playbook.
- [[concepts/etihad-igs-training-curriculum]] — Solved Etihad IGS training curriculum.
- [[work_attendance_and_shift_roster]] — Master team attendance and shift ledger.
