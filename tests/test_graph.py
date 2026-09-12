from src.graph.travel_graph import build_travel_graph


def test_travel_graph():
    graph = build_travel_graph()

    nodes = graph.nodes

    assert "destination" in nodes
    assert "stay" in nodes
    assert "activity" in nodes
    assert "weather" in nodes
    assert "food" in nodes