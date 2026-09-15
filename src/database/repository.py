from typing import Any

from sqlalchemy import select
from sqlalchemy.orm import Session

from src.database.models import TravelPlan, Trip


def create_trip(
    db: Session,
    destination: str,
    travel_dates: str,
    duration: int,
    travelers: int,
    budget: float,
    preferences: list[str],
    status: str = "created",
) -> Trip:
    """Create and persist a new trip request."""

    trip = Trip(
        destination=destination,
        travel_dates=travel_dates,
        duration=duration,
        travelers=travelers,
        budget=budget,
        preferences=preferences,
        status=status,
    )

    db.add(trip)
    db.commit()
    db.refresh(trip)

    return trip


def get_trip(
    db: Session,
    trip_id: int,
) -> Trip | None:
    """Retrieve a trip by its primary key."""

    statement = select(Trip).where(
        Trip.id == trip_id
    )

    return db.scalar(statement)


def update_trip_status(
    db: Session,
    trip_id: int,
    status: str,
) -> Trip | None:
    """Update the status of an existing trip."""

    trip = get_trip(db, trip_id)

    if trip is None:
        return None

    trip.status = status

    db.commit()
    db.refresh(trip)

    return trip


def create_travel_plan(
    db: Session,
    trip_id: int,
    itinerary: dict[str, Any],
    accommodation_summary: dict[str, Any] | None = None,
    food_summary: dict[str, Any] | None = None,
    travel_tips: dict[str, Any] | None = None,
    validation: dict[str, Any] | None = None,
    validation_attempts: int = 0,
) -> TravelPlan:
    """Create and persist a generated travel plan."""

    travel_plan = TravelPlan(
        trip_id=trip_id,
        itinerary=itinerary,
        accommodation_summary=accommodation_summary or {},
        food_summary=food_summary or {},
        travel_tips=travel_tips or {},
        validation=validation or {},
        validation_attempts=validation_attempts,
    )

    db.add(travel_plan)
    db.commit()
    db.refresh(travel_plan)

    return travel_plan


def get_travel_plan(
    db: Session,
    plan_id: int,
) -> TravelPlan | None:
    """Retrieve a travel plan by its primary key."""

    statement = select(TravelPlan).where(
        TravelPlan.id == plan_id
    )

    return db.scalar(statement)


def get_travel_plans_for_trip(
    db: Session,
    trip_id: int,
) -> list[TravelPlan]:
    """Retrieve all travel plans generated for a trip."""

    statement = (
        select(TravelPlan)
        .where(TravelPlan.trip_id == trip_id)
        .order_by(TravelPlan.created_at.desc())
    )

    return list(db.scalars(statement).all())