from src.state import TravelState


def test_travel_state():
    state: TravelState = {
        "destination": "Goa",
        "travel_dates": "2026-10-10 to 2026-10-14",
        "duration": 5,
        "travelers": 2,
        "budget": 30000.0,
        "preferences": ["beaches", "local food"],
    }

    assert state["destination"] == "Goa"
    assert state["duration"] == 5
    assert state["travelers"] == 2
    assert state["budget"] == 30000.0
    assert "beaches" in state["preferences"]