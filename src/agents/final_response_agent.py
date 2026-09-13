from langchain_core.messages import HumanMessage

from src.schemas.final_response import FinalResponse
from src.services.llm import get_structured_llm
from src.state import TravelState


def build_final_response_prompt(state: TravelState) -> str:
    return f"""
You are the final travel response assistant.

Create a clear, practical, user-facing travel plan from the validated
travel research and itinerary.

TRAVEL REQUEST

Destination: {state["destination"]}
Travel Dates: {state.get("travel_dates", "Not specified")}
Duration: {state.get("duration", "Not specified")} days
Travelers: {state.get("travelers", "Not specified")}
Budget: {state.get("budget", "Not specified")}
Preferences: {", ".join(state.get("preferences", []))}

DESTINATION RESEARCH

{state.get("destination_data", {})}

ACCOMMODATION

{state.get("stay_options", {})}

ACTIVITIES

{state.get("activities", {})}

WEATHER

{state.get("weather", {})}

RESTAURANTS

{state.get("restaurants", {})}

VALIDATED ITINERARY

{state.get("itinerary", {})}

VALIDATION

{state.get("validation", {})}

FINAL RESPONSE RULES

1. Present the validated itinerary clearly and practically.
2. Use only information available in the provided research.
3. Do not invent attractions, restaurants, prices, locations, or other
   factual information.
4. Preserve the validated itinerary rather than creating a new itinerary.
5. Summarize the accommodation recommendation using the available
   accommodation research.
6. Summarize the food recommendations using the available restaurant
   research.
7. Include useful travel tips based only on the available research.
8. If information is unavailable, explicitly state that it is unavailable.
9. Keep the response concise enough for a normal travel-planning response.
10. Do not include internal validation details unless they are useful to
    the traveler.

Return a structured final travel response.
"""


def final_response_agent(state: TravelState) -> TravelState:
    structured_llm = get_structured_llm(
        FinalResponse
    )

    prompt = build_final_response_prompt(state)

    user_message = HumanMessage(
        content=prompt
    )

    response = structured_llm.invoke(
        [user_message]
    )

    return {
        "final_response": response.model_dump()
    }