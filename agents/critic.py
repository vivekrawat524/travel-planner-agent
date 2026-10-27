"""Critic: checks the plan; can send it back to the Itinerary Builder."""
import re

import llm

SYSTEM = """You are a strict travel-plan critic. Check the itinerary for:
1. Every requested day is present.
2. Timings and travel between places are realistic.
3. The plan respects the weather.
4. Budget: if the estimate is OVER budget, approve only if the plan openly acknowledges it and
   gives concrete savings (cheaper stay, shared transport, free activities). Do not demand impossible fixes.
Reply with ONLY JSON: {"approved": true|false, "feedback": "specific fixes, or empty if approved"}"""


def critic_node(state: dict) -> dict:
    d = state["trip_details"]
    plan = state.get("itinerary", "")
    budget = state.get("budget_breakdown", {})
    issues = []

    # Rule-based checks: cheap and reliable, run before the LLM.
    found_days = {int(n) for n in re.findall(r"day\s*(\d+)", plan, flags=re.I)}
    missing = [n for n in range(1, d["days"] + 1) if n not in found_days]
    if missing:
        issues.append(f"Missing day sections: {missing}.")

    # LLM check for qualitative problems.
    try:
        verdict = llm.extract_json(
            llm.ask(SYSTEM, f"Trip: {d}\nBudget estimate: {budget}\n\nItinerary:\n{plan}")
        )
        if not verdict.get("approved", True) and verdict.get("feedback"):
            issues.append(str(verdict["feedback"]))
    except Exception:
        pass  # if the LLM check fails, rely on the rule-based checks

    approved = not issues
    msg = "Approved" if approved else "Needs changes: " + " ".join(issues)[:200]
    return {
        "approved": approved,
        "critic_feedback": " ".join(issues),
        "agent_log": [{"agent": "Critic", "message": msg}],
    }
