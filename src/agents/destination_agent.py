from src.state import TravelState
from src.schemas.destination import DestinationAnalysis
from src.services.llm import get_structured_llm


def build_destination_prompt(state: TravelState) -> str:
    return f"""
You are a travel destination research assistant.

Analyze the following travel request:

Destination: {state["destination"]}
Duration: {state.get("duration", "Not specified")} days
Travelers: {state.get("travelers", "Not specified")}
Budget: {state.get("budget", "Not specified")}
Preferences: {", ".join(state.get("preferences", []))}

Provide a concise destination overview covering:
1. Why the destination is suitable for this trip
2. Recommended areas to explore
3. Important travel considerations
4. Suggestions based on the traveler's preferences
"""


def destination_agent(state: TravelState) -> TravelState:
    structured_llm = get_structured_llm(DestinationAnalysis)

    prompt = build_destination_prompt(state)

    response = structured_llm.invoke(prompt)

    state["destination_data"] = response.model_dump()

    return state