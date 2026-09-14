from langchain_core.messages import HumanMessage

from src.schemas.validation import ItineraryValidation
from src.services.llm import get_structured_llm
from src.state import TravelState
from src.utils.itinerary_checks import (
    find_duplicate_itinerary_places,
    find_geographic_inconsistencies,
    find_ungrounded_itinerary_places,
)


def build_validation_prompt(state: TravelState) -> str:
    return f"""
You are a strict itinerary validation assistant.

Your job is to validate the generated itinerary against the ORIGINAL
TRAVEL REQUEST and the AVAILABLE RESEARCH.

You are a validator, not a travel planner.

Do NOT add new attractions, restaurants, accommodations, prices,
distances, durations, or other factual information.

Do NOT assume that an itinerary item is valid simply because it sounds
reasonable for the destination.

============================================================
ORIGINAL TRAVEL REQUEST
============================================================

Destination: {state["destination"]}
Travel Dates: {state.get("travel_dates", "Not specified")}
Duration: {state.get("duration", "Not specified")} days
Travelers: {state.get("travelers", "Not specified")}
Budget: {state.get("budget", "Not specified")}
Preferences: {", ".join(state.get("preferences", []))}

============================================================
AVAILABLE RESEARCH
============================================================

DESTINATION RESEARCH:
{state.get("destination_data", {})}

ACCOMMODATION RESEARCH:
{state.get("stay_options", {})}

ACTIVITY RESEARCH:
{state.get("activities", {})}

WEATHER RESEARCH:
{state.get("weather", {})}

RESTAURANT RESEARCH:
{state.get("restaurants", {})}

============================================================
GENERATED ITINERARY
============================================================

{state.get("itinerary", {})}

============================================================
STRICT VALIDATION RULES
============================================================

1. EXACT DURATION

The itinerary must contain exactly the requested number of days.

Every day from day 1 through the requested duration must be represented.

If a day is missing, duplicated incorrectly, or the duration is wrong,
the itinerary is INVALID.

------------------------------------------------------------

2. ACTIVITY GROUNDING

Every actual attraction or activity in the itinerary must be traceable
to the researched activity results.

Compare the itinerary activity/location against:

activities.recommended_activities

Do not accept an activity merely because it is a well-known attraction
in the destination.

If an attraction is not present in the researched activity results,
mark the itinerary INVALID and identify the unsupported item.

------------------------------------------------------------

3. RESTAURANT GROUNDING

Every restaurant named in the itinerary must be traceable to the
researched restaurant results.

Compare restaurant names against:

restaurants.recommended_restaurants

Do not accept restaurants based on general knowledge.

If a restaurant is not present in the researched restaurant results,
mark the itinerary INVALID and identify the unsupported restaurant.

------------------------------------------------------------

4. ACCOMMODATION GROUNDING

If a specific accommodation is named in the itinerary, it must be
present in:

stay_options.accommodation_options

Do not accept a hotel or accommodation merely because it sounds
appropriate for the destination.

If a specific accommodation is named but cannot be found in the
research, mark the itinerary INVALID.

------------------------------------------------------------

5. NO INVENTED FACTS

Check descriptions, prices, ratings, durations, locations, and other
factual claims.

A statement should only be accepted when it is supported by the
available research or by the original travel request.

Do not treat model-generated assumptions as research evidence.

------------------------------------------------------------

6. UNAVAILABLE DATA

A value of 0.0 for an activity cost means that pricing information may
be unavailable.

Do NOT interpret 0.0 as proof that an activity is free.

Similarly, "Not available" means the source did not provide that
information.

Do not allow unsupported claims based on unavailable fields.

------------------------------------------------------------

7. WEATHER CONSISTENCY

Compare outdoor activities with the available weather research.

The itinerary does not need to avoid all outdoor activities when
weather is unfavorable.

However, it should not make unsupported claims that weather conditions
will definitely be favorable.

Weather-dependent activities should acknowledge relevant weather
limitations when necessary.

------------------------------------------------------------

8. PREFERENCE ALIGNMENT

The itinerary should reasonably reflect the user's stated preferences.

For this request, evaluate alignment with:

{", ".join(state.get("preferences", []))}

Do not require every itinerary item to satisfy every preference.

Evaluate the overall trip rather than individual items in isolation.

------------------------------------------------------------

9. BUDGET CONSISTENCY

Check whether budget-related claims are supported by the available
research.

Do not assume that a total trip budget is sufficient merely because
individual accommodation or restaurant prices appear low.

If exact total trip costs cannot be calculated from the available
research, the itinerary should avoid claiming an exact total cost.

Do not treat unavailable activity pricing as free.

------------------------------------------------------------

10. GEOGRAPHIC EFFICIENCY

Evaluate whether the itinerary unnecessarily moves between distant
areas of the destination.

Use locations explicitly present in the research.

Flag clearly inefficient geographic planning when the itinerary places
multiple geographically separated locations into the same day or causes
unnecessary travel for a short trip.

Do NOT invent travel times or distances when they are not present in the
research.

If geographic efficiency cannot be reliably determined from the
available information, mention the limitation rather than assuming the
itinerary is efficient.

------------------------------------------------------------

11. DUPLICATE PLACES

Avoid unnecessarily repeating the same attraction or activity on
multiple days.

If the same named attraction or activity appears on multiple days,
flag it as a validation issue unless repetition is clearly justified
by the original travel request.

Generic activities such as:

- Check-in
- Check-out
- Breakfast
- Lunch
- Dinner
- Free time
- Relaxation

should not be considered duplicate places merely because they appear
multiple times.

------------------------------------------------------------

12. OVERCROWDING

Check whether the number of activities and transitions is reasonable
for the requested duration.

Do not automatically reject an itinerary because it contains several
items.

Reject or flag it only when the schedule appears unnecessarily
overcrowded or unrealistic based on the information available.

------------------------------------------------------------

13. REQUIRED FIELDS

Every itinerary item must contain:

- day
- time
- activity
- location
- description

If any required field is missing, the itinerary is INVALID.

------------------------------------------------------------

14. PRESERVE VALID INFORMATION

If most of the itinerary is valid but one or more items violate the
rules, identify the specific invalid items.

Do not mark the entire itinerary invalid without explaining the exact
problem.

============================================================
VALIDATION DECISION
============================================================

Set is_valid to TRUE only when:

- the requested number of days is correct,
- activities are grounded in the activity research,
- restaurants are grounded in the restaurant research,
- named accommodation is grounded in accommodation research,
- there are no unsupported factual claims that materially affect the
  itinerary,
- weather considerations are reasonable,
- preferences are reasonably satisfied,
- budget claims are supported,
- geographic planning is reasonably efficient based on available data,
- unnecessary duplicate attractions are avoided,
- the itinerary is not unnecessarily overcrowded,
- and all required fields are present.

Set is_valid to FALSE when one or more important validation rules fail.

The issues list must contain specific problems.

The feedback must briefly explain why the itinerary passed or what
must be corrected.

Return a structured itinerary validation.
"""


def itinerary_validator(state: TravelState) -> TravelState:
    """
    Validate the itinerary using:

    1. LLM-based semantic validation
    2. Deterministic geographic validation
    3. Deterministic duplicate-place validation
    4. Deterministic research-grounding validation

    The itinerary is considered valid only when the LLM validation
    passes and all deterministic validation checks pass.
    """

    structured_llm = get_structured_llm(
        ItineraryValidation
    )

    prompt = build_validation_prompt(state)

    user_message = HumanMessage(
        content=prompt
    )

    response = structured_llm.invoke(
        [user_message]
    )

    # ------------------------------------------------------------
    # Extract itinerary
    # ------------------------------------------------------------

    itinerary = state.get(
        "itinerary",
        {}
    )

    itinerary_items = itinerary.get(
        "itinerary",
        []
    )

    # ------------------------------------------------------------
    # Extract research data
    # ------------------------------------------------------------

    activities = state.get(
        "activities",
        {}
    )

    restaurants = state.get(
        "restaurants",
        {}
    )

    stay_options = state.get(
        "stay_options",
        {}
    )

    # ------------------------------------------------------------
    # Deterministic geographic validation
    # ------------------------------------------------------------

    geographic_issues = find_geographic_inconsistencies(
        itinerary_items,
        state["destination"],
    )

    # ------------------------------------------------------------
    # Deterministic duplicate-place validation
    # ------------------------------------------------------------

    duplicate_place_issues = find_duplicate_itinerary_places(
        itinerary_items
    )

    # ------------------------------------------------------------
    # Deterministic research-grounding validation
    # ------------------------------------------------------------

    grounding_issues = find_ungrounded_itinerary_places(
        itinerary_items,
        activities,
        restaurants,
        stay_options,
    )

    # ------------------------------------------------------------
    # Combine LLM and deterministic validation
    # ------------------------------------------------------------

    issues = list(response.issues)

    if geographic_issues:
        issues.extend(
            geographic_issues
        )

    if duplicate_place_issues:
        issues.extend(
            duplicate_place_issues
        )

    if grounding_issues:
        issues.extend(
            grounding_issues
        )

    # ------------------------------------------------------------
    # Final validation decision
    # ------------------------------------------------------------

    is_valid = (
        response.is_valid
        and not geographic_issues
        and not duplicate_place_issues
        and not grounding_issues
    )

    # ------------------------------------------------------------
    # Build combined feedback
    # ------------------------------------------------------------

    feedback = response.feedback

    additional_issues = (
        geographic_issues
        + duplicate_place_issues
        + grounding_issues
    )

    if additional_issues:
        feedback = (
            f"{feedback} "
            f"Deterministic validation also found: "
            f"{' '.join(additional_issues)}"
        )

    # ------------------------------------------------------------
    # Return validation result
    # ------------------------------------------------------------

    return {
        "validation": {
            "is_valid": is_valid,
            "issues": issues,
            "feedback": feedback,
        },
        "validation_attempts": (
            state.get("validation_attempts", 0) + 1
        ),
    }