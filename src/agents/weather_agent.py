from langchain_core.messages import HumanMessage, ToolMessage

from src.services.llm import get_llm
from src.state import TravelState
from src.tools.weather import search_weather
from src.schemas.weather import WeatherAnalysis
from src.services.llm import get_structured_llm


def build_weather_prompt(state: TravelState) -> str:
    return f"""
You are a travel weather research assistant.

Analyze the weather requirements for this travel request:

Destination: {state["destination"]}
Duration: {state.get("duration", "Not specified")} days
Travelers: {state.get("travelers", "Not specified")}
Budget: {state.get("budget", "Not specified")}
Preferences: {", ".join(state.get("preferences", []))}

Use the available weather search tool to retrieve forecast information
for the destination.

Analyze the weather based on:
1. Temperature
2. Precipitation and rain probability
3. Weather conditions
4. Suitability for travel
5. Impact on outdoor activities

Provide practical weather recommendations for the traveler.
"""


def weather_agent(state: TravelState) -> TravelState:
    llm = get_llm()

    llm_with_tools = llm.bind_tools(
        [search_weather]
    )

    prompt = build_weather_prompt(state)
    user_message = HumanMessage(content=prompt)

    response = llm_with_tools.invoke(
        [user_message]
    )

    if response.tool_calls:
        tool_call = response.tool_calls[0]

        tool_result = search_weather.invoke(
            tool_call["args"]
        )

        tool_message = ToolMessage(
            content=str(tool_result),
            tool_call_id=tool_call["id"],
        )

        structured_llm = get_structured_llm(WeatherAnalysis)

        final_response = structured_llm.invoke(
            [
                user_message,
                response,
                tool_message,
            ]
        )

        state["weather"] = final_response.model_dump()

    return state