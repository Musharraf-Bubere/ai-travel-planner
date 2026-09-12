from src.schemas.food import FoodAnalysis, Restaurant


def test_food_analysis():
    restaurant = Restaurant(
        name="Test Restaurant",
        location="Bandra",
        category="Indian",
        price_level=2,
        rating=4.5,
        distance="1.2 km",
        description="A good local restaurant.",
    )

    food = FoodAnalysis(
        recommended_restaurants=[restaurant],
        restaurants_by_category={
            "Indian": ["Test Restaurant"]
        },
        budget_assessment="Suitable for a moderate budget.",
        food_recommendation="Good option for local Indian food.",
    )

    assert food.recommended_restaurants[0].name == "Test Restaurant"
    assert food.recommended_restaurants[0].rating == 4.5
    assert food.restaurants_by_category["Indian"] == ["Test Restaurant"]