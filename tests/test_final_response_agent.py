from src.agents.final_response_agent import final_response_agent


def test_final_response_agent():
    state = {
        "destination": "Goa",
        "travel_dates": "2026-10-10 to 2026-10-13",
        "duration": 3,
        "travelers": 2,
        "budget": 30000,
        "preferences": ["beaches", "food"],

        "destination_data": {
            "overview": "Goa is a coastal destination.",
            "recommended_areas": ["North Goa"],
            "travel_considerations": ["Plan outdoor activities around weather."],
            "preference_suggestions": ["Explore beaches and local food."],
        },

        "stay_options": {
            "recommended_area": "North Goa",
            "accommodation_options": [
                {
                    "name": "Sample Beach Hotel",
                    "area": "North Goa",
                    "price_per_night": 3000,
                    "rating": 4.2,
                    "description": "Beachside accommodation.",
                }
            ],
            "budget_assessment": "Within the requested budget.",
            "stay_recommendation": "North Goa is suitable for this trip.",
        },

        "activities": {
            "recommended_activities": [
                {
                    "name": "Baga Beach",
                    "location": "North Goa",
                    "category": "Beach",
                    "estimated_cost": 0.0,
                    "duration": "Not available",
                    "description": "Popular beach destination.",
                }
            ],
            "activities_by_category": {
                "Beach": ["Baga Beach"]
            },
            "budget_assessment": "Suitable for the requested budget.",
            "activity_recommendation": "Focus on beach activities.",
        },

        "weather": {
            "forecast": [],
            "weather_summary": "Weather information available.",
            "weather_recommendation": "Check the forecast before outdoor activities.",
        },

        "restaurants": {
            "recommended_restaurants": [
                {
                    "name": "Sample Restaurant",
                    "location": "North Goa",
                    "category": "Restaurant",
                    "price_level": 2,
                    "rating": 4.3,
                    "distance": "Not available",
                    "description": "Local restaurant.",
                }
            ],
            "restaurants_by_category": {
                "Restaurant": ["Sample Restaurant"]
            },
            "budget_assessment": "Suitable for the requested budget.",
            "food_recommendation": "Try local restaurants in North Goa.",
        },

        "itinerary": {
            "itinerary": [
                {
                    "day": 1,
                    "time": "Morning",
                    "activity": "Baga Beach",
                    "location": "North Goa",
                    "description": "Visit the beach.",
                }
            ],
            "total_days": 3,
            "budget_assessment": "Within budget.",
            "planning_notes": ["Keep outdoor activities flexible."],
        },

        "validation": {
            "is_valid": True,
            "issues": [],
            "feedback": "The itinerary satisfies the validation rules.",
        },
    }

    result = final_response_agent(state)

    assert "final_response" in result

    final_response = result["final_response"]

    assert final_response["destination"] == "Goa"
    assert final_response["trip_summary"]
    assert isinstance(final_response["itinerary"], list)
    assert final_response["accommodation_summary"]
    assert final_response["food_summary"]
    assert isinstance(final_response["travel_tips"], list)