from collections import defaultdict
import re


GOA_AREA_KEYWORDS = {
    "north_goa": [
        # North Goa towns / areas
        "arambol",
        "mandrem",
        "ashwem",
        "morjim",
        "siolim",
        "chapora",
        "vagator",
        "mapusa",
        "bardez",
        "anjuna",
        "assagao",
        "parra",
        "arpora",
        "calangute",
        "baga",
        "candolim",
        "nerul",
        "sinquerim",
        "reis magos",
        "saligao",
        "porvorim",

        # Common North Goa attractions / beaches
        "arambol beach",
        "mandrem beach",
        "ashwem beach",
        "morjim beach",
        "vagator beach",
        "chapora beach",
        "anjuna beach",
        "calangute beach",
        "baga beach",
        "candolim beach",
        "sinquerim beach",
        "fort aguada",
        "aguada fort",
        "chapora fort",
        "sweet water lake",
        "sweetwater lake",
    ],
    "central_goa": [
        # Central Goa / Panaji and Mormugao areas
        "panaji",
        "panjim",
        "miramar",
        "caranzalem",
        "dona paula",
        "taleigao",
        "old goa",
        "velha goa",
        "ribandar",
        "mormugao",
        "marmugao",
        "vasco",
        "vasco da gama",
        "chicalim",
        "sancoale",
        "verna",

        # Common Central Goa attractions
        "miramar beach",
        "dona paula",
        "basilica of bom jesus",
        "se cathedral",
    ],
    "south_goa": [
        # South Goa towns / areas
        "palolem",
        "canacona",
        "agonda",
        "patnem",
        "colomb",
        "galgibaga",
        "talpona",
        "cabo de rama",
        "cavelossim",
        "mobor",
        "varca",
        "benaulim",
        "betalbatim",
        "colva",
        "majorda",
        "utorda",
        "loutolim",
        "salcete",
        "margao",
        "madgaon",
        "seraulim",
        "velsao",
        "cansaulim",
        "quiteria",
        "chinchinim",

        # Common South Goa attractions / beaches
        "palolem beach",
        "patnem beach",
        "agonda beach",
        "galgibaga beach",
        "colva beach",
        "benaulim beach",
        "varca beach",
        "cavelossim beach",
        "mobor beach",
        "betalbatim beach",
        "majorda beach",
        "utorda beach",
        "velsao beach",
        "cabo de rama fort",
        "butterfly beach",
        "honeymoon beach",
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
    "dining",
    "riverside dining",
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



def repair_geographic_conflicts(
    itinerary: list[dict],
    destination: str,
) -> list[dict]:
    """
    Deterministically repair geographic conflicts for Goa.

    The LLM performs the primary semantic repair. This function is a
    conservative safety net that removes conflicting known-region items.

    Important invariant:
    A deterministic cleanup must never remove every itinerary item from a
    required day. If a repair would empty a day, that repair is skipped and
    the normal validation/refinement loop is allowed to handle the issue.

    The function never invents locations, prices, distances, or other facts.
    """
    if not itinerary:
        return []

    if destination.lower().strip() != "goa":
        return itinerary

    repaired = [dict(item) for item in itinerary]

    def item_area(item: dict) -> str:
        location = item.get("location", "")
        return classify_area(location) if location else "unknown"

    def day_groups(items: list[dict]) -> dict[int, list[dict]]:
        grouped: dict[int, list[dict]] = defaultdict(list)
        for item in items:
            day = item.get("day")
            if day is not None:
                grouped[day].append(item)
        return grouped

    # ------------------------------------------------------------
    # Pass 1: resolve same-day conflicts without emptying a day.
    # ------------------------------------------------------------
    grouped = day_groups(repaired)

    for day, items in grouped.items():
        known_areas = [
            item_area(item)
            for item in items
            if item_area(item) != "unknown"
        ]

        if len(set(known_areas)) <= 1:
            continue

        area_counts = defaultdict(int)
        for area in known_areas:
            area_counts[area] += 1

        primary_area = max(
            area_counts,
            key=area_counts.get,
        )

        candidate = [
            item
            for item in repaired
            if (
                item.get("day") != day
                or item_area(item) in ("unknown", primary_area)
            )
        ]

        # Never turn a required day into an empty day.
        if any(item.get("day") == day for item in candidate):
            repaired = candidate

    # ------------------------------------------------------------
    # Pass 2: resolve disjoint consecutive-day conflicts.
    # Never empty either affected day.
    # ------------------------------------------------------------
    grouped = day_groups(repaired)
    ordered_days = sorted(grouped)

    for previous_day, current_day in zip(
        ordered_days,
        ordered_days[1:],
    ):
        previous_areas = {
            item_area(item)
            for item in grouped[previous_day]
            if item_area(item) != "unknown"
        }
        current_areas = {
            item_area(item)
            for item in grouped[current_day]
            if item_area(item) != "unknown"
        }

        if not previous_areas or not current_areas:
            continue

        if not previous_areas.isdisjoint(current_areas):
            continue

        previous_counts = defaultdict(int)
        current_counts = defaultdict(int)

        for item in grouped[previous_day]:
            area = item_area(item)
            if area != "unknown":
                previous_counts[area] += 1

        for item in grouped[current_day]:
            area = item_area(item)
            if area != "unknown":
                current_counts[area] += 1

        previous_total = sum(previous_counts.values())
        current_total = sum(current_counts.values())

        if previous_total >= current_total:
            keep_area = max(
                previous_counts,
                key=previous_counts.get,
            )
        else:
            keep_area = max(
                current_counts,
                key=current_counts.get,
            )

        affected_days = {previous_day, current_day}

        candidate = [
            item
            for item in repaired
            if (
                item.get("day") not in affected_days
                or item_area(item) in ("unknown", keep_area)
            )
        ]

        # Do not apply a repair that removes every item from either required
        # day. The validator/refinement loop must solve that case semantically.
        candidate_grouped = day_groups(candidate)

        if (
            candidate_grouped.get(previous_day)
            and candidate_grouped.get(current_day)
        ):
            repaired = candidate
            grouped = candidate_grouped

    # ------------------------------------------------------------
    # Pass 3: only remove remaining cross-region items if every day
    # remains represented afterwards.
    # ------------------------------------------------------------
    area_counts = defaultdict(int)

    for item in repaired:
        area = item_area(item)
        if area != "unknown":
            area_counts[area] += 1

    if len(area_counts) > 1:
        primary_area = max(
            area_counts,
            key=area_counts.get,
        )

        candidate = [
            item
            for item in repaired
            if item_area(item) in ("unknown", primary_area)
        ]

        original_days = {
            item.get("day")
            for item in repaired
            if item.get("day") is not None
        }
        candidate_days = {
            item.get("day")
            for item in candidate
            if item.get("day") is not None
        }

        # Preserve exact day coverage. If global cleanup would remove a
        # required day, leave the itinerary untouched for LLM refinement.
        if original_days.issubset(candidate_days):
            repaired = candidate

    return repaired

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

def repair_duplicate_itinerary_places(
    itinerary: list[dict],
) -> list[dict]:
    """
    Deterministically remove later duplicate named places.

    Generic activities are ignored. If removing a duplicate would make a
    day empty, the repair is skipped for that duplicate so day coverage is
    preserved.
    """
    if not itinerary:
        return []

    generic = {
        "check-in", "check in", "check-out", "check out",
        "breakfast", "lunch", "dinner", "dining",
        "free time", "relaxation", "riverside dining",
    }

    result = [dict(item) for item in itinerary]
    seen: dict[str, int] = defaultdict(int)

    for index, item in enumerate(result):
        activity = str(item.get("activity", "")).strip()
        location = str(item.get("location", "")).strip()
        activity_norm = normalize_location(activity)

        if activity_norm in generic:
            candidate = location
        else:
            candidate = activity

        normalized = normalize_place_name(candidate)

        if not normalized or normalized in {"goa", "goa india", "not available"}:
            continue

        tokens = set(normalized.split())
        if tokens and tokens.issubset(GENERIC_PLACE_WORDS):
            continue

        seen[normalized] += 1

        if seen[normalized] <= 1:
            continue

        day = item.get("day")
        day_count = sum(1 for existing in result if existing.get("day") == day)

        if day_count <= 1:
            continue

        # Remove the later duplicate while preserving at least one item
        # on the affected day.
        result[index] = None

    return [
        item for item in result
        if item is not None
    ]


def repair_missing_morning_slots(
    itinerary: list[dict],
    required_duration: int | None = None,
) -> list[dict]:
    """
    Ensure represented trip days have a Morning slot by rescheduling an
    existing item from Afternoon/Evening when possible.

    This function never invents an activity.
    """
    if not itinerary:
        return []

    result = [dict(item) for item in itinerary]
    grouped: dict[int, list[dict]] = defaultdict(list)

    for item in result:
        day = item.get("day")
        if isinstance(day, int):
            grouped[day].append(item)

    target_days = (
        range(1, required_duration + 1)
        if required_duration
        else sorted(grouped)
    )

    for day in target_days:
        day_items = grouped.get(day, [])

        if not day_items:
            # A completely missing day cannot be safely invented here.
            continue

        if any(
            str(item.get("time", "")).strip().lower() == "morning"
            for item in day_items
        ):
            continue

        candidate = next(
            (
                item for item in day_items
                if str(item.get("time", "")).strip().lower()
                in {"afternoon", "evening"}
            ),
            None,
        )

        if candidate is not None:
            candidate["time"] = "Morning"

    return result

