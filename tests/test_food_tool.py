from src.tools.food import search_restaurants


def test_search_restaurants_tool():
    assert search_restaurants.name == "search_restaurants"
    assert search_restaurants.description