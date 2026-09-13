from src.agents.itinerary_agent import itinerary_agent


def test_itinerary_agent():
    state = {
        "destination": "Goa, India",
        "travel_dates": "2026-10-10 to 2026-10-12",
        "duration": 2,
        "travelers": 2,
        "budget": 50000,
        "preferences": ["beaches", "adventure", "food"],
        "destination_data": {
            "overview": "Goa is suitable for a beach-focused trip.",
            "recommended_areas": ["Anjuna", "Baga"],
            "travel_considerations": [
                "Plan outdoor activities around weather conditions."
            ],
            "preference_suggestions": ["Beaches", "Adventure", "Food"],
        },
        "stay_options": {
            "recommended_area": "Anjuna/Baga",
            "accommodation_options": [
                {
                    "name": "Hotel El - Paso",
                    "area": "Baga, Goa",
                    "price_per_night": 744.0,
                    "rating": 4.6,
                    "description": "Accommodation in Goa.",
                }
            ],
            "budget_assessment": "Within budget.",
            "stay_recommendation": "Consider staying around Anjuna or Baga.",
        },
        "activities": {
            "recommended_activities": [
                {
                    "name": "Baga Beach",
                    "location": "Baga, Goa",
                    "category": "Beach",
                    "estimated_cost": 0.0,
                    "duration": "Not available",
                    "description": "Beach attraction in Goa.",
                },
                {
                    "name": "Anjuna Beach",
                    "location": "Anjuna, Goa",
                    "category": "Beach",
                    "estimated_cost": 0.0,
                    "duration": "Not available",
                    "description": "Beach attraction in Goa.",
                },
            ],
            "activities_by_category": {
                "Beach": ["Baga Beach", "Anjuna Beach"]
            },
            "budget_assessment": "Activity pricing is unavailable.",
            "activity_recommendation": "Prioritize beach activities.",
        },
        "weather": {
            "forecast": [],
            "weather_summary": "Weather information should be considered.",
            "recommendations": [
                "Check weather before outdoor activities."
            ],
        },
        "restaurants": {
            "recommended_restaurants": [
                {
                    "name": "Restaurant A",
                    "location": "Baga, Goa",
                    "category": "Restaurant",
                    "price_level": 2,
                    "rating": 4.5,
                    "distance": "Not available",
                    "description": "Restaurant in Goa.",
                }
            ],
            "restaurants_by_category": {
                "Restaurant": ["Restaurant A"]
            },
            "budget_assessment": "Restaurant pricing is represented by price level.",
            "food_recommendation": "Consider local restaurants.",
        },
    }

    result = itinerary_agent(state)

    assert "itinerary" in result
    assert result["itinerary"]["total_days"] == 2
    assert len(result["itinerary"]["itinerary"]) > 0
    assert "budget_assessment" in result["itinerary"]
    assert "planning_notes" in result["itinerary"]