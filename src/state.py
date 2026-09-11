from typing import TypedDict

from src.schemas.destination import DestinationAnalysis


class TravelState(TypedDict, total=False):
    # User input
    destination: str
    travel_dates: str
    duration: int
    travelers: int
    budget: float
    preferences: list[str]

    # Agent outputs
    destination_data: DestinationAnalysis
    stay_options: list[dict]
    activities: list[dict]
    weather: dict
    restaurants: list[dict]
    itinerary: dict