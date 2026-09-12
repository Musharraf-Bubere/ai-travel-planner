from typing import TypedDict

from src.schemas.destination import DestinationAnalysis
from src.schemas.stay import StayAnalysis
from src.schemas.activity import ActivityAnalysis
from src.schemas.weather import WeatherAnalysis


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
    activities: ActivityAnalysis
    weather: WeatherAnalysis
    restaurants: list[dict]
    itinerary: dict