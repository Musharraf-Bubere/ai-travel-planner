from langchain_core.tools import tool


@tool
def search_activities(
    destination: str,
    budget: float,
    preferences: list[str],
) -> list[dict]:
    """Search activity options for a destination based on budget and traveler preferences."""

    return [
        {
            "name": "Baga Beach",
            "location": "Baga",
            "category": "Beach",
            "estimated_cost": 0,
            "duration": "2-3 hours",
            "description": "Popular beach suitable for relaxation and water activities.",
        },
        {
            "name": "Scuba Diving",
            "location": "Grande Island",
            "category": "Adventure",
            "estimated_cost": 2500,
            "duration": "Half day",
            "description": "Scuba diving experience suitable for adventure-focused travelers.",
        },
        {
            "name": "Parasailing",
            "location": "Calangute",
            "category": "Adventure",
            "estimated_cost": 1800,
            "duration": "1-2 hours",
            "description": "Adventure water sport offering aerial views of the coastline.",
        },
        {
            "name": "Fort Aguada",
            "location": "Candolim",
            "category": "Culture",
            "estimated_cost": 50,
            "duration": "2 hours",
            "description": "Historic fort offering coastal views and cultural exploration.",
        },
        {
            "name": "Sunset Cruise",
            "location": "Panaji",
            "category": "Experience",
            "estimated_cost": 1200,
            "duration": "2 hours",
            "description": "Relaxing evening cruise with views of the Goan coastline.",
        },
    ]