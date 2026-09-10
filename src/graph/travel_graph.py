from langgraph.graph import StateGraph, START, END

from src.state import TravelState
from src.agents.destination_agent import destination_agent


def build_travel_graph():
    graph = StateGraph(TravelState)

    graph.add_node("destination", destination_agent)

    graph.add_edge(START, "destination")
    graph.add_edge("destination", END)

    return graph.compile()