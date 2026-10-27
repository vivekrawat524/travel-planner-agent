"""Deterministic budget estimator (all figures in INR, rough assumptions)."""
import math

# Per-tier assumptions. Edit these to match your region.
RATES = {
    "budget":  {"room_night": 1000, "food_pp_day": 350,  "local_transport_day": 600,  "activities_pp_day": 150,  "intercity_pp": 400},
    "mid":     {"room_night": 2200, "food_pp_day": 700,  "local_transport_day": 1200, "activities_pp_day": 350,  "intercity_pp": 800},
    "premium": {"room_night": 6000, "food_pp_day": 2000, "local_transport_day": 3000, "activities_pp_day": 1000, "intercity_pp": 2500},
}


def pick_tier(budget: float, people: int, days: int) -> str:
    per_person_day = budget / max(people, 1) / max(days, 1)
    if per_person_day < 1500:
        return "budget"
    if per_person_day < 3500:
        return "mid"
    return "premium"


def estimate_budget(budget: float, people: int, days: int) -> dict:
    people, days = max(int(people), 1), max(int(days), 1)
    tier = pick_tier(budget, people, days)
    r = RATES[tier]
    rooms = math.ceil(people / 2)
    nights = max(days - 1, 1)

    breakdown = {
        "stay": rooms * nights * r["room_night"],
        "food": people * days * r["food_pp_day"],
        "local_transport": days * r["local_transport_day"],
        "activities": people * days * r["activities_pp_day"],
        "intercity_transport": people * r["intercity_pp"],
    }
    subtotal = sum(breakdown.values())
    breakdown["contingency_5pct"] = round(subtotal * 0.05)
    total = subtotal + breakdown["contingency_5pct"]

    return {
        "tier": tier,
        "rooms": rooms,
        "nights": nights,
        "breakdown": breakdown,
        "total": total,
        "budget": budget,
        "within_budget": total <= budget,
        "difference": round(budget - total),  # negative = over budget
    }
