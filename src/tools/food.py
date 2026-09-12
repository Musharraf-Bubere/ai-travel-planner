import os

import requests
from dotenv import load_dotenv
from langchain_core.tools import tool


load_dotenv()


@tool
def search_restaurants(
    destination: str,
    price_level: int = 2,
    limit: int = 5,
) -> list[dict]:
    """Search for restaurants in a destination using SerpApi Google Maps."""

    api_key = os.getenv("SERPAPI_API_KEY")

    if not api_key:
        raise ValueError(
            "SERPAPI_API_KEY is not set in the environment."
        )

    url = "https://serpapi.com/search.json"

    params = {
        "engine": "google_maps",
        "q": f"restaurants in {destination}",
        "api_key": api_key,
        "type": "search",
        "limit": limit,
    }

    response = requests.get(
        url,
        params=params,
        timeout=10,
    )

    response.raise_for_status()

    data = response.json()

    restaurants = []

    for place in data.get("local_results", [])[:limit]:
        restaurants.append(
            {
                "name": place.get("title", "Unknown"),
                "location": place.get("address", destination),
                "category": place.get("type", "Restaurant"),
                "price_level": price_level,
                "rating": place.get("rating", 0.0),
                "distance": place.get("distance", "Not available"),
                "description": place.get(
                    "description",
                    f"Restaurant in {destination}.",
                ),
            }
        )

    return restaurants