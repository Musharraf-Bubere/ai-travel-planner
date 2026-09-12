from src.tools.weather import search_weather


def test_weather_tool_definition():
    assert search_weather.name == "search_weather"
    assert search_weather.description