from src.schemas.destination import DestinationAnalysis


def test_destination_analysis():
    analysis = DestinationAnalysis(
        overview="Goa is suitable for a beach and food-focused trip.",
        recommended_areas=["Candolim", "Anjuna", "Palolem"],
        travel_considerations=["Book accommodation early during peak season."],
        preference_suggestions=[
            "Try local Goan seafood.",
            "Visit less crowded beaches.",
        ],
    )

    assert analysis.overview
    assert "Candolim" in analysis.recommended_areas
    assert analysis.travel_considerations
    assert analysis.preference_suggestions