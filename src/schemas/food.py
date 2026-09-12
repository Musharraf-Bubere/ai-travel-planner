from pydantic import BaseModel


class Restaurant(BaseModel):
    name: str
    location: str
    category: str
    price_level: int
    rating: float
    distance: str
    description: str


class FoodAnalysis(BaseModel):
    recommended_restaurants: list[Restaurant]
    restaurants_by_category: dict[str, list[str]]
    budget_assessment: str
    food_recommendation: str