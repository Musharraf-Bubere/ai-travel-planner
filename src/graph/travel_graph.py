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
    """
    Route the workflow based on itinerary validation.

    Routes:

    - valid:
        Validation succeeded.

    - invalid:
        Validation failed but refinement attempts remain.

    - max_attempts:
        Validation is still failing after the maximum number
        of allowed attempts.
    """
    validation = state.get("validation", {})
    attempts = state.get("validation_attempts", 0)

    if validation.get("is_valid", False):
        return "valid"

    if attempts >= MAX_VALIDATION_ATTEMPTS:
        return "max_attempts"

    return "invalid"


def validation_failed(state: TravelState) -> TravelState:
    """
    Handle the case where the itinerary remains invalid after
    the maximum number of validation attempts.

    The workflow does not treat an invalid itinerary as valid.
    Instead, it returns a controlled failure response.
    """
    validation = state.get("validation", {})

    issues = validation.get(
        "issues",
        [],
    )

    return {
        "final_response": {
            "destination": state["destination"],
            "trip_summary": (
                "The itinerary could not be validated successfully "
                "after the maximum number of refinement attempts."
            ),
            "itinerary": state.get(
                "itinerary",
                {},
            ).get(
                "itinerary",
                [],
            ),
            "accommodation_summary": "",
            "food_summary": "",
            "travel_tips": [
                "Please review the itinerary validation issues "
                "before using this travel plan."
            ],
        },
        "validation": {
            "is_valid": False,
            "issues": issues,
            "feedback": (
                "The itinerary remained invalid after the maximum "
                "number of refinement attempts."
            ),
        },
    }


def build_travel_graph():
    graph = StateGraph(TravelState)

    # ------------------------------------------------------------
    # Agents
    # ------------------------------------------------------------

    graph.add_node(
        "destination",
        destination_agent,
    )

    graph.add_node(
        "stay",
        stay_agent,
    )

    graph.add_node(
        "activity",
        activity_agent,
    )

    graph.add_node(
        "weather",
        weather_agent,
    )

    graph.add_node(
        "food",
        food_agent,
    )

    graph.add_node(
        "itinerary",
        itinerary_agent,
    )

    graph.add_node(
        "validator",
        itinerary_validator,
    )

    graph.add_node(
        "refine_itinerary",
        refine_itinerary,
    )

    graph.add_node(
        "final_response",
        final_response_agent,
    )

    graph.add_node(
        "validation_failed",
        validation_failed,
    )

    # ------------------------------------------------------------
    # Start
    # ------------------------------------------------------------

    graph.add_edge(
        START,
        "destination",
    )

    # ------------------------------------------------------------
    # Parallel Research Branches
    # ------------------------------------------------------------

    graph.add_edge(
        "destination",
        "stay",
    )

    graph.add_edge(
        "destination",
        "activity",
    )

    graph.add_edge(
        "destination",
        "weather",
    )

    # ------------------------------------------------------------
    # Parallel Join
    # ------------------------------------------------------------

    graph.add_edge(
        "stay",
        "food",
    )

    graph.add_edge(
        "activity",
        "food",
    )

    graph.add_edge(
        "weather",
        "food",
    )

    # ------------------------------------------------------------
    # Sequential Planning
    # ------------------------------------------------------------

    graph.add_edge(
        "food",
        "itinerary",
    )

    graph.add_edge(
        "itinerary",
        "validator",
    )

    # ------------------------------------------------------------
    # Conditional + Iterative Validation Workflow
    # ------------------------------------------------------------

    graph.add_conditional_edges(
        "validator",
        route_after_validation,
        {
            "valid": "final_response",
            "invalid": "refine_itinerary",
            "max_attempts": "validation_failed",
        },
    )

    # ------------------------------------------------------------
    # Iterative Refinement Loop
    # ------------------------------------------------------------

    graph.add_edge(
        "refine_itinerary",
        "validator",
    )

    # ------------------------------------------------------------
    # Successful Completion
    # ------------------------------------------------------------

    graph.add_edge(
        "final_response",
        END,
    )

    # ------------------------------------------------------------
    # Controlled Validation Failure
    # ------------------------------------------------------------

    graph.add_edge(
        "validation_failed",
        END,
    )

    return graph.compile()