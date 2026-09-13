import os

import requests
from dotenv import load_dotenv
from langchain_core.tools import tool


load_dotenv()


def parse_travel_dates(travel_dates: str) -> tuple[str, str]:
    """Parse travel dates in YYYY-MM-DD to YYYY-MM-DD format."""

    parts = [
        part.strip()
        for part in travel_dates.split("to")
    ]

    if len(parts) != 2:
        raise ValueError(
            "travel_dates must use the format "
            "'YYYY-MM-DD to YYYY-MM-DD'."
        )

    return parts[0], parts[1]


@tool
def search_accommodations(
    destination: str,
    travel_dates: str,
    duration: int,
    travelers: int,
    budget: float,
    preferences: list[str],
) -> list[dict]:
    """Search real accommodation options using SerpApi Google Hotels."""

    api_key = os.getenv("SERPAPI_API_KEY")

    if not api_key:
        raise ValueError(
            "SERPAPI_API_KEY is not set in the environment."
        )

    check_in, check_out = parse_travel_dates(
        travel_dates
    )

    url = "https://serpapi.com/search"

    params = {
        "engine": "google_hotels",
        "q": f"hotels in {destination}",
        "check_in_date": check_in,
        "check_out_date": check_out,
        "adults": travelers,
        "currency": "INR",
        "gl": "in",
        "hl": "en",
        "sort_by": "3",
        "api_key": api_key,
    }

    response = requests.get(
        url,
        params=params,
        timeout=20,
    )

    response.raise_for_status()

    data = response.json()

    accommodations = []

    for property_data in data.get("properties", [])[:10]:
        rate = property_data.get(
            "rate_per_night",
            {}
        )

        price = rate.get(
            "extracted_lowest",
            0.0,
        )

        rating = property_data.get(
            "overall_rating",
            property_data.get(
                "rating",
                0.0,
            ),
        )

        accommodations.append(
            {
                "name": property_data.get(
                    "name",
                    "Unknown",
                ),
                "area": property_data.get(
                    "address",
                    destination,
                ),
                "price_per_night": float(price),
                "rating": float(rating),
                "description": property_data.get(
                    "description",
                    f"Accommodation in {destination}.",
                ),
            }
        )

    return accommodations