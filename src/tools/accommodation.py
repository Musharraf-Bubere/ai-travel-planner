from langchain_core.tools import tool


@tool
def search_accommodations(
    destination: str,
    budget: float,
) -> list[dict]:
    """Search accommodation options for a destination within a nightly budget."""

    return [
        {
            "name": "Goa Beach Resort",
            "area": "Candolim",
            "price_per_night": 4500,
            "rating": 4.3,
            "description": "Beachside resort suitable for couples and families.",
        },
        {
            "name": "Anjuna Stay",
            "area": "Anjuna",
            "price_per_night": 3500,
            "rating": 4.1,
            "description": "Comfortable stay close to beaches and local restaurants.",
        },
        {
            "name": "Palolem Retreat",
            "area": "Palolem",
            "price_per_night": 3000,
            "rating": 4.0,
            "description": "Relaxed accommodation near Palolem Beach.",
        },
    ]