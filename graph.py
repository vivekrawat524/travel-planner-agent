"""LangGraph workflow.

supervisor -> [researcher | weather | budget] (parallel) -> itinerary -> critic
                                                              ^             |
                                                              +--- retry ---+
"""
from langgraph.graph import END, START, StateGraph

from agents.budget import budget_node
from agents.critic import critic_node
from agents.itinerary import itinerary_node
from agents.researcher import researcher_node
from agents.supervisor import supervisor_node
from agents.weather import weather_node
from config import MAX_CRITIC_ITERATIONS
from state import TripState


def route_after_critic(state: TripState) -> str:
    """Loop back for fixes unless approved or the iteration cap is reached."""
    if state.get("approved") or state.get("iterations", 0) >= MAX_CRITIC_ITERATIONS:
        return END
    return "itinerary"


def build_graph():
    g = StateGraph(TripState)
    g.add_node("supervisor", supervisor_node)
    g.add_node("researcher", researcher_node)
    g.add_node("weather", weather_node)
    g.add_node("budget", budget_node)
    g.add_node("itinerary", itinerary_node)
    g.add_node("critic", critic_node)

    g.add_edge(START, "supervisor")
    for worker in ("researcher", "weather", "budget"):  # fan-out (parallel)
        g.add_edge("supervisor", worker)
    g.add_edge(["researcher", "weather", "budget"], "itinerary")  # fan-in (waits for all three)
    g.add_edge("itinerary", "critic")
    g.add_conditional_edges("critic", route_after_critic, {"itinerary": "itinerary", END: END})
    return g.compile()


def plan_trip(request: str) -> dict:
    """Run the whole workflow and return the final state."""
    return build_graph().invoke({"request": request, "agent_log": []})
