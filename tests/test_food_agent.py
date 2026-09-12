from src.agents.food_agent import food_agent


def test_food_agent():
    state = {
        "destination": "Mumbai",
        "duration": 3,
        "travelers": 2,
        "budget": 30000,
        "preferences": ["food", "culture"],
    }

    result = food_agent(state)

    assert "restaurants" in result
    assert result["restaurants"]