import json

from mcp.server import MCPServer

from src.tools.destination import search_destination
from src.tools.accommodation import search_accommodations
from src.tools.activity import search_activities
from src.tools.weather import search_weather
from src.tools.food import search_restaurants


mcp = MCPServer("ai-travel-planner")


@mcp.tool()
def destination_research(
    destination: str,
    preferences: list[str],
) -> str:
    """Research a travel destination using Tavily web search."""
    result = search_destination.invoke(
        {
            "destination": destination,
            "preferences": preferences,
        }
    )

    return json.dumps(result, ensure_ascii=False)


@mcp.tool()
def accommodation_search(
    destination: str,
    travel_dates: str,
    duration: int,
    travelers: int,
    budget: float,
    preferences: list[str],
) -> str:
    """Search real accommodation options using SerpApi Google Hotels."""
    result = search_accommodations.invoke(
        {
            "destination": destination,
            "travel_dates": travel_dates,
            "duration": duration,
            "travelers": travelers,
            "budget": budget,
            "preferences": preferences,
        }
    )

    return json.dumps(result, ensure_ascii=False)


@mcp.tool()
def activity_search(
    destination: str,
    preferences: list[str],
    limit: int = 8,
) -> str:
    """Search real activities and attractions using SerpApi Google Maps."""
    result = search_activities.invoke(
        {
            "destination": destination,
            "preferences": preferences,
            "limit": limit,
        }
    )

    return json.dumps(result, ensure_ascii=False)


@mcp.tool()
def weather_search(
    destination: str,
    duration: int,
) -> str:
    """Retrieve weather information for a destination."""
    result = search_weather.invoke(
        {
            "destination": destination,
            "duration": duration,
        }
    )

    return json.dumps(result, ensure_ascii=False)


@mcp.tool()
def restaurant_search(
    destination: str,
    price_level: int = 2,
    limit: int = 5,
) -> str:
    """Search restaurants using SerpApi Google Maps."""
    result = search_restaurants.invoke(
        {
            "destination": destination,
            "price_level": price_level,
            "limit": limit,
        }
    )

    return json.dumps(result, ensure_ascii=False)


if __name__ == "__main__":
    mcp.run()