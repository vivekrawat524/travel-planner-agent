"""Web search tool (DuckDuckGo, no API key needed)."""


def web_search(query: str, max_results: int = 5) -> list[dict]:
    """Return a list of {title, body, href}. Returns [] on any failure."""
    try:
        try:
            from ddgs import DDGS
        except ImportError:  # older package name
            from duckduckgo_search import DDGS
        results = DDGS().text(query, max_results=max_results)
        return [
            {"title": r.get("title", ""), "body": r.get("body", ""), "href": r.get("href", "")}
            for r in results or []
        ]
    except Exception:
        return []
