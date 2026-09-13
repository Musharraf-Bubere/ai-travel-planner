from langchain_core.messages import HumanMessage

from src.schemas.itinerary import ItineraryAnalysis
from src.services.llm import get_structured_llm
from src.state import TravelState


def build_itinerary_prompt(state: TravelState) -> str:
    return f"""
You are a travel itinerary planning assistant.

Create a practical day-by-day itinerary using ONLY the information
available in the provided travel research.

TRAVEL REQUEST
Destination: {state["destination"]}
Travel Dates: {state.get("travel_dates", "Not specified")}
Duration: {state.get("duration", "Not specified")} days
Travelers: {state.get("travelers", "Not specified")}
Budget: {state.get("budget", "Not specified")}
Preferences: {", ".join(state.get("preferences", []))}

DESTINATION RESEARCH
{state.get("destination_data", {})}

ACCOMMODATION OPTIONS
{state.get("stay_options", {})}

ACTIVITIES
{state.get("activities", {})}

WEATHER
{state.get("weather", {})}

RESTAURANTS
{state.get("restaurants", {})}

ITINERARY RULES

1. Create an itinerary for exactly the requested number of days.
2. Use only activities and restaurants present in the provided research.
3. Do not invent attractions, restaurants, prices, locations, or other
   factual information.
4. Consider the traveler's preferences when selecting activities.
5. Consider weather information when planning outdoor activities.
6. Group activities logically by location where possible.
7. Include appropriate time slots such as Morning, Afternoon, and Evening.
8. Use restaurants from the provided restaurant research for food-related
   itinerary items.
9. Keep the itinerary practical rather than overcrowded.
10. If information is unavailable, explicitly state that it is unavailable
    instead of guessing.
11. Do not create additional places that are not present in the research.

For each itinerary item provide:
- day
- time
- activity
- location
- description

Also provide:
- total_days
- budget_assessment
- planning_notes

Return a structured itinerary analysis.
"""


def itinerary_agent(state: TravelState) -> TravelState:
    structured_llm = get_structured_llm(
        ItineraryAnalysis
    )

    prompt = build_itinerary_prompt(state)

    user_message = HumanMessage(
        content=prompt
    )

    response = structured_llm.invoke(
        [user_message]
    )

    state["itinerary"] = response.model_dump()

    return state