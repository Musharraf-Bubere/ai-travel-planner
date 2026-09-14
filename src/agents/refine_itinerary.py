from langchain_core.messages import HumanMessage

from src.schemas.itinerary import ItineraryAnalysis
from src.services.llm import get_structured_llm
from src.state import TravelState


def build_refinement_prompt(state: TravelState) -> str:
    validation = state.get("validation", {})
    itinerary = state.get("itinerary", {})

    validation_issues = validation.get(
        "issues",
        []
    )

    validation_feedback = validation.get(
        "feedback",
        ""
    )

    return f"""
You are a strict travel itinerary refinement assistant.

Your task is to REPAIR the current itinerary using the validation
feedback and the available research.

You are NOT creating a completely new itinerary unless necessary.

The refined itinerary must directly address EVERY validation issue.

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

DESTINATION:
{state.get("destination_data", {})}

ACCOMMODATION:
{state.get("stay_options", {})}

ACTIVITIES:
{state.get("activities", {})}

WEATHER:
{state.get("weather", {})}

RESTAURANTS:
{state.get("restaurants", {})}

============================================================
CURRENT ITINERARY
============================================================

{itinerary}

============================================================
VALIDATION ISSUES
============================================================

{validation_issues}

============================================================
VALIDATION FEEDBACK
============================================================

{validation_feedback}

============================================================
HARD REFINEMENT REQUIREMENTS
============================================================

1. EVERY VALIDATION ISSUE MUST BE FIXED

You must actively modify the itinerary to resolve every issue listed
in the validation result.

Do not simply preserve an itinerary item that caused a validation issue.

Do not claim that an issue was fixed unless the resulting itinerary
actually satisfies the validation requirement.

------------------------------------------------------------

2. DETERMINISTIC VALIDATION ISSUES ARE HARD CONSTRAINTS

Some validation issues are produced by deterministic programmatic
checks.

These issues MUST be treated as hard constraints.

Do not override them with your own judgment.

For example, if validation reports:

"Day 3 combines locations from multiple geographic areas
(central_goa, south_goa)."

then Day 3 MUST be changed so that the conflicting geographic grouping
is removed.

Do NOT merely state that the itinerary is now geographically grouped.

The actual itinerary must change.

------------------------------------------------------------

3. GEOGRAPHIC REFINEMENT

When a geographic inconsistency is reported:

- Identify the itinerary items responsible for the conflict.
- Keep compatible locations together.
- Move or replace the conflicting item using another researched item
  when appropriate.
- Do not invent a new attraction.
- Do not invent travel distances or travel times.
- Prefer grouping activities from the same geographic area on the same
  day.
- If an item must be removed, replace it only with a researched and
  suitable item.
- If no suitable replacement exists, reduce unnecessary activities
  rather than inventing one.

For a short trip, geographic coherence is more important than keeping
every original activity.

------------------------------------------------------------

4. DUPLICATE-PLACE REFINEMENT

If validation reports a repeated attraction, activity, restaurant, or
other named place:

- Remove the unnecessary repetition.
- Replace it only with a researched alternative when appropriate.
- Do not invent a replacement.

Generic activities such as:

- Breakfast
- Lunch
- Dinner
- Check-in
- Check-out
- Free time
- Relaxation

may repeat when appropriate.

------------------------------------------------------------

5. ACTIVITY GROUNDING

Every actual attraction or activity must come from:

activities.recommended_activities

Do not introduce attractions from general knowledge.

If an activity is not present in the researched activity results,
remove or replace it with a researched activity.

------------------------------------------------------------

6. RESTAURANT GROUNDING

Every named restaurant must come from:

restaurants.recommended_restaurants

Do not introduce restaurants from general knowledge.

If a restaurant is not present in the researched restaurant results,
remove or replace it with a researched restaurant.

------------------------------------------------------------

7. ACCOMMODATION GROUNDING

If a specific accommodation is named, it must come from:

stay_options.accommodation_options

Do not invent accommodation names.

------------------------------------------------------------

8. NO HALLUCINATED FACTS

Do not invent:

- attractions
- restaurants
- hotels
- prices
- ratings
- distances
- travel times
- durations
- weather conditions
- facilities
- factual descriptions

Use only the original travel request and available research.

------------------------------------------------------------

9. UNAVAILABLE INFORMATION

If a research field contains:

- 0.0
- "Not available"
- missing information

do not interpret the value as a confirmed fact.

For example:

Activity cost = 0.0

does NOT mean the activity is free.

It means pricing information may be unavailable.

Similarly, restaurant price_level is a relative price category and
should not be converted into an exact meal price.

------------------------------------------------------------

10. EXACT DURATION

Keep exactly the requested number of days.

Every requested day must be represented.

Do not add extra days.

Do not remove required days.

------------------------------------------------------------

11. PREFERENCE ALIGNMENT

Preserve the traveler's stated preferences where possible:

{", ".join(state.get("preferences", []))}

However, preferences must not override validation requirements.

A valid, grounded itinerary is more important than keeping an
unsupported activity merely because it matches a preference.

------------------------------------------------------------

12. WEATHER

Use the available weather research.

Do not invent weather information.

Avoid unsupported claims that an outdoor activity will definitely have
good weather.

------------------------------------------------------------

13. BUDGET

Keep budget-related statements grounded in the available research.

Do not claim an exact total trip cost unless the available research
supports that calculation.

Do not treat unavailable activity prices as free.

Do not confuse accommodation nightly prices with total trip cost.

------------------------------------------------------------

14. AVOID OVERCROWDING

Do not add activities simply to fill empty time.

Prefer a smaller, realistic itinerary over an overcrowded itinerary.

------------------------------------------------------------

15. PRESERVE VALID INFORMATION

Preserve itinerary items that are already valid when doing so does not
conflict with a validation issue.

Only modify the parts necessary to repair the itinerary.

============================================================
REFINEMENT PROCEDURE
============================================================

Before producing the final itinerary:

STEP 1:
Read every validation issue.

STEP 2:
Identify exactly which itinerary item or items caused each issue.

STEP 3:
Modify those items.

STEP 4:
Check that the modified items use only available research.

STEP 5:
Check geographic consistency again.

STEP 6:
Check duplicate places again.

STEP 7:
Check activity, restaurant, and accommodation grounding again.

STEP 8:
Check that the itinerary still contains exactly the requested number
of days.

STEP 9:
Check that no unsupported facts were introduced.

STEP 10:
Return the repaired itinerary.

IMPORTANT:

Do not output an explanation of what you intended to fix.

The STRUCTURED ITINERARY itself must contain the corrections.

If validation says an item is invalid, the final itinerary must no longer
contain that invalid item unless it has been genuinely corrected.

Return the complete improved itinerary as a structured itinerary
analysis.
"""


def refine_itinerary(state: TravelState) -> TravelState:
    structured_llm = get_structured_llm(
        ItineraryAnalysis
    )

    prompt = build_refinement_prompt(state)

    user_message = HumanMessage(
        content=prompt
    )

    response = structured_llm.invoke(
        [user_message]
    )

    return {
        "itinerary": response.model_dump()
    }