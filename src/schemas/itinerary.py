from pydantic import BaseModel


class ItineraryItem(BaseModel):
    day: int
    time: str
    activity: str
    location: str
    description: str


class ItineraryAnalysis(BaseModel):
    itinerary: list[ItineraryItem]
    total_days: int
    budget_assessment: str
    planning_notes: list[str]