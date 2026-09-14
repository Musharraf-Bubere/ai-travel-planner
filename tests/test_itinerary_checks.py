from src.utils.itinerary_checks import (
    classify_area,
    extract_location_groups,
    find_duplicate_itinerary_places,
    find_geographic_inconsistencies,
    find_ungrounded_itinerary_places,
)


def test_classify_goa_location():
    assert classify_area("Palolem, Canacona, Goa") == "south_goa"
    assert classify_area("Anjuna, Goa") == "north_goa"
    assert classify_area("Panaji, Goa") == "central_goa"


def test_extract_location_groups():
    itinerary = [
        {
            "day": 1,
            "time": "Morning",
            "activity": "Velsao Beach",
            "location": "Velsao, Goa",
            "description": "",
        },
        {
            "day": 1,
            "time": "Evening",
            "activity": "Dinner",
            "location": "Betalbatim, Goa",
            "description": "",
        },
        {
            "day": 2,
            "time": "Morning",
            "activity": "Palolem Beach",
            "location": "Palolem, Goa",
            "description": "",
        },
    ]

    groups = extract_location_groups(itinerary)

    assert 1 in groups
    assert 2 in groups
    assert len(groups[1]) == 2
    assert len(groups[2]) == 1


def test_detect_mixed_geographic_areas():
    itinerary = [
        {
            "day": 1,
            "time": "Morning",
            "activity": "Palolem Beach",
            "location": "Palolem, Goa",
            "description": "",
        },
        {
            "day": 1,
            "time": "Evening",
            "activity": "Dinner",
            "location": "Anjuna, Goa",
            "description": "",
        },
    ]

    issues = find_geographic_inconsistencies(
        itinerary,
        "Goa",
    )

    assert len(issues) == 1
    assert "Day 1" in issues[0]
    assert "multiple geographic areas" in issues[0]


def test_accept_same_geographic_area():
    itinerary = [
        {
            "day": 1,
            "time": "Morning",
            "activity": "Palolem Beach",
            "location": "Palolem, Goa",
            "description": "",
        },
        {
            "day": 1,
            "time": "Afternoon",
            "activity": "Agonda Beach",
            "location": "Agonda, Goa",
            "description": "",
        },
    ]

    issues = find_geographic_inconsistencies(
        itinerary,
        "Goa",
    )

    assert issues == []


def test_skip_geographic_check_for_unknown_destination():
    itinerary = [
        {
            "day": 1,
            "time": "Morning",
            "activity": "Attraction",
            "location": "Somewhere",
            "description": "",
        }
    ]

    issues = find_geographic_inconsistencies(
        itinerary,
        "Paris",
    )

    assert issues == []

def test_detect_cross_region_movement_across_short_trip():
    itinerary = [
        {
            "day": 1,
            "time": "10:00 AM",
            "activity": "Sinquerim Beach Visit",
            "location": "Sinquerim, Candolim, Goa",
            "description": "Beach visit.",
        },
        {
            "day": 2,
            "time": "10:00 AM",
            "activity": "Velsao Beach Visit",
            "location": "Velsao, Goa",
            "description": "Beach visit.",
        },
        {
            "day": 3,
            "time": "10:00 AM",
            "activity": "Japanese Garden Visit",
            "location": "Mormugao, Goa",
            "description": "Garden visit.",
        },
    ]

    issues = find_geographic_inconsistencies(
        itinerary,
        "Goa",
    )

    assert issues

    assert any(
        "north_goa" in issue
        and "south_goa" in issue
        for issue in issues
    )

def test_detect_duplicate_itinerary_places():
    itinerary = [
        {
            "day": 1,
            "time": "Morning",
            "activity": "Palolem Beach",
            "location": "Palolem, Goa",
            "description": "",
        },
        {
            "day": 2,
            "time": "Morning",
            "activity": "Palolem Beach",
            "location": "Palolem, Goa",
            "description": "",
        },
    ]

    issues = find_duplicate_itinerary_places(
        itinerary
    )

    assert len(issues) == 1
    assert "palolem beach" in issues[0]
    assert "1, 2" in issues[0]

def test_detect_duplicate_restaurants():
    itinerary = [
        {
            "day": 1,
            "time": "Evening",
            "activity": "Dinner",
            "location": "The Fishermans Wharf, Goa",
            "description": "",
        },
        {
            "day": 2,
            "time": "Evening",
            "activity": "Dinner",
            "location": "The Fishermans Wharf, Goa",
            "description": "",
        },
    ]

    issues = find_duplicate_itinerary_places(
        itinerary
    )

    assert len(issues) == 1
    assert "the fishermans wharf" in issues[0]
    assert "1, 2" in issues[0]


def test_detect_ungrounded_activity():
    itinerary = [
        {
            "day": 1,
            "time": "Morning",
            "activity": "Explore Hidden Waterfall",
            "location": "Goa",
            "description": "",
        }
    ]

    activities = {
        "recommended_activities": [
            {
                "name": "Palolem Beach",
            }
        ]
    }

    restaurants = {
        "recommended_restaurants": []
    }

    stay_options = {
        "accommodation_options": []
    }

    issues = find_ungrounded_itinerary_places(
        itinerary,
        activities,
        restaurants,
        stay_options,
    )

    assert len(issues) == 1
    assert "Explore Hidden Waterfall" in issues[0]
    assert "researched activity results" in issues[0]


def test_accept_grounded_activity_and_restaurant():
    itinerary = [
        {
            "day": 1,
            "time": "Morning",
            "activity": "Palolem Beach Visit",
            "location": "Palolem, Goa",
            "description": "",
        },
        {
            "day": 1,
            "time": "Evening",
            "activity": "Dinner at Fat Fish",
            "location": "Arpora, Goa",
            "description": "",
        }
    ]

    activities = {
        "recommended_activities": [
            {
                "name": "Palolem Beach",
            }
        ]
    }

    restaurants = {
        "recommended_restaurants": [
            {
                "name": "Fat Fish",
            }
        ]
    }

    stay_options = {
        "accommodation_options": []
    }

    issues = find_ungrounded_itinerary_places(
        itinerary,
        activities,
        restaurants,
        stay_options,
    )

    assert issues == []