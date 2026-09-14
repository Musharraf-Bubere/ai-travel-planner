from fastapi.testclient import TestClient

from src.api.main import app


client = TestClient(app)


MOCK_FINAL_RESPONSE = {
    "destination": "Goa",
    "trip_summary": "A 3-day Goa travel plan.",
    "itinerary": [
        {
            "day": 1,
            "time": "10:00 AM",
            "activity": "Sinquerim Beach Visit",
            "location": "Sinquerim, Goa",
            "description": "Beach visit.",
        }
    ],
    "accommodation_summary": "Recommended accommodation in Goa.",
    "food_summary": "Recommended restaurants in Goa.",
    "travel_tips": [
        "Check weather conditions before outdoor activities."
    ],
}


MOCK_GRAPH_RESULT = {
    "destination": "Goa",
    "travel_dates": "2026-10-10 to 2026-10-13",
    "validation": {
        "is_valid": True,
        "issues": [],
        "feedback": "Itinerary passed validation.",
    },
    "validation_attempts": 1,
    "final_response": MOCK_FINAL_RESPONSE,
}


def test_health_check():
    response = client.get("/health")

    assert response.status_code == 200

    assert response.json() == {
        "status": "healthy",
        "service": "AI Travel Planner API",
    }


def test_valid_travel_request(monkeypatch):
    def mock_run_travel_planner(request):
        return MOCK_GRAPH_RESULT

    monkeypatch.setattr(
        "src.api.main.run_travel_planner",
        mock_run_travel_planner,
    )

    payload = {
        "destination": "Goa",
        "travel_dates": "2026-10-10 to 2026-10-13",
        "duration": 3,
        "travelers": 2,
        "budget": 30000,
        "preferences": [
            "beaches",
            "food",
            "relaxation",
        ],
    }

    response = client.post(
        "/plan",
        json=payload,
    )

    assert response.status_code == 200

    data = response.json()

    assert data["destination"] == "Goa"

    assert data["travel_dates"] == (
        "2026-10-10 to 2026-10-13"
    )

    assert data["validation"]["is_valid"] is True

    assert data["validation_attempts"] == 1

    assert (
        data["final_response"]["destination"]
        == "Goa"
    )


def test_invalid_duration():
    payload = {
        "destination": "Goa",
        "travel_dates": "2026-10-10 to 2026-10-13",
        "duration": 0,
        "travelers": 2,
        "budget": 30000,
        "preferences": [
            "beaches",
        ],
    }

    response = client.post(
        "/plan",
        json=payload,
    )

    assert response.status_code == 422


def test_invalid_travelers():
    payload = {
        "destination": "Goa",
        "travel_dates": "2026-10-10 to 2026-10-13",
        "duration": 3,
        "travelers": 0,
        "budget": 30000,
        "preferences": [
            "beaches",
        ],
    }

    response = client.post(
        "/plan",
        json=payload,
    )

    assert response.status_code == 422


def test_invalid_budget():
    payload = {
        "destination": "Goa",
        "travel_dates": "2026-10-10 to 2026-10-13",
        "duration": 3,
        "travelers": 2,
        "budget": 0,
        "preferences": [
            "beaches",
        ],
    }

    response = client.post(
        "/plan",
        json=payload,
    )

    assert response.status_code == 422


def test_missing_destination():
    payload = {
        "travel_dates": "2026-10-10 to 2026-10-13",
        "duration": 3,
        "travelers": 2,
        "budget": 30000,
        "preferences": [
            "beaches",
        ],
    }

    response = client.post(
        "/plan",
        json=payload,
    )

    assert response.status_code == 422


def test_missing_required_fields():
    response = client.post(
        "/plan",
        json={},
    )

    assert response.status_code == 422


def test_empty_destination():
    payload = {
        "destination": "",
        "travel_dates": "2026-10-10 to 2026-10-13",
        "duration": 3,
        "travelers": 2,
        "budget": 30000,
        "preferences": [
            "beaches",
        ],
    }

    response = client.post(
        "/plan",
        json=payload,
    )

    assert response.status_code == 422


def test_empty_travel_dates():
    payload = {
        "destination": "Goa",
        "travel_dates": "",
        "duration": 3,
        "travelers": 2,
        "budget": 30000,
        "preferences": [
            "beaches",
        ],
    }

    response = client.post(
        "/plan",
        json=payload,
    )

    assert response.status_code == 422


def test_negative_duration():
    payload = {
        "destination": "Goa",
        "travel_dates": "2026-10-10 to 2026-10-13",
        "duration": -1,
        "travelers": 2,
        "budget": 30000,
        "preferences": [
            "beaches",
        ],
    }

    response = client.post(
        "/plan",
        json=payload,
    )

    assert response.status_code == 422


def test_negative_travelers():
    payload = {
        "destination": "Goa",
        "travel_dates": "2026-10-10 to 2026-10-13",
        "duration": 3,
        "travelers": -1,
        "budget": 30000,
        "preferences": [
            "beaches",
        ],
    }

    response = client.post(
        "/plan",
        json=payload,
    )

    assert response.status_code == 422


def test_negative_budget():
    payload = {
        "destination": "Goa",
        "travel_dates": "2026-10-10 to 2026-10-13",
        "duration": 3,
        "travelers": 2,
        "budget": -1000,
        "preferences": [
            "beaches",
        ],
    }

    response = client.post(
        "/plan",
        json=payload,
    )

    assert response.status_code == 422


def test_empty_preferences_are_allowed(monkeypatch):
    def mock_run_travel_planner(request):
        return MOCK_GRAPH_RESULT

    monkeypatch.setattr(
        "src.api.main.run_travel_planner",
        mock_run_travel_planner,
    )

    payload = {
        "destination": "Goa",
        "travel_dates": "2026-10-10 to 2026-10-13",
        "duration": 3,
        "travelers": 2,
        "budget": 30000,
    }

    response = client.post(
        "/plan",
        json=payload,
    )

    assert response.status_code == 200


def test_planning_failure_returns_500(monkeypatch):
    def mock_run_travel_planner(request):
        raise RuntimeError(
            "Test planning failure"
        )

    monkeypatch.setattr(
        "src.api.main.run_travel_planner",
        mock_run_travel_planner,
    )

    payload = {
        "destination": "Goa",
        "travel_dates": "2026-10-10 to 2026-10-13",
        "duration": 3,
        "travelers": 2,
        "budget": 30000,
        "preferences": [
            "beaches",
        ],
    }

    response = client.post(
        "/plan",
        json=payload,
    )

    assert response.status_code == 500

    assert response.json() == {
        "detail": (
            "Travel planning failed: Test planning failure"
        )
    }