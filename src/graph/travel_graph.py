from langgraph.graph import StateGraph, START, END

from src.state import TravelState
from src.agents.destination_agent import destination_agent
from src.agents.stay_agent import stay_agent


def build_travel_graph():
    graph = StateGraph(TravelState)

    graph.add_node("destination", destination_agent)
    graph.add_node("stay", stay_agent)

    graph.add_edge(START, "destination")
    graph.add_edge("destination", "stay")
    graph.add_edge("stay", END)

    return graph.compile()