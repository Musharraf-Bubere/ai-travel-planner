from src.schemas.itinerary import (
    ItineraryAnalysis,
    ItineraryItem,
)


def test_itinerary_item_schema():
    item = ItineraryItem(
        day=1,
        time="Morning",
        activity="Baga Beach",
        location="Baga, Goa",
        description="Beach activity.",
    )

    assert item.day == 1
    assert item.time == "Morning"
    assert item.activity == "Baga Beach"
    assert item.location == "Baga, Goa"


def test_itinerary_analysis_schema():
    itinerary = ItineraryAnalysis(
        itinerary=[
            ItineraryItem(
                day=1,
                time="Morning",
                activity="Baga Beach",
                location="Baga, Goa",
                description="Beach activity.",
            )
        ],
        total_days=1,
        budget_assessment="Within budget.",
        planning_notes=["Check weather before outdoor activities."],
    )

    assert itinerary.total_days == 1
    assert len(itinerary.itinerary) == 1
    assert len(itinerary.planning_notes) == 1