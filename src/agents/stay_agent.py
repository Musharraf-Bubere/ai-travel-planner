from langchain_core.messages import HumanMessage, ToolMessage
from langchain_core.tools import tool

from src.schemas.stay import StayAnalysis
from src.services.llm import get_llm, get_structured_llm
from src.state import TravelState
from src.mcp_server.client import call_mcp_tool


@tool
def accommodation_search_tool(
    destination: str,
    travel_dates: str,
    duration: int,
    travelers: int,
    budget: float,
    preferences: list[str],
) -> list[dict]:
    """Search real accommodation options through the MCP travel server."""
    return call_mcp_tool(
        "accommodation_search",
        {
            "destination": destination,
            "travel_dates": travel_dates,
            "duration": duration,
            "travelers": travelers,
            "budget": budget,
            "preferences": preferences,
        },
    )


def build_stay_prompt(state: TravelState) -> str:
    return f"""
You are a travel accommodation research assistant.

Analyze the accommodation requirements for this travel request:

Destination: {state["destination"]}
Travel Dates: {state.get("travel_dates", "Not specified")}
Duration: {state.get("duration", "Not specified")} days
Travelers: {state.get("travelers", "Not specified")}
Budget: {state.get("budget", "Not specified")}
Preferences: {", ".join(state.get("preferences", []))}

Use the available accommodation search tool to find suitable
hotel or accommodation options for this exact travel request.

When calling the tool, provide:
- destination
- travel_dates
- duration
- travelers
- budget
- preferences

Evaluate the available options based on:
1. Location
2. Budget
3. Rating
4. Traveler preferences

IMPORTANT DATA-GROUNDING RULES:
1. Use only accommodation options returned by the search tool.
2. Do not invent hotels, prices, ratings, locations, or descriptions.
3. If a field is unavailable in the tool results, clearly state that
   the information is unavailable.
4. Budget assessment must be based only on the retrieved accommodation
   information and the user's stated budget.
5. Recommendations must refer only to retrieved accommodation options.

After receiving the accommodation search results, provide a
practical recommendation.

Return a structured accommodation analysis grounded strictly in
the retrieved tool results.
"""


def stay_agent(state: TravelState) -> TravelState:
    llm = get_llm()

    llm_with_tools = llm.bind_tools(
        [accommodation_search_tool]
    )

    prompt = build_stay_prompt(state)

    user_message = HumanMessage(
        content=prompt
    )

    response = llm_with_tools.invoke(
        [user_message]
    )

    if not response.tool_calls:
        raise ValueError(
            "Stay agent did not call the accommodation search tool."
        )

    tool_call = response.tool_calls[0]

    tool_result = accommodation_search_tool.invoke(
        tool_call["args"]
    )

    tool_message = ToolMessage(
        content=str(tool_result),
        tool_call_id=tool_call["id"],
    )

    structured_llm = get_structured_llm(
        StayAnalysis
    )

    final_response = structured_llm.invoke(
        [
            user_message,
            response,
            tool_message,
        ]
    )

    return {
        "stay_options": final_response.model_dump()
    }