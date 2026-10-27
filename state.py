"""Shared state that every agent reads from and writes to."""
import operator
from typing import Annotated, TypedDict


class TripState(TypedDict, total=False):
    request: str                 # raw user request
    trip_details: dict           # destination, origin, days, people, budget, interests
    research_notes: str          # from Destination Researcher
    sources: list                # links used by the researcher
    weather: dict                # from Weather Agent
    budget_breakdown: dict       # from Budget Planner
    itinerary: str               # from Itinerary Builder
    critic_feedback: str         # from Critic
    approved: bool               # Critic decision
    iterations: int              # how many times the itinerary was built
    # Reducer: parallel agents can all append log lines safely.
    agent_log: Annotated[list, operator.add]
