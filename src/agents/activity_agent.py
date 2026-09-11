from langchain_core.messages import HumanMessage, ToolMessage

from src.schemas.activity import ActivityAnalysis
from src.services.llm import get_llm, get_structured_llm
from src.state import TravelState
from src.tools.activity import search_activities


def build_activity_prompt(state: TravelState) -> str:
    return f"""
You are a travel activity research assistant.

Analyze the activity requirements for this travel request:

Destination: {state["destination"]}
Duration: {state.get("duration", "Not specified")} days
Travelers: {state.get("travelers", "Not specified")}
Budget: {state.get("budget", "Not specified")}
Preferences: {", ".join(state.get("preferences", []))}

Use the available activity search tool to find suitable activities.

Evaluate the available activities based on:
1. Traveler preferences
2. Budget
3. Duration
4. Activity category
5. Location

Recommend activities that provide a practical and enjoyable experience for the traveler.

Return a structured activity analysis.
"""


def activity_agent(state: TravelState) -> TravelState:
    llm = get_llm()

    llm_with_tools = llm.bind_tools(
        [search_activities]
    )

    prompt = build_activity_prompt(state)
    user_message = HumanMessage(content=prompt)

    response = llm_with_tools.invoke(
        [user_message]
    )

    if response.tool_calls:
        tool_call = response.tool_calls[0]

        tool_result = search_activities.invoke(
            tool_call["args"]
        )

        tool_message = ToolMessage(
            content=str(tool_result),
            tool_call_id=tool_call["id"],
        )

        structured_llm = get_structured_llm(ActivityAnalysis)

        final_response = structured_llm.invoke(
            [
                user_message,
                response,
                tool_message,
            ]
        )

        state["activities"] = final_response.model_dump()
    else:
        state["activities"] = {}

    return state