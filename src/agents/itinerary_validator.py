from langchain_core.messages import HumanMessage

from src.schemas.validation import ItineraryValidation
from src.services.llm import get_structured_llm
from src.state import TravelState


def build_validation_prompt(state: TravelState) -> str:
    return f"""
You are an itinerary validation assistant.

Validate the generated travel itinerary against the original travel
request and the available research.

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

GENERATED ITINERARY

{state.get("itinerary", {})}

VALIDATION RULES

1. The itinerary must contain exactly the requested number of days.
2. Activities should come from the researched activity results.
3. Restaurants should come from the researched restaurant results.
4. Do not accept invented attractions or restaurants.
5. The itinerary should not be unnecessarily overcrowded.
6. Outdoor activities should consider the available weather information.
7. The itinerary should be consistent with the traveler's preferences.
8. Budget information should not contain unsupported factual claims.
9. Each itinerary item should contain a day, time, activity, location,
   and description.
10. If information required for validation is unavailable, do not assume
    that it is valid. Mention the limitation in the feedback.

Return:
- is_valid: true only when the itinerary satisfies the validation rules.
- issues: a list of specific problems found.
- feedback: concise guidance explaining why the itinerary is valid or
  what should be improved.

Return a structured itinerary validation.
"""


def itinerary_validator(state: TravelState) -> TravelState:
    structured_llm = get_structured_llm(ItineraryValidation)

    prompt = build_validation_prompt(state)

    user_message = HumanMessage(
        content=prompt
    )

    response = structured_llm.invoke(
        [user_message]
    )

    return {
        "validation": response.model_dump(),
        "validation_attempts": state.get("validation_attempts", 0) + 1,
    }