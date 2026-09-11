from src.tools.accommodation import search_accommodations


def test_search_accommodations():
    result = search_accommodations.invoke(
        {
            "destination": "Goa",
            "budget": 5000,
        }
    )

    assert result
    assert isinstance(result, list)
    assert result[0]["name"]
    assert result[0]["price_per_night"] <= 5000