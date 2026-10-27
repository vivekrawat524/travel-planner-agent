"""Weather Agent: forecast + simple packing advice (rule-based, no LLM needed)."""
from tools import weather_api


def weather_node(state: dict) -> dict:
    d = state["trip_details"]
    result = weather_api.get_forecast(d["destination"], d["days"])

    if "error" in result:
        weather = {"available": False, "summary": result["error"], "advice": []}
        msg = f"Weather unavailable: {result['error']}"
    else:
        daily = result["daily"]
        advice = []
        if max(x["rain_chance"] or 0 for x in daily) >= 50:
            advice.append("Carry rain gear - high chance of rain on at least one day.")
        if min(x["min_c"] for x in daily) <= 10:
            advice.append("Pack warm layers - nights are cold.")
        if max(x["max_c"] for x in daily) >= 32:
            advice.append("Hot days expected - plan outdoor activities early morning or evening.")
        weather = {"available": True, "city": result["city"], "daily": daily, "advice": advice}
        msg = f"Forecast loaded for {len(daily)} days"

    return {"weather": weather, "agent_log": [{"agent": "Weather Agent", "message": msg}]}
