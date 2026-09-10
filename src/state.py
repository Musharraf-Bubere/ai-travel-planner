from typing import TypedDict


class TravelState(TypedDict, total=False):
    # User input
    destination: str
    travel_dates: str
    duration: int
    travelers: int
    budget: float
    preferences: list[str]

    # Agent outputs
    destination_data: dict
    stay_options: list[dict]
    activities: list[dict]
    weather: dict
    restaurants: list[dict]
    itinerary: dict