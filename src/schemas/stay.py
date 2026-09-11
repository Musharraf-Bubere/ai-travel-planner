from pydantic import BaseModel


class Accommodation(BaseModel):
    name: str
    area: str
    price_per_night: float
    rating: float
    description: str


class StayAnalysis(BaseModel):
    recommended_area: str
    accommodation_options: list[Accommodation]
    budget_assessment: str
    stay_recommendation: str