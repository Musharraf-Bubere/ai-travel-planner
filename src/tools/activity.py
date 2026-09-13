import os

import requests
from dotenv import load_dotenv
from langchain_core.tools import tool


load_dotenv()


@tool
def search_activities(
    destination: str,
    preferences: list[str],
    limit: int = 8,
) -> list[dict]:
    """Search real activities and attractions using SerpApi Google Maps."""

    api_key = os.getenv("SERPAPI_API_KEY")

    if not api_key:
        raise ValueError(
            "SERPAPI_API_KEY is not set in the environment."
        )

    preference_text = ", ".join(preferences)

    query = (
        f"things to do, activities, attractions, and experiences "
        f"in {destination}"
    )

    if preference_text:
        query += f" for {preference_text}"

    url = "https://serpapi.com/search.json"

    params = {
        "engine": "google_maps",
        "q": query,
        "api_key": api_key,
        "type": "search",
        "limit": limit,
        "hl": "en",
        "gl": "in",
    }

    response = requests.get(
        url,
        params=params,
        timeout=20,
    )

    response.raise_for_status()

    data = response.json()

    activities = []

    for place in data.get("local_results", [])[:limit]:
        activities.append(
            {
                "name": place.get(
                    "title",
                    "Unknown",
                ),
                "location": place.get(
                    "address",
                    destination,
                ),
                "category": place.get(
                    "type",
                    "Attraction",
                ),
                "estimated_cost": 0.0,
                "duration": "Not available",
                "description": place.get(
                    "description",
                    f"Activity or attraction in {destination}.",
                ),
            }
        )

    return activities