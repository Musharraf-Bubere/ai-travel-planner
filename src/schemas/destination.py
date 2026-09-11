from pydantic import BaseModel


class DestinationAnalysis(BaseModel):
    overview: str
    recommended_areas: list[str]
    travel_considerations: list[str]
    preference_suggestions: list[str]