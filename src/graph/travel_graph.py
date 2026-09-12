from langgraph.graph import StateGraph, START, END

from src.state import TravelState
from src.agents.destination_agent import destination_agent
from src.agents.stay_agent import stay_agent
from src.agents.activity_agent import activity_agent
from src.agents.weather_agent import weather_agent
from src.agents.food_agent import food_agent


def build_travel_graph():
    graph = StateGraph(TravelState)

    graph.add_node("destination", destination_agent)
    graph.add_node("stay", stay_agent)
    graph.add_node("activity", activity_agent)
    graph.add_node("weather", weather_agent)
    graph.add_node("food", food_agent)

    graph.add_edge(START, "destination")
    graph.add_edge("destination", "stay")
    graph.add_edge("stay", "activity")
    graph.add_edge("activity", "weather")
    graph.add_edge("weather", "food")
    graph.add_edge("food", END)

    return graph.compile()