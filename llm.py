"""Thin LLM wrapper so the rest of the code is provider-agnostic."""
import json
import os
import re

from dotenv import load_dotenv

load_dotenv()


def get_llm():
    provider = os.getenv("LLM_PROVIDER", "gemini").lower()
    model = os.getenv("LLM_MODEL") or None

    if provider == "openai":
        from langchain_openai import ChatOpenAI
        return ChatOpenAI(model=model or "gpt-4o-mini", temperature=0.3)
    if provider == "anthropic":
        from langchain_anthropic import ChatAnthropic
        return ChatAnthropic(model=model or "claude-haiku-5-5", temperature=0.3, max_tokens=2000)
    if provider == "gemini":
        from langchain_google_genai import ChatGoogleGenerativeAI
        return ChatGoogleGenerativeAI(model=model or "gemini-2.5-flash", temperature=0.3)
    raise ValueError(f"Unknown LLM_PROVIDER '{provider}'. Use gemini, openai or anthropic.")


def ask(system: str, user: str) -> str:
    """Send a system + user prompt and return the reply as plain text."""
    from langchain_core.messages import HumanMessage, SystemMessage

    reply = get_llm().invoke([SystemMessage(content=system), HumanMessage(content=user)])
    content = reply.content
    if isinstance(content, list):  # some providers return content blocks
        content = "".join(b.get("text", "") if isinstance(b, dict) else str(b) for b in content)
    return content.strip()


def extract_json(text: str) -> dict:
    """Pull the first JSON object out of an LLM reply (handles ```json fences)."""
    text = re.sub(r"```(?:json)?", "", text)
    start, end = text.find("{"), text.rfind("}")
    if start == -1 or end == -1:
        raise ValueError("No JSON object found in LLM reply")
    return json.loads(text[start : end + 1])
