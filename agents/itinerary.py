"""Itinerary Builder: merges research, weather and budget into a day-by-day plan."""
import json

import llm

SYSTEM = """You are an expert itinerary builder.
Write a day-by-day travel plan in Markdown using the inputs provided.
Rules:
- Exactly one section per day: '## Day N - theme', with Morning / Afternoon / Evening.
- Group nearby places on the same day; keep travel times realistic.
- Use only places from the research notes when possible.
- Respect the weather advice and the budget breakdown (mention rough daily spend).
- If critic feedback is given, fix every issue it lists.
- End with a short 'Budget summary' and 'Packing tips' section."""


def itinerary_node(state: dict) -> dict:
    d = state["trip_details"]
    iteration = state.get("iterations", 0) + 1

    prompt = (
        f"Trip: {json.dumps(d)}\n\n"
        f"Research notes:\n{state.get('research_notes', '')}\n\n"
        f"Weather: {json.dumps(state.get('weather', {}))}\n\n"
        f"Budget breakdown (INR): {json.dumps(state.get('budget_breakdown', {}))}\n\n"
        f"Critic feedback to fix: {state.get('critic_feedback') or 'none (first draft)'}"
    )
    try:
        plan = llm.ask(SYSTEM, prompt)
    except Exception as exc:
        plan = f"Could not generate itinerary: {exc}"

    return {
        "itinerary": plan,
        "iterations": iteration,
        "agent_log": [{"agent": "Itinerary Builder", "message": f"Draft #{iteration} written"}],
    }
