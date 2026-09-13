from src.tools.accommodation import search_accommodations


def test_search_accommodations():
    result = search_accommodations.invoke(
        {
            "destination": "Goa, India",
            "travel_dates": "2026-10-10 to 2026-10-12",
            "duration": 2,
            "travelers": 2,
            "budget": 50000,
            "preferences": ["beaches", "food"],
        }
    )

    assert isinstance(result, list)
    assert len(result) > 0

    first_result = result[0]

    assert "name" in first_result
    assert "area" in first_result
    assert "price_per_night" in first_result
    assert "rating" in first_result
    assert "description" in first_result