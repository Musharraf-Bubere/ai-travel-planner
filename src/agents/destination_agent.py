from langchain_core.messages import HumanMessage, ToolMessage
from langchain_core.tools import tool

from src.schemas.destination import DestinationAnalysis
from src.services.llm import get_llm, get_structured_llm
from src.state import TravelState
from src.mcp_server.client import call_mcp_tool


@tool
def destination_research_tool(
    destination: str,
    preferences: list[str],
) -> list[dict]:
    """Research a travel destination using the MCP travel research server."""
    return call_mcp_tool(
        "destination_research",
        {
            "destination": destination,
            "preferences": preferences,
        },
    )


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
        [destination_research_tool]
    )

    prompt = build_destination_prompt(state)
    user_message = HumanMessage(content=prompt)

    response = llm_with_tools.invoke(
        [user_message]
    )

    if not response.tool_calls:
        raise ValueError(
            "Destination agent did not call the destination research tool."
        )

    tool_call = response.tool_calls[0]

    tool_result = destination_research_tool.invoke(
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

    return {
        "destination_data": final_response.model_dump()
    }