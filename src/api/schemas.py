from pydantic import BaseModel, Field

from src.schemas.final_response import FinalResponse


class TravelRequest(BaseModel):
    destination: str = Field(
        min_length=1,
        description="Travel destination.",
    )

    travel_dates: str = Field(
        min_length=1,
        description="Travel dates in the format YYYY-MM-DD to YYYY-MM-DD.",
    )

    duration: int = Field(
        gt=0,
        description="Trip duration in days.",
    )

    travelers: int = Field(
        gt=0,
        description="Number of travelers.",
    )

    budget: float = Field(
        gt=0,
        description="Total trip budget.",
    )

    preferences: list[str] = Field(
        default_factory=list,
        description="Traveler preferences.",
    )


class TravelPlanResponse(BaseModel):
    destination: str
    travel_dates: str
    validation: dict
    validation_attempts: int
    final_response: FinalResponse