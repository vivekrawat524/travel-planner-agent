"""Supervisor: turns the free-text request into structured trip details."""
import llm

SYSTEM = """You are the Supervisor of a travel-planning team.
Extract trip details from the user's request and reply with ONLY a JSON object:
{"destination": str, "origin": str, "days": int, "people": int,
 "budget": int (total in INR), "interests": [str]}
Use sensible defaults if something is missing: origin "", days 3, people 2, budget 20000, interests []."""

DEFAULTS = {"destination": "", "origin": "", "days": 3, "people": 2, "budget": 20000, "interests": []}


def supervisor_node(state: dict) -> dict:
    request = state["request"]
    try:
        parsed = llm.extract_json(llm.ask(SYSTEM, request))
    except Exception:
        parsed = {}

    details = {**DEFAULTS, **{k: v for k, v in parsed.items() if v not in (None, "")}}
    # Coerce numeric fields so downstream tools never crash.
    for key, fallback in (("days", 3), ("people", 2), ("budget", 20000)):
        try:
            details[key] = max(int(details[key]), 1)
        except (TypeError, ValueError):
            details[key] = fallback

    if not details["destination"]:
        details["destination"] = request.strip()[:60]

    msg = (
        f"Planning {details['days']}-day trip to {details['destination']} for "
        f"{details['people']} people, budget Rs {details['budget']:,}."
    )
    return {
        "trip_details": details,
        "iterations": 0,
        "agent_log": [{"agent": "Supervisor", "message": msg}],
    }
