from pydantic import BaseModel


class WeatherAnalysis(BaseModel):
    forecast_summary: str
    temperature_summary: str
    precipitation_summary: str
    travel_assessment: str
    weather_recommendation: str