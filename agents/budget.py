"""Budget Planner: deterministic estimate (tools/budget_calc) checked against the user's budget."""
from tools.budget_calc import estimate_budget


def budget_node(state: dict) -> dict:
    d = state["trip_details"]
    result = estimate_budget(d["budget"], d["people"], d["days"])

    if result["within_budget"]:
        msg = f"Estimated Rs {result['total']:,} - within budget by Rs {result['difference']:,}"
    else:
        msg = f"Estimated Rs {result['total']:,} - OVER budget by Rs {-result['difference']:,}"

    return {"budget_breakdown": result, "agent_log": [{"agent": "Budget Planner", "message": msg}]}
