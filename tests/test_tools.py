import pytest

from llm import extract_json
from tools.budget_calc import estimate_budget, pick_tier


def test_tier_selection():
    assert pick_tier(5000, 2, 3) == "budget"
    assert pick_tier(20000, 3, 4) == "mid"
    assert pick_tier(100000, 2, 3) == "premium"


def test_budget_totals_add_up():
    r = estimate_budget(15000, 3, 4)
    parts = sum(r["breakdown"].values())
    assert r["total"] == parts
    assert r["rooms"] == 2 and r["nights"] == 3


def test_over_budget_flag():
    assert estimate_budget(1000, 4, 5)["within_budget"] is False
    assert estimate_budget(1_000_000, 2, 3)["within_budget"] is True


def test_extract_json_handles_fences():
    assert extract_json('Sure!\n```json\n{"a": 1}\n```') == {"a": 1}


def test_extract_json_raises_on_garbage():
    with pytest.raises(ValueError):
        extract_json("no json here")
