from src.schemas.weather import WeatherAnalysis


def test_weather_analysis():
    weather = WeatherAnalysis(
        forecast_summary="Generally warm with occasional rain.",
        temperature_summary="Temperatures range from 25°C to 31°C.",
        precipitation_summary="Moderate chance of rain on some days.",
        travel_assessment="Outdoor activities are suitable on clearer days.",
        weather_recommendation="Carry light rain protection and keep the itinerary flexible.",
    )

    assert weather.forecast_summary
    assert weather.temperature_summary
    assert weather.precipitation_summary
    assert weather.travel_assessment
    assert weather.weather_recommendation