#!/usr/bin/env python3
"""
===============================================================================
✈️ RUNWAY WINDSHEAR & CROSSWIND ANALYZER (Aethelgard Aviation Ops)
Station: Damascus International Airport (OSDI / DAM) & General Aerodromes
ICAO Standards: Doc 9817 (Manual on Low-level Wind Shear and Turbulence)
===============================================================================
"""

import math
import sys
import argparse
import json
from dataclasses import dataclass, asdict
from typing import List, Tuple, Optional

# Standard Fleet Limits (Dry Runway Crosswind Limits in Knots)
DEFAULT_FLEET_LIMITS = {
    "A320": {"max_crosswind": 33, "max_tailwind": 10, "max_gust_spread": 15},
    "A321": {"max_crosswind": 33, "max_tailwind": 10, "max_gust_spread": 15},
    "A330": {"max_crosswind": 32, "max_tailwind": 15, "max_gust_spread": 20},
    "B777-300ER": {"max_crosswind": 38, "max_tailwind": 15, "max_gust_spread": 20},
    "B787-9": {"max_crosswind": 33, "max_tailwind": 15, "max_gust_spread": 20},
    "B737-800": {"max_crosswind": 33, "max_tailwind": 10, "max_gust_spread": 15},
}

# Aerodrome Runway Configurations (Damascus International Airport - OSDI)
DAMASCUS_RUNWAYS = {
    "05R": {"heading": 53, "length_m": 3600, "surface": "Asphalt/Concrete"},
    "23L": {"heading": 233, "length_m": 3600, "surface": "Asphalt/Concrete"},
    "05L": {"heading": 53, "length_m": 3000, "surface": "Asphalt/Concrete"},
    "23R": {"heading": 233, "length_m": 3000, "surface": "Asphalt/Concrete"},
}


@dataclass
class WindVector:
    direction: float  # Magnetic degrees (0-360)
    speed_kts: float   # Sustained speed in knots
    gust_kts: float    # Gust speed in knots (0 if none)


@dataclass
class WindshearMetrics:
    headwind_kts: float
    crosswind_kts: float
    crosswind_direction: str  # "LEFT" or "RIGHT"
    is_tailwind: bool
    tailwind_kts: float
    gust_spread_kts: float
    windshear_loss_gain_kts: float
    f_factor: float           # Bowles F-Factor hazard index
    hazard_level: str         # "NORMAL", "CAUTION", "WARNING_WINDSHEAR", "CRITICAL_MICROBURST"
    exceedances: List[str]
    recommendation: str


def calculate_runway_components(
    runway_heading: float,
    wind: WindVector,
    altitude_agl_ft: float = 500.0,
    aircraft_type: str = "B777-300ER",
    wet_runway: bool = False
) -> WindshearMetrics:
    """
    Computes Headwind, Crosswind, Tailwind, Windshear Loss/Gain, and F-Factor.
    
    F-Factor Formula (Bowles / NASA / FAA):
      F = (dV/dt) / g - (w / V_TAS)
      Hazard Threshold: F >= 0.105 (Alert), F >= 0.13 (Microburst Warning)
    """
    angle_rad = math.radians(wind.direction - runway_heading)
    
    # Wind component along runway axis (+ = Headwind, - = Tailwind)
    longitudinal = wind.speed_kts * math.cos(angle_rad)
    
    # Wind component perpendicular to runway (+ = Right, - = Left)
    lateral = wind.speed_kts * math.sin(angle_rad)
    
    # Gust-adjusted vectors
    effective_speed = max(wind.speed_kts, wind.gust_kts) if wind.gust_kts > 0 else wind.speed_kts
    gust_spread = max(0.0, wind.gust_kts - wind.speed_kts) if wind.gust_kts > 0 else 0.0
    
    headwind = max(0.0, longitudinal)
    tailwind = abs(longitudinal) if longitudinal < 0 else 0.0
    is_tailwind = longitudinal < 0
    
    crosswind = abs(lateral)
    crosswind_dir = "FROM RIGHT" if lateral > 0 else ("FROM LEFT" if lateral < 0 else "DIRECT")
    
    # Low Level Windshear Delta Calculation (ICAO Doc 9817 LLWAS Model)
    # Windshear vector difference between surface and approach path (simulated/reported)
    windshear_delta = gust_spread + (abs(tailwind) * 1.5 if is_tailwind else 0.0)
    
    # F-Factor Hazard Index Calculation
    # Approximating longitudinal shear rate and vertical downdraft component
    tas_knots = 140.0  # standard approach V_ref + 5
    v_tas_fps = tas_knots * 1.68781
    shear_rate_fps2 = (windshear_delta * 1.68781) / 10.0  # assumed 10s traversal
    g = 32.174
    
    downdraft_fps = (windshear_delta * 0.4) * 1.68781  # typical microburst downdraft ratio
    f_factor = (shear_rate_fps2 / g) + (downdraft_fps / v_tas_fps)
    
    # Check Aircraft Fleet Limits
    limits = DEFAULT_FLEET_LIMITS.get(aircraft_type, DEFAULT_FLEET_LIMITS["B777-300ER"])
    max_xwind = limits["max_crosswind"] * (0.75 if wet_runway else 1.0)
    max_twind = limits["max_tailwind"] * (0.80 if wet_runway else 1.0)
    
    exceedances = []
    if crosswind > max_xwind:
        exceedances.append(f"CROSSWIND EXCEEDED ({crosswind:.1f} kts > Limit {max_xwind:.1f} kts)")
    if is_tailwind and tailwind > max_twind:
        exceedances.append(f"TAILWIND EXCEEDED ({tailwind:.1f} kts > Limit {max_twind:.1f} kts)")
    if gust_spread > limits["max_gust_spread"]:
        exceedances.append(f"GUST SPREAD EXCEEDED ({gust_spread:.1f} kts > Limit {limits['max_gust_spread']} kts)")
        
    # Determine Threat Level
    if f_factor >= 0.130 or windshear_delta >= 25.0:
        hazard = "CRITICAL_MICROBURST"
        rec = "🛑 IMMEDIATE GO-AROUND / EXECUTE WINDSHEAR ESCAPE MANEUVER. Do not change aircraft configuration until clear."
    elif f_factor >= 0.105 or windshear_delta >= 15.0 or len(exceedances) > 0:
        hazard = "WARNING_WINDSHEAR"
        rec = "⚠️ WINDSHEAR ALERT: Significant airspeed loss/gain expected. Consider go-around or runway change."
    elif gust_spread >= 10.0 or crosswind >= (max_xwind * 0.8):
        hazard = "CAUTION"
        rec = "⚡ CAUTION: Moderate turbulence and gusty crosswind. Maintain stabilized approach airspeed (V_REF + Gust Addition)."
    else:
        hazard = "NORMAL"
        rec = "✅ NORMAL: Runway wind vectors within standard operational parameters."
        
    return WindshearMetrics(
        headwind_kts=round(headwind, 1),
        crosswind_kts=round(crosswind, 1),
        crosswind_direction=crosswind_dir,
        is_tailwind=is_tailwind,
        tailwind_kts=round(tailwind, 1),
        gust_spread_kts=round(gust_spread, 1),
        windshear_loss_gain_kts=round(windshear_delta, 1),
        f_factor=round(f_factor, 4),
        hazard_level=hazard,
        exceedances=exceedances,
        recommendation=rec
    )


def generate_ascii_visualizer(runway_id: str, runway_hdg: float, wind: WindVector, metrics: WindshearMetrics) -> str:
    """Renders high-density ASCII runway wind compass diagram."""
    status_icon = "🟢" if metrics.hazard_level == "NORMAL" else ("🟡" if metrics.hazard_level == "CAUTION" else "🔴")
    
    diagram = f"""
┌────────────────────────────────────────────────────────────────────────┐
│ 🛫 RUNWAY WINDSHEAR VECTOR MONITOR — RWY {runway_id:<4} (HDG {runway_hdg:03.0f}°)       {status_icon} │
├────────────────────────────────────────────────────────────────────────┤
│ Wind Direction : {wind.direction:03.0f}° @ {wind.speed_kts:.0f} kts (Gusts: {wind.gust_kts:.0f} kts)                        │
│ Headwind Comp  : {metrics.headwind_kts:5.1f} kts  │ Tailwind Comp : {metrics.tailwind_kts:5.1f} kts                │
│ Crosswind Comp : {metrics.crosswind_kts:5.1f} kts  │ Crosswind Dir : {metrics.crosswind_direction:<10}              │
│ Gust Spread    : {metrics.gust_spread_kts:5.1f} kts  │ Windshear ΔV  : {metrics.windshear_loss_gain_kts:5.1f} kts                │
│ Bowles F-Factor: {metrics.f_factor:6.4f}   │ Threat Status : {metrics.hazard_level:<20} │
├────────────────────────────────────────────────────────────────────────┤
│                          [ RUNWAY ALIGNMENT ]                          │
│                                                                        │
│                                 {runway_hdg:03.0f}°                                │
│                                  ▲                                     │
│                                  │                                     │
│                           ┌──────┴──────┐                              │
│                           │  [=== {runway_id:<3} ===] │                              │
│                           │      |      │                              │
│                           │      |      │                              │
│                           │      |      │                              │
│                           │      |      │                              │
│                           │  [=== {runway_id:<3} ===] │                              │
│                           └──────┬──────┘                              │
│                                  │                                     │
│                                                                        │
│ Threat Evaluation: {metrics.hazard_level:<48}    │
│ Action: {metrics.recommendation:<59} │
└────────────────────────────────────────────────────────────────────────┘
"""
    return diagram


def run_full_aerodrome_analysis(wind: WindVector, aircraft: str = "B777-300ER", wet: bool = False):
    print("=" * 74)
    print(f"✈️ AETHELGARD AERODROME WINDSHEAR AUDIT: Damascus Int'l (OSDI / DAM)")
    print(f"Target Aircraft: {aircraft} | Surface: {'WET' if wet else 'DRY'} | Reported Wind: {wind.direction:03.0f}°/{wind.speed_kts:.0f}G{wind.gust_kts:.0f}KT")
    print("=" * 74)
    
    best_runway = None
    min_hazard_score = 999
    
    for rwy_id, rwy_info in DAMASCUS_RUNWAYS.items():
        metrics = calculate_runway_components(rwy_info["heading"], wind, aircraft_type=aircraft, wet_runway=wet)
        print(generate_ascii_visualizer(rwy_id, rwy_info["heading"], wind, metrics))
        
        # Scoring optimal runway
        hazard_score = metrics.f_factor * 100 + (metrics.tailwind_kts * 2) + metrics.crosswind_kts
        if hazard_score < min_hazard_score:
            min_hazard_score = hazard_score
            best_runway = (rwy_id, metrics)
            
    print("=" * 74)
    print(f"🎯 OPTIMAL RUNWAY SELECTION: Runway {best_runway[0]}")
    print(f"   Headwind: {best_runway[1].headwind_kts} kts | Crosswind: {best_runway[1].crosswind_kts} kts ({best_runway[1].crosswind_direction})")
    print(f"   F-Factor: {best_runway[1].f_factor} | Status: {best_runway[1].hazard_level}")
    print("=" * 74)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Runway Windshear & Crosswind Vector Engine")
    parser.add_argument("--dir", type=float, default=240, help="Wind Direction (0-360 degrees)")
    parser.add_argument("--spd", type=float, default=22, help="Wind Speed (Knots)")
    parser.add_argument("--gust", type=float, default=36, help="Wind Gust Speed (Knots)")
    parser.add_argument("--aircraft", type=str, default="B777-300ER", choices=list(DEFAULT_FLEET_LIMITS.keys()))
    parser.add_argument("--wet", action="store_true", help="Wet runway flag (reduces crosswind limits)")
    parser.add_argument("--json", action="store_true", help="Output results as JSON")
    
    args = parser.parse_args()
    wind = WindVector(direction=args.dir, speed_kts=args.spd, gust_kts=args.gust)
    
    if args.json:
        results = {}
        for rwy_id, rwy_info in DAMASCUS_RUNWAYS.items():
            res = calculate_runway_components(rwy_info["heading"], wind, aircraft_type=args.aircraft, wet_runway=args.wet)
            results[rwy_id] = asdict(res)
        print(json.dumps(results, indent=2))
    else:
        run_full_aerodrome_analysis(wind, aircraft=args.aircraft, wet=args.wet)
