from src.schemas.stay import Accommodation, StayAnalysis


def test_stay_analysis():
    analysis = StayAnalysis(
        recommended_area="Candolim",
        accommodation_options=[
            Accommodation(
                name="Goa Beach Resort",
                area="Candolim",
                price_per_night=4500,
                rating=4.3,
                description="Beachside resort suitable for couples and families.",
            )
        ],
        budget_assessment="The accommodation fits within the nightly budget.",
        stay_recommendation="Candolim is a good choice for a beach-focused trip.",
    )

    assert analysis.recommended_area == "Candolim"
    assert analysis.accommodation_options
    assert analysis.accommodation_options[0].name == "Goa Beach Resort"
    assert analysis.budget_assessment
    assert analysis.stay_recommendation