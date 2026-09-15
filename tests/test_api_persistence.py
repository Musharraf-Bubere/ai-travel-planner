from fastapi.testclient import TestClient

from src.api.main import app
from src.database.connection import SessionLocal
from src.database.models import Trip
from src.database.repository import get_travel_plans_for_trip


client = TestClient(
    app,
    raise_server_exceptions=False,
)


def test_plan_persists_trip_and_travel_plan(monkeypatch):
    """Verify that /plan persists the trip and generated plan."""

    mock_result = {
        "itinerary": {
            "days": [
                {
                    "day": 1,
                    "morning": "Visit the old town",
                    "afternoon": "Explore the local market",
                    "evening": "Enjoy a local dinner",
                }
            ]
        },
        "stay_options": {
            "recommended_area": "Central Area",
            "accommodation_options": [],
            "budget_assessment": "Within budget",
            "stay_recommendation": "Stay near the city center.",
        },
        "restaurants": {
            "recommended_restaurants": [],
            "restaurants_by_cuisine": {},
            "budget_assessment": "Within budget",
            "food_recommendation": "Try local cuisine.",
        },
        "validation": {
            "is_valid": True,
            "issues": [],
            "feedback": "The itinerary is valid.",
        },
        "validation_attempts": 1,
        "final_response": {
            "destination": "Test Destination",
            "trip_summary": "A short test travel plan.",
            "itinerary": [
                {
                    "day": 1,
                    "morning": "Visit the old town",
                    "afternoon": "Explore the local market",
                    "evening": "Enjoy a local dinner",
                }
            ],
            "accommodation_summary": "Stay near the city center.",
            "food_summary": "Try local cuisine.",
            "travel_tips": [
                "Carry essential documents.",
            ],
        },
    }

    monkeypatch.setattr(
        "src.api.main.run_travel_planner",
        lambda request: mock_result,
    )

    response = client.post(
        "/plan",
        json={
            "destination": "Test Destination",
            "travel_dates": "2026-10-01 to 2026-10-03",
            "duration": 3,
            "travelers": 2,
            "budget": 50000,
            "preferences": [
                "nature",
                "food",
            ],
        },
    )

    assert response.status_code == 200

    response_data = response.json()

    assert response_data["destination"] == "Test Destination"

    assert response_data["travel_dates"] == (
        "2026-10-01 to 2026-10-03"
    )

    assert response_data["validation"]["is_valid"] is True

    assert response_data["validation_attempts"] == 1

    assert response_data["final_response"]["destination"] == (
        "Test Destination"
    )

    assert response_data["final_response"]["trip_summary"] == (
        "A short test travel plan."
    )

    assert response_data["final_response"]["itinerary"][0]["day"] == 1

    assert response_data["final_response"]["accommodation_summary"] == (
        "Stay near the city center."
    )

    assert response_data["final_response"]["food_summary"] == (
        "Try local cuisine."
    )

    assert response_data["final_response"]["travel_tips"] == [
        "Carry essential documents.",
    ]

    db = SessionLocal()

    trip = None

    try:
        trip = (
            db.query(Trip)
            .filter(
                Trip.destination == "Test Destination"
            )
            .order_by(Trip.id.desc())
            .first()
        )

        assert trip is not None

        assert trip.status == "completed"

        assert trip.travel_dates == (
            "2026-10-01 to 2026-10-03"
        )

        assert trip.duration == 3

        assert trip.travelers == 2

        assert trip.budget == 50000

        assert trip.preferences == [
            "nature",
            "food",
        ]

        plans = get_travel_plans_for_trip(
            db,
            trip_id=trip.id,
        )

        assert plans

        plan = plans[0]

        assert plan.trip_id == trip.id

        assert plan.itinerary["days"][0]["day"] == 1

        assert plan.itinerary["days"][0]["morning"] == (
            "Visit the old town"
        )

        assert plan.validation["is_valid"] is True

        assert plan.validation["issues"] == []

        assert plan.validation_attempts == 1

        assert plan.accommodation_summary[
            "recommended_area"
        ] == "Central Area"

        assert plan.food_summary[
            "food_recommendation"
        ] == "Try local cuisine."

        assert plan.travel_tips == [
            "Carry essential documents.",
        ]

    finally:
        if trip is not None:
            db.delete(trip)
            db.commit()

        db.close()


def test_plan_marks_trip_failed_when_planner_fails(
    monkeypatch,
):
    """Verify that a planning failure marks the trip as failed."""

    def mock_failed_planner(request):
        raise RuntimeError(
            "Simulated planner failure"
        )

    monkeypatch.setattr(
        "src.api.main.run_travel_planner",
        mock_failed_planner,
    )

    response = client.post(
        "/plan",
        json={
            "destination": "Failure Test Destination",
            "travel_dates": "2026-10-01 to 2026-10-03",
            "duration": 3,
            "travelers": 2,
            "budget": 50000,
            "preferences": [
                "nature",
            ],
        },
    )

    assert response.status_code == 500

    response_data = response.json()

    assert response_data["detail"] == (
        "Travel planning failed: Simulated planner failure"
    )

    db = SessionLocal()

    trip = None

    try:
        trip = (
            db.query(Trip)
            .filter(
                Trip.destination
                == "Failure Test Destination"
            )
            .order_by(Trip.id.desc())
            .first()
        )

        assert trip is not None

        assert trip.status == "failed"

        plans = get_travel_plans_for_trip(
            db,
            trip_id=trip.id,
        )

        assert plans == []

    finally:
        if trip is not None:
            db.delete(trip)
            db.commit()

        db.close()