from datetime import datetime

from sqlalchemy import DateTime, Float, ForeignKey, Integer, String, Text
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func

from src.database.connection import Base


class Trip(Base):
    """Store the original travel request."""

    __tablename__ = "trips"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True,
    )

    destination: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    travel_dates: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    duration: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )

    travelers: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )

    budget: Mapped[float] = mapped_column(
        Float,
        nullable=False,
    )

    preferences: Mapped[list] = mapped_column(
        JSONB,
        nullable=False,
        default=list,
    )

    status: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        default="created",
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )

    travel_plans: Mapped[list["TravelPlan"]] = relationship(
        "TravelPlan",
        back_populates="trip",
        cascade="all, delete-orphan",
    )


class TravelPlan(Base):
    """Store the generated AI travel plan."""

    __tablename__ = "travel_plans"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True,
    )

    trip_id: Mapped[int] = mapped_column(
        ForeignKey("trips.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    itinerary: Mapped[dict] = mapped_column(
        JSONB,
        nullable=False,
    )

    accommodation_summary: Mapped[dict] = mapped_column(
        JSONB,
        nullable=False,
        default=dict,
    )

    food_summary: Mapped[dict] = mapped_column(
        JSONB,
        nullable=False,
        default=dict,
    )

    travel_tips: Mapped[dict] = mapped_column(
        JSONB,
        nullable=False,
        default=dict,
    )

    validation: Mapped[dict] = mapped_column(
        JSONB,
        nullable=False,
        default=dict,
    )

    validation_attempts: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        default=0,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )

    trip: Mapped["Trip"] = relationship(
        "Trip",
        back_populates="travel_plans",
    )