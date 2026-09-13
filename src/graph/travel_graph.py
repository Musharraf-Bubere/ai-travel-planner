from langgraph.graph import StateGraph, START, END

from src.state import TravelState
from src.agents.destination_agent import destination_agent
from src.agents.stay_agent import stay_agent
from src.agents.activity_agent import activity_agent
from src.agents.weather_agent import weather_agent
from src.agents.food_agent import food_agent
from src.agents.itinerary_agent import itinerary_agent
from src.agents.itinerary_validator import itinerary_validator
from src.agents.refine_itinerary import refine_itinerary
from src.agents.final_response_agent import final_response_agent


MAX_VALIDATION_ATTEMPTS = 3


def route_after_validation(state: TravelState) -> str:
    validation = state.get("validation", {})
    attempts = state.get("validation_attempts", 0)

    if validation.get("is_valid", False):
        return "valid"

    if attempts >= MAX_VALIDATION_ATTEMPTS:
        return "valid"

    return "invalid"


def build_travel_graph():
    graph = StateGraph(TravelState)

    graph.add_node("destination", destination_agent)
    graph.add_node("stay", stay_agent)
    graph.add_node("activity", activity_agent)
    graph.add_node("weather", weather_agent)
    graph.add_node("food", food_agent)
    graph.add_node("itinerary", itinerary_agent)
    graph.add_node("validator", itinerary_validator)
    graph.add_node("refine_itinerary", refine_itinerary)
    graph.add_node("final_response", final_response_agent)

    graph.add_edge(START, "destination")

    # Parallel research branches
    graph.add_edge("destination", "stay")
    graph.add_edge("destination", "activity")
    graph.add_edge("destination", "weather")

    # Join parallel branches
    graph.add_edge("stay", "food")
    graph.add_edge("activity", "food")
    graph.add_edge("weather", "food")

    graph.add_edge("food", "itinerary")
    graph.add_edge("itinerary", "validator")

    graph.add_conditional_edges(
        "validator",
        route_after_validation,
        {
            "valid": "final_response",
            "invalid": "refine_itinerary",
        },
    )

    graph.add_edge("refine_itinerary", "validator")
    graph.add_edge("final_response", END)

    return graph.compile()