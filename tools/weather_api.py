"""Weather tool using the free Open-Meteo API (no key needed)."""
import requests

GEO_URL = "https://geocoding-api.open-meteo.com/v1/search"
FORECAST_URL = "https://api.open-meteo.com/v1/forecast"


def get_forecast(city: str, days: int = 5) -> dict:
    """Return {'city', 'daily': [...]} or {'error': '...'} if anything fails."""
    days = max(1, min(int(days), 16))
    try:
        geo = requests.get(GEO_URL, params={"name": city, "count": 1}, timeout=10).json()
        if not geo.get("results"):
            return {"error": f"Could not find location '{city}'"}
        place = geo["results"][0]
        data = requests.get(
            FORECAST_URL,
            params={
                "latitude": place["latitude"],
                "longitude": place["longitude"],
                "daily": "temperature_2m_max,temperature_2m_min,precipitation_probability_max",
                "timezone": "auto",
                "forecast_days": days,
            },
            timeout=10,
        ).json()["daily"]
        daily = [
            {
                "date": data["time"][i],
                "max_c": data["temperature_2m_max"][i],
                "min_c": data["temperature_2m_min"][i],
                "rain_chance": data["precipitation_probability_max"][i],
            }
            for i in range(len(data["time"]))
        ]
        return {"city": place["name"], "daily": daily}
    except Exception as exc:
        return {"error": f"Weather service unavailable: {exc}"}
