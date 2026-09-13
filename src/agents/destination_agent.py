from langchain_core.messages import HumanMessage, ToolMessage

from src.schemas.destination import DestinationAnalysis
from src.services.llm import get_llm, get_structured_llm
from src.state import TravelState
from src.tools.destination import search_destination


def build_destination_prompt(state: TravelState) -> str:
    return f"""
You are a travel destination research assistant.

Analyze the following travel request:

Destination: {state["destination"]}
Duration: {state.get("duration", "Not specified")} days
Travelers: {state.get("travelers", "Not specified")}
Budget: {state.get("budget", "Not specified")}
Preferences: {", ".join(state.get("preferences", []))}

Use the available destination research tool to retrieve relevant
information about the destination.

Evaluate the research based on:
1. Destination suitability
2. Recommended areas
3. Important travel considerations
4. Traveler preferences

Use the retrieved research information to provide practical,
preference-aware destination recommendations.

Return a structured destination analysis.
"""


def destination_agent(state: TravelState) -> TravelState:
    llm = get_llm()

    llm_with_tools = llm.bind_tools(
        [search_destination]
    )

    prompt = build_destination_prompt(state)
    user_message = HumanMessage(content=prompt)

    response = llm_with_tools.invoke(
        [user_message]
    )

    if response.tool_calls:
        tool_call = response.tool_calls[0]

        tool_result = search_destination.invoke(
            tool_call["args"]
        )

        tool_message = ToolMessage(
            content=str(tool_result),
            tool_call_id=tool_call["id"],
        )

        structured_llm = get_structured_llm(
            DestinationAnalysis
        )

        final_response = structured_llm.invoke(
            [
                user_message,
                response,
                tool_message,
            ]
        )

        state["destination_data"] = final_response.model_dump()

    return state