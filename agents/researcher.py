"""Destination Researcher: web search + LLM summary of places, food and hidden gems."""
import llm
from tools import search as search_tool

SYSTEM = """You are a destination researcher for a travel team.
Using the search snippets (and your own knowledge if snippets are thin), write concise notes:
- 5-7 attractions (name + one line each)
- 3-4 food / cafe spots
- 2-3 hidden gems
Tailor to the traveller's interests. Do not invent prices. Keep it under 300 words."""


def researcher_node(state: dict) -> dict:
    d = state["trip_details"]
    dest, interests = d["destination"], ", ".join(d.get("interests", []))

    queries = [
        f"top attractions in {dest}",
        f"best cafes and local food in {dest}",
        f"hidden gems offbeat places {dest} {interests}".strip(),
    ]
    snippets, sources = [], []
    for q in queries:
        for r in search_tool.web_search(q, max_results=4):
            snippets.append(f"- {r['title']}: {r['body']}")
            if r["href"] and r["href"] not in sources:
                sources.append(r["href"])

    try:
        notes = llm.ask(
            SYSTEM,
            f"Destination: {dest}\nInterests: {interests or 'general'}\n\nSearch snippets:\n"
            + ("\n".join(snippets) if snippets else "(search returned nothing - use your own knowledge)"),
        )
    except Exception as exc:
        notes = f"Research unavailable ({exc}). Build the itinerary from general knowledge."

    status = f"Found {len(sources)} sources" if sources else "Search returned nothing, used model knowledge"
    return {
        "research_notes": notes,
        "sources": sources[:8],
        "agent_log": [{"agent": "Destination Researcher", "message": status}],
    }
