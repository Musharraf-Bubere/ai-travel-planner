from langchain_core.messages import HumanMessage

from src.schemas.itinerary import ItineraryAnalysis
from src.services.llm import get_structured_llm
from src.state import TravelState


def build_refinement_prompt(state: TravelState) -> str:
    validation = state.get("validation", {})
    itinerary = state.get("itinerary", {})

    return f"""
You are a travel itinerary refinement assistant.

Improve the generated itinerary based on the validation feedback.

ORIGINAL TRAVEL REQUEST

Destination: {state["destination"]}
Travel Dates: {state.get("travel_dates", "Not specified")}
Duration: {state.get("duration", "Not specified")} days
Travelers: {state.get("travelers", "Not specified")}
Budget: {state.get("budget", "Not specified")}
Preferences: {", ".join(state.get("preferences", []))}

AVAILABLE RESEARCH

Destination:
{state.get("destination_data", {})}

Accommodation:
{state.get("stay_options", {})}

Activities:
{state.get("activities", {})}

Weather:
{state.get("weather", {})}

Restaurants:
{state.get("restaurants", {})}

CURRENT ITINERARY

{itinerary}

VALIDATION RESULT

{validation}

REFINEMENT RULES

1. Fix every issue identified by the validator where possible.
2. Keep exactly the requested number of days.
3. Use only activities present in the researched activity results.
4. Use only restaurants present in the researched restaurant results.
5. Do not invent attractions, restaurants, prices, locations, or other
   factual information.
6. Respect the traveler's preferences.
7. Consider available weather information.
8. Avoid unnecessarily overcrowding the itinerary.
9. Preserve valid parts of the existing itinerary when appropriate.
10. If information is unavailable, explicitly state that it is unavailable
    instead of guessing.

Return the complete improved itinerary as a structured itinerary analysis.
"""


def refine_itinerary(state: TravelState) -> TravelState:
    structured_llm = get_structured_llm(
        ItineraryAnalysis
    )

    prompt = build_refinement_prompt(state)

    user_message = HumanMessage(
        content=prompt
    )

    response = structured_llm.invoke(
        [user_message]
    )

    return {
        "itinerary": response.model_dump()
    }