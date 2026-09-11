from langchain_core.messages import HumanMessage, ToolMessage

from src.schemas.stay import StayAnalysis
from src.services.llm import get_llm, get_structured_llm
from src.state import TravelState
from src.tools.accommodation import search_accommodations


def build_stay_prompt(state: TravelState) -> str:
    return f"""
You are a travel accommodation research assistant.

Analyze the accommodation requirements for this travel request:

Destination: {state["destination"]}
Duration: {state.get("duration", "Not specified")} days
Travelers: {state.get("travelers", "Not specified")}
Budget: {state.get("budget", "Not specified")}
Preferences: {", ".join(state.get("preferences", []))}

Use the available accommodation search tool to find suitable options.

Evaluate the available options based on:
1. Location
2. Budget
3. Rating
4. Traveler preferences

Provide a practical accommodation recommendation.
"""


def stay_agent(state: TravelState) -> TravelState:
    llm = get_llm()

    llm_with_tools = llm.bind_tools(
        [search_accommodations]
    )

    prompt = build_stay_prompt(state)
    user_message = HumanMessage(content=prompt)

    response = llm_with_tools.invoke(
        [user_message]
    )

    if response.tool_calls:
        tool_call = response.tool_calls[0]

        tool_result = search_accommodations.invoke(
            tool_call["args"]
        )

        tool_message = ToolMessage(
            content=str(tool_result),
            tool_call_id=tool_call["id"],
        )

        structured_llm = get_structured_llm(StayAnalysis)

        final_response = structured_llm.invoke(
            [
                user_message,
                response,
                tool_message,
            ]
        )

        state["stay_options"] = final_response.model_dump()
    else:
        state["stay_options"] = {}

    return state