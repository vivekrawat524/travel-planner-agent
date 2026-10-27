"""End-to-end graph test with the LLM, search and weather API stubbed out."""
import llm
from graph import build_graph
from tools import search, weather_api


def fake_ask_factory(critic_replies):
    replies = iter(critic_replies)

    def fake_ask(system, user):
        if "Supervisor" in system:
            return '{"destination": "Mussoorie", "origin": "Dehradun", "days": 2, "people": 3, "budget": 15000, "interests": ["nature"]}'
        if "itinerary builder" in system:
            return "## Day 1 - Arrival\nMorning...\n## Day 2 - Nature\nMorning..."
        if "travel-plan critic" in system:
            return next(replies)
        return "research notes"

    return fake_ask


def patch_all(monkeypatch, critic_replies):
    monkeypatch.setattr(llm, "ask", fake_ask_factory(critic_replies))
    monkeypatch.setattr(search, "web_search", lambda q, max_results=5: [{"title": "t", "body": "b", "href": "http://x"}])
    monkeypatch.setattr(
        weather_api,
        "get_forecast",
        lambda city, days=5: {"city": city, "daily": [{"date": "2026-11-01", "max_c": 20, "min_c": 8, "rain_chance": 60}] * days},
    )


def test_happy_path_runs_all_agents(monkeypatch):
    patch_all(monkeypatch, ['{"approved": true, "feedback": ""}'])
    final = build_graph().invoke({"request": "trip", "agent_log": []})
    agents_run = {e["agent"] for e in final["agent_log"]}
    assert {"Supervisor", "Destination Researcher", "Weather Agent", "Budget Planner", "Itinerary Builder", "Critic"} <= agents_run
    assert final["approved"] is True
    assert final["iterations"] == 1
    assert "Day 2" in final["itinerary"]


def test_critic_loop_is_capped(monkeypatch):
    # Critic rejects every time -> loop must stop at MAX_CRITIC_ITERATIONS (2).
    patch_all(monkeypatch, ['{"approved": false, "feedback": "too rushed"}'] * 5)
    final = build_graph().invoke({"request": "trip", "agent_log": []})
    assert final["iterations"] == 2
    assert final["approved"] is False


def test_missing_day_triggers_retry(monkeypatch):
    patch_all(monkeypatch, ['{"approved": true, "feedback": ""}'] * 3)
    # Builder only ever returns Day 1 for a 2-day trip -> rule-based critic must reject.
    base = llm.ask
    monkeypatch.setattr(llm, "ask", lambda s, u: "## Day 1 - only" if "itinerary builder" in s else base(s, u))
    final = build_graph().invoke({"request": "trip", "agent_log": []})
    assert final["iterations"] == 2
    assert "Missing day" in final["critic_feedback"]
