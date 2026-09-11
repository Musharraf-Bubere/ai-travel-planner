from pydantic import BaseModel


class Activity(BaseModel):
    name: str
    location: str
    category: str
    estimated_cost: float
    duration: str
    description: str


class ActivityAnalysis(BaseModel):
    recommended_activities: list[Activity]
    activities_by_category: dict[str, list[str]]
    budget_assessment: str
    activity_recommendation: str