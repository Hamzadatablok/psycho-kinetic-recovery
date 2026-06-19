"""
Scientific & decision logic for Psycho-Kinetic Recovery.

Reuses the ACWR / risk functions from earlier projects, and adds the
dual-recovery rule: how to adjust tomorrow's physical load and mental
support based on the athlete's daily pain and mood feedback.

These are deterministic, testable functions — the LLM agents phrase the
plan, but the load/support decision is made here in code.
"""

from typing import List


# ---------- Reused workload science ----------
def compute_acwr(daily_loads: List[float]) -> dict:
    """Compute the Acute:Chronic Workload Ratio (ACWR) and its zone."""
    if len(daily_loads) < 7:
        raise ValueError("At least 7 days are required")

    acute = sum(daily_loads[-7:]) / 7
    chronic_window = daily_loads[-28:]
    chronic = sum(chronic_window) / len(chronic_window)
    acwr = round(acute / chronic, 2) if chronic > 0 else 0.0

    if acwr < 0.80:
        zone = "undertraining"
    elif acwr <= 1.30:
        zone = "sweet_spot"
    else:
        zone = "danger"

    return {"acute_load": round(acute, 1), "chronic_load": round(chronic, 1),
            "acwr": acwr, "acwr_zone": zone}


# ---------- New: dual-recovery decision ----------
def adjust_plan(pain: int, mood: int, current_load: float) -> dict:
    """Decide tomorrow's physical load % and mental-support level.

    Args:
        pain: athlete-reported pain, 0-10 (higher = worse)
        mood: athlete-reported mood,  0-10 (higher = better)
        current_load: today's physical load

    Returns a decision dict the agents will turn into a concrete plan.
    """
    load_factor = 1.0           # 100% of current load by default
    mental_support = "standard"
    reasons: List[str] = []

    # --- Physical adjustment driven by pain ---
    if pain >= 7:
        load_factor = 0.5       # cut load in half
        reasons.append(f"High pain ({pain}/10) -> reduce physical load 50%")
    elif pain >= 4:
        load_factor = 0.75
        reasons.append(f"Moderate pain ({pain}/10) -> reduce physical load 25%")
    else:
        load_factor = 1.1       # safe to progress slightly
        reasons.append(f"Low pain ({pain}/10) -> progress load +10%")

    # --- Mental support driven by mood ---
    if mood <= 3:
        mental_support = "high"
        reasons.append(f"Low mood ({mood}/10) -> increase mental support")
    elif mood <= 6:
        mental_support = "moderate"
        reasons.append(f"Average mood ({mood}/10) -> moderate mental support")
    else:
        mental_support = "light"
        reasons.append(f"Good mood ({mood}/10) -> light mental support")

    # --- Safety override: high pain + low mood = recovery day ---
    recovery_day = pain >= 7 and mood <= 3
    if recovery_day:
        load_factor = 0.0
        reasons.append("High pain AND low mood -> full recovery day, no load")

    return {
        "next_load": round(current_load * load_factor, 1),
        "load_factor": load_factor,
        "mental_support": mental_support,
        "recovery_day": recovery_day,
        "reasons": reasons,
    }
