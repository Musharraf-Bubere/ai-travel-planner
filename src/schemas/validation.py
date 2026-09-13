from pydantic import BaseModel


class ItineraryValidation(BaseModel):
    is_valid: bool
    issues: list[str]
    feedback: str