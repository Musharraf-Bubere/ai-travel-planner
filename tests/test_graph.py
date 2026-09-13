from src.graph.travel_graph import build_travel_graph


def test_graph_compiles():
    graph = build_travel_graph()

    assert graph is not None


def test_parallel_workflow_structure():
    graph = build_travel_graph()

    graph_structure = graph.get_graph()

    assert "destination" in graph_structure.nodes
    assert "stay" in graph_structure.nodes
    assert "activity" in graph_structure.nodes
    assert "weather" in graph_structure.nodes
    assert "food" in graph_structure.nodes
    assert "itinerary" in graph_structure.nodes
    assert "validator" in graph_structure.nodes
    assert "refine_itinerary" in graph_structure.nodes
    assert "final_response" in graph_structure.nodes

    destination_edges = [
        edge
        for edge in graph_structure.edges
        if edge.source == "destination"
    ]

    assert {edge.target for edge in destination_edges} == {
        "stay",
        "activity",
        "weather",
    }

    food_edges = [
        edge
        for edge in graph_structure.edges
        if edge.target == "food"
    ]

    assert {edge.source for edge in food_edges} == {
        "stay",
        "activity",
        "weather",
    }


def test_route_after_validation_valid():
    from src.graph.travel_graph import route_after_validation

    state = {
        "validation": {
            "is_valid": True,
        },
        "validation_attempts": 1,
    }

    assert route_after_validation(state) == "valid"


def test_route_after_validation_invalid_with_attempts_remaining():
    from src.graph.travel_graph import route_after_validation

    state = {
        "validation": {
            "is_valid": False,
        },
        "validation_attempts": 1,
    }

    assert route_after_validation(state) == "invalid"


def test_route_after_validation_stops_at_max_attempts():
    from src.graph.travel_graph import route_after_validation

    state = {
        "validation": {
            "is_valid": False,
        },
        "validation_attempts": 3,
    }

    assert route_after_validation(state) == "valid"


def test_final_response_workflow_structure():
    graph = build_travel_graph()

    graph_structure = graph.get_graph()

    assert "final_response" in graph_structure.nodes

    final_response_edges = [
        edge
        for edge in graph_structure.edges
        if edge.source == "final_response"
    ]

    assert any(
        edge.target == "__end__"
        for edge in final_response_edges
    )