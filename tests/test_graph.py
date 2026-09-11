from src.graph.travel_graph import build_travel_graph


def test_travel_graph():
    graph = build_travel_graph()

    initial_state = {
        "destination": "Goa",
        "duration": 5,
        "travelers": 2,
        "budget": 30000.0,
        "preferences": ["beaches", "local food"],
    }

    result = graph.invoke(initial_state)

    assert result["destination"] == "Goa"
    assert result["destination_data"]["overview"]
    assert result["destination_data"]["recommended_areas"]
    assert result["destination_data"]["travel_considerations"]
    assert result["destination_data"]["preference_suggestions"]