from langchain_core.messages import HumanMessage, ToolMessage

from src.schemas.food import FoodAnalysis
from src.services.llm import get_llm, get_structured_llm
from src.state import TravelState
from src.tools.food import search_restaurants


def build_food_prompt(state: TravelState) -> str:
    return f"""
You are a travel food and restaurant research assistant.

Analyze the food requirements for this travel request:

Destination: {state["destination"]}
Duration: {state.get("duration", "Not specified")} days
Travelers: {state.get("travelers", "Not specified")}
Budget: {state.get("budget", "Not specified")}
Preferences: {", ".join(state.get("preferences", []))}

Use the available restaurant search tool to find suitable restaurants.

IMPORTANT DATA-GROUNDING RULES:
1. Use only restaurants returned by the restaurant search tool.
2. Do not invent restaurant names, ratings, locations, prices,
   distances, categories, or descriptions.
3. Every recommended restaurant must correspond to a restaurant
   returned by the search tool.
4. If a field is unavailable in the tool results, clearly state that
   the information is unavailable.
5. Do not create restaurant recommendations from general knowledge.
6. Budget assessment must be based only on the retrieved restaurant
   information and the user's stated budget.

Evaluate the available restaurants based on:
1. Traveler preferences
2. Budget
3. Restaurant rating
4. Cuisine/category
5. Location
6. Overall suitability for the trip

Recommend restaurants that provide a practical and enjoyable dining
experience for the traveler.

Return a structured food analysis grounded strictly in the
retrieved tool results.
"""


def food_agent(state: TravelState) -> TravelState:
    llm = get_llm()

    llm_with_tools = llm.bind_tools(
        [search_restaurants]
    )

    prompt = build_food_prompt(state)

    user_message = HumanMessage(
        content=prompt
    )

    response = llm_with_tools.invoke(
        [user_message]
    )

    if not response.tool_calls:
        raise ValueError(
            "Food agent did not call the restaurant search tool."
        )

    tool_call = response.tool_calls[0]

    tool_result = search_restaurants.invoke(
        tool_call["args"]
    )

    tool_message = ToolMessage(
        content=str(tool_result),
        tool_call_id=tool_call["id"],
    )

    structured_llm = get_structured_llm(
        FoodAnalysis
    )

    final_response = structured_llm.invoke(
        [
            user_message,
            response,
            tool_message,
        ]
    )

    return {
        "restaurants": final_response.model_dump()
    }