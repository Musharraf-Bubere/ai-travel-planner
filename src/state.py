from typing import TypedDict

from src.schemas.destination import DestinationAnalysis
from src.schemas.stay import StayAnalysis


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
    stay_options: StayAnalysis
    activities: list[dict]
    weather: dict
    restaurants: list[dict]
    itinerary: dict