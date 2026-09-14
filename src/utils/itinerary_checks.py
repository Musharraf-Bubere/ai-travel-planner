from collections import defaultdict
import re


GOA_AREA_KEYWORDS = {
    "north_goa": [
        "anjuna",
        "calangute",
        "baga",
        "bardez",
        "arpora",
        "candolim",
        "nerul",
        "sinquerim",
    ],
    "central_goa": [
        "panaji",
        "panjim",
        "mormugao",
        "marmugao",
        "vasco",
    ],
    "south_goa": [
        "palolem",
        "canacona",
        "agonda",
        "betalbatim",
        "loutolim",
        "salcete",
        "margao",
        "madgaon",
        "seraulim",
        "velsao",
    ],
}


GENERIC_ACTIVITIES = {
    "check-in",
    "check in",
    "check-out",
    "check out",
    "dinner",
    "lunch",
    "breakfast",
    "free time",
    "relaxation",
}


# Activities that may look like place names after normalization
# but are not specific enough to represent a unique place.
GENERIC_PLACE_WORDS = {
    "beach",
    "visit",
    "activity",
    "attraction",
    "experience",
    "sightseeing",
    "explore",
    "exploration",
    "relax",
    "relaxation",
}


# Words that can be safely removed when comparing an itinerary
# place name with a researched place name.
PLACE_NAME_STOPWORDS = {
    "visit",
    "goa",
}


def normalize_location(location: str) -> str:
    """Normalize a location string for comparison."""
    return " ".join(location.lower().split())


def normalize_place_name(name: str) -> str:
    """
    Normalize a place name for tolerant entity matching.

    This removes harmless naming differences such as:
    - capitalization
    - punctuation
    - common itinerary suffixes such as 'Visit'
    - destination suffixes such as 'Goa'

    It does not perform fuzzy matching and does not invent aliases.
    """
    normalized = normalize_location(name)

    # Replace punctuation with spaces.
    normalized = re.sub(
        r"[^a-z0-9\s]",
        " ",
        normalized,
    )

    # Normalize whitespace after punctuation removal.
    tokens = normalized.split()

    # Remove harmless comparison-only words.
    tokens = [
        token
        for token in tokens
        if token not in PLACE_NAME_STOPWORDS
    ]

    return " ".join(tokens)


def places_match(
    itinerary_name: str,
    researched_name: str,
) -> bool:
    """
    Determine whether an itinerary place matches a researched place.

    Matching is intentionally conservative.

    Examples:
        'Butterfly Beach Visit' == 'Butterfly Beach Goa'
        'Palolem Beach Visit' == 'Palolem Beach, GOA'

    Longer names are also supported when one normalized name contains
    the other, such as an itinerary name containing a researched name.
    """
    itinerary_normalized = normalize_place_name(
        itinerary_name
    )

    researched_normalized = normalize_place_name(
        researched_name
    )

    if not itinerary_normalized or not researched_normalized:
        return False

    if itinerary_normalized == researched_normalized:
        return True

    return (
        itinerary_normalized in researched_normalized
        or researched_normalized in itinerary_normalized
    )


def classify_area(location: str) -> str:
    """
    Classify a location into a broad geographic area.

    Returns 'unknown' when the available location data is insufficient.
    """
    normalized = normalize_location(location)

    for area, keywords in GOA_AREA_KEYWORDS.items():
        if any(
            keyword in normalized
            for keyword in keywords
        ):
            return area

    return "unknown"


def extract_location_groups(
    itinerary: list[dict],
) -> dict[int, list[str]]:
    """Group itinerary locations by day."""
    locations_by_day = defaultdict(list)

    for item in itinerary:
        day = item.get("day")
        location = item.get("location")

        if day is None or not location:
            continue

        normalized = normalize_location(location)

        if normalized not in locations_by_day[day]:
            locations_by_day[day].append(normalized)

    return dict(locations_by_day)


def find_geographic_inconsistencies(
    itinerary: list[dict],
    destination: str,
) -> list[str]:
    """
    Detect potentially inefficient geographic planning.

    This check validates:

    1. Multiple geographic areas within the same day.
    2. Excessive geographic spread across a short trip.
    3. Direct movement between different geographic regions
       on consecutive days.

    The check is intentionally conservative and only uses known
    geographic keywords. It does not invent distances or travel times.
    """
    if not itinerary:
        return []

    if destination.lower().strip() != "goa":
        return []

    issues = []

    locations_by_day = extract_location_groups(
        itinerary
    )

    # ------------------------------------------------------------
    # Determine geographic areas used by each day
    # ------------------------------------------------------------

    day_areas = {}

    for day, locations in locations_by_day.items():
        areas = {
            classify_area(location)
            for location in locations
        }

        # Unknown locations cannot safely be used to make a
        # geographic judgment.
        areas.discard("unknown")

        day_areas[day] = areas

    # ------------------------------------------------------------
    # Check 1: Multiple geographic areas within the same day
    # ------------------------------------------------------------

    for day, areas in day_areas.items():
        if len(areas) > 1:
            area_names = ", ".join(
                sorted(areas)
            )

            issues.append(
                f"Day {day} combines locations from multiple geographic "
                f"areas ({area_names}). Consider grouping activities within "
                f"the same area for a short trip."
            )

    # ------------------------------------------------------------
    # Collect days containing known geographic information
    # ------------------------------------------------------------

    known_day_areas = {
        day: areas
        for day, areas in day_areas.items()
        if areas
    }

    if not known_day_areas:
        return issues

    # ------------------------------------------------------------
    # Check 2: Geographic spread across the complete short trip
    # ------------------------------------------------------------

    all_areas = set()

    for areas in known_day_areas.values():
        all_areas.update(areas)

    # A short Goa trip spanning all three broad regions is a strong
    # indication of unnecessary geographic movement.
    if len(all_areas) >= 3:
        area_names = ", ".join(
            sorted(all_areas)
        )

        issues.append(
            f"The itinerary spans multiple distant geographic areas "
            f"across the short trip ({area_names}). Consider selecting "
            f"one primary region instead of repeatedly moving between "
            f"North, Central, and South Goa."
        )

    # ------------------------------------------------------------
    # Check 3: Consecutive-day geographic movement
    # ------------------------------------------------------------

    ordered_days = sorted(
        known_day_areas
    )

    for previous_day, current_day in zip(
        ordered_days,
        ordered_days[1:],
    ):
        previous_areas = known_day_areas[
            previous_day
        ]

        current_areas = known_day_areas[
            current_day
        ]

        # If the two consecutive days have no geographic
        # region in common, flag the movement.
        if previous_areas.isdisjoint(
            current_areas
        ):
            previous_names = ", ".join(
                sorted(previous_areas)
            )

            current_names = ", ".join(
                sorted(current_areas)
            )

            issues.append(
                f"The itinerary moves from {previous_names} on "
                f"Day {previous_day} to {current_names} on "
                f"Day {current_day}. Consider keeping consecutive "
                f"days within the same primary geographic region "
                f"for a short trip."
            )

    return issues


def extract_itinerary_places(
    itinerary: list[dict],
) -> dict[str, list[int]]:
    """
    Extract meaningful named places from itinerary items.

    Activities use the activity field as the place name.

    Restaurant-style entries such as Dinner use the location field
    because the actual restaurant name is stored there.

    Generic activity names such as 'Beach Visit' are not treated as
    named places because they do not identify a unique location.
    """
    place_occurrences = defaultdict(list)

    for item in itinerary:
        activity = item.get(
            "activity",
            "",
        ).strip()

        location = item.get(
            "location",
            "",
        ).strip()

        day = item.get("day")

        if not day:
            continue

        activity_normalized = normalize_location(
            activity
        )

        # --------------------------------------------------------
        # Generic activities
        # --------------------------------------------------------

        if activity_normalized in GENERIC_ACTIVITIES:
            if location:
                normalized_location = normalize_location(
                    location
                )

                if normalized_location:
                    place_occurrences[
                        normalized_location
                    ].append(day)

            continue

        # --------------------------------------------------------
        # Generic activity patterns
        # --------------------------------------------------------

        normalized_activity_for_duplicate_check = (
            normalize_place_name(activity)
        )

        activity_tokens = set(
            normalized_activity_for_duplicate_check.split()
        )

        # If normalization leaves only generic words such as
        # 'beach', 'visit', or 'attraction', the activity does not
        # identify a unique place and should not be treated as one.
        if (
            normalized_activity_for_duplicate_check
            and activity_tokens
            and activity_tokens.issubset(
                GENERIC_PLACE_WORDS
            )
        ):
            continue

        # --------------------------------------------------------
        # Normal activity / attraction
        # --------------------------------------------------------

        if activity:
            normalized_place = normalize_place_name(
                activity
            )

            if normalized_place:
                place_occurrences[
                    normalized_place
                ].append(day)

    return dict(place_occurrences)


def find_duplicate_itinerary_places(
    itinerary: list[dict],
) -> list[str]:
    """
    Detect repeated named places across different itinerary days.

    Generic activities such as Dinner, Lunch, Breakfast, Check-in,
    and Relaxation are not treated as places themselves.

    Generic descriptions such as 'Beach Visit' are also not treated
    as unique places.

    For generic activities, the location is checked so repeated
    restaurants can still be detected.
    """
    place_occurrences = extract_itinerary_places(
        itinerary
    )

    issues = []

    for place, days in place_occurrences.items():
        unique_days = sorted(
            set(days)
        )

        if len(unique_days) > 1:
            issues.append(
                f"'{place}' is repeated on multiple days: "
                f"{', '.join(str(day) for day in unique_days)}."
            )

    return issues


def find_ungrounded_itinerary_places(
    itinerary: list[dict],
    activities: dict,
    restaurants: dict,
    stay_options: dict,
) -> list[str]:
    """
    Detect itinerary places that cannot be traced to the available
    research results.

    This deterministic check complements the LLM validator by checking
    explicit names against researched activities, restaurants, and
    accommodations.
    """
    issues = []

    # ------------------------------------------------------------
    # Extract researched activity names
    # ------------------------------------------------------------

    researched_activities = [
        activity.get("name", "")
        for activity in activities.get(
            "recommended_activities",
            [],
        )
        if activity.get("name")
    ]

    # ------------------------------------------------------------
    # Extract researched restaurant names
    # ------------------------------------------------------------

    researched_restaurants = [
        restaurant.get("name", "")
        for restaurant in restaurants.get(
            "recommended_restaurants",
            [],
        )
        if restaurant.get("name")
    ]

    # ------------------------------------------------------------
    # Extract researched accommodation names
    # ------------------------------------------------------------

    researched_accommodations = [
        accommodation.get("name", "")
        for accommodation in stay_options.get(
            "accommodation_options",
            [],
        )
        if accommodation.get("name")
    ]

    # ------------------------------------------------------------
    # Check itinerary items
    # ------------------------------------------------------------

    for item in itinerary:
        activity = item.get(
            "activity",
            "",
        ).strip()

        location = item.get(
            "location",
            "",
        ).strip()

        description = item.get(
            "description",
            "",
        ).strip()

        if not activity:
            continue

        activity_normalized = normalize_location(
            activity
        )

        # --------------------------------------------------------
        # Generic activities
        # --------------------------------------------------------

        if activity_normalized in GENERIC_ACTIVITIES:
            continue

        # --------------------------------------------------------
        # Restaurant entries
        # --------------------------------------------------------

        if activity_normalized.startswith(
            "dinner at "
        ):
            restaurant_name = activity[
                len("dinner at "):
            ].strip()

            matched_restaurant = any(
                places_match(
                    restaurant_name,
                    researched_name,
                )
                for researched_name
                in researched_restaurants
            )

            if not matched_restaurant:
                issues.append(
                    f"Restaurant '{restaurant_name}' "
                    f"is not present in the researched restaurant results."
                )

            continue

        if activity_normalized.startswith(
            "lunch at "
        ):
            restaurant_name = activity[
                len("lunch at "):
            ].strip()

            matched_restaurant = any(
                places_match(
                    restaurant_name,
                    researched_name,
                )
                for researched_name
                in researched_restaurants
            )

            if not matched_restaurant:
                issues.append(
                    f"Restaurant '{restaurant_name}' "
                    f"is not present in the researched restaurant results."
                )

            continue

        # --------------------------------------------------------
        # Accommodation entries
        # --------------------------------------------------------

        if (
            "check-in" in activity_normalized
            or "check in" in activity_normalized
        ):
            accommodation_text = (
                f"{activity} "
                f"{location} "
                f"{description}"
            )

            # If the itinerary explicitly mentions a researched
            # accommodation, it is grounded.
            matched_accommodation = any(
                places_match(
                    researched_name,
                    accommodation_text,
                )
                for researched_name
                in researched_accommodations
            )

            # If no specific accommodation is mentioned,
            # generic check-in is acceptable.
            has_specific_accommodation = any(
                normalize_place_name(
                    researched_name
                ) in normalize_place_name(
                    accommodation_text
                )
                for researched_name
                in researched_accommodations
            )

            if (
                not matched_accommodation
                and has_specific_accommodation
            ):
                issues.append(
                    f"Accommodation in '{activity}' "
                    f"cannot be traced to the researched "
                    f"accommodation results."
                )

            continue

        # --------------------------------------------------------
        # Normal activity / attraction
        # --------------------------------------------------------

        matched_activity = any(
            places_match(
                activity,
                researched_name,
            )
            for researched_name
            in researched_activities
        )

        if not matched_activity:
            issues.append(
                f"Activity '{activity}' is not present in the "
                f"researched activity results."
            )

    return issues