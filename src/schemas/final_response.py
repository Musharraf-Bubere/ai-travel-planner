from pydantic import BaseModel


class FinalResponse(BaseModel):
    destination: str
    trip_summary: str
    itinerary: list[dict]
    accommodation_summary: str
    food_summary: str
    travel_tips: list[str]