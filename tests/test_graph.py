from src.graph.travel_graph import build_travel_graph


def test_travel_graph():
    graph = build_travel_graph()

    initial_state = {
        "destination": "Goa",
        "duration": 5,
        "travelers": 2,
        "budget": 30000.0,
        "preferences": ["beaches", "adventure"],
    }

    result = graph.invoke(initial_state)

    assert result["destination"] == "Goa"

    # Destination Agent
    assert result["destination_data"]["overview"]
    assert result["destination_data"]["recommended_areas"]
    assert result["destination_data"]["travel_considerations"]
    assert result["destination_data"]["preference_suggestions"]

    # Stay Agent
    assert result["stay_options"]["recommended_area"]
    assert result["stay_options"]["accommodation_options"]
    assert result["stay_options"]["budget_assessment"]
    assert result["stay_options"]["stay_recommendation"]

    # Activity Agent
    assert result["activities"]["recommended_activities"]
    assert result["activities"]["activities_by_category"]
    assert result["activities"]["budget_assessment"]
    assert result["activities"]["activity_recommendation"]