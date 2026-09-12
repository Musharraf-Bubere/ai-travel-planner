from src.agents.weather_agent import weather_agent


def test_weather_agent():
    state = {
        "destination": "Goa",
        "duration": 3,
        "travelers": 2,
        "budget": 15000,
        "preferences": ["beach", "adventure"],
    }

    result = weather_agent(state)

    assert "weather" in result

    weather = result["weather"]

    assert "forecast_summary" in weather
    assert "temperature_summary" in weather
    assert "precipitation_summary" in weather
    assert "travel_assessment" in weather
    assert "weather_recommendation" in weather

    print("\nWeather Analysis:")
    print(weather)