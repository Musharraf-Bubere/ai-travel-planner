import os

import requests
from dotenv import load_dotenv
from langchain_core.tools import tool


load_dotenv()


@tool
def search_weather(
    destination: str,
    duration: int,
) -> list[dict]:
    """Retrieve forecast weather information for a destination."""

    api_key = os.getenv("WEATHER_API_KEY")

    if not api_key:
        raise ValueError("WEATHER_API_KEY is not set in the environment.")

    url = "https://api.weatherapi.com/v1/forecast.json"

    params = {
        "key": api_key,
        "q": destination,
        "days": duration,
        "aqi": "no",
        "alerts": "no",
    }

    response = requests.get(
        url,
        params=params,
        timeout=10,
    )

    response.raise_for_status()

    data = response.json()

    forecast = []

    for day in data["forecast"]["forecastday"]:
        forecast.append(
            {
                "date": day["date"],
                "temperature_c": day["day"]["avgtemp_c"],
                "max_temperature_c": day["day"]["maxtemp_c"],
                "min_temperature_c": day["day"]["mintemp_c"],
                "condition": day["day"]["condition"]["text"],
                "rain_probability": day["day"]["daily_chance_of_rain"],
                "precipitation_mm": day["day"]["totalprecip_mm"],
                "max_wind_kph": day["day"]["maxwind_kph"],
            }
        )

    return forecast