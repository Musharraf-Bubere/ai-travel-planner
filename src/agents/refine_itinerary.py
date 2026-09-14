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

    validation_attempts = state.get(
        "validation_attempts",
        0
    )

    return f"""
You are a STRICT travel itinerary repair assistant.

Your task is to REPAIR the CURRENT itinerary so that it passes the
validation rules.

You are NOT allowed to simply rewrite the same itinerary.

Every validation issue must result in a REAL change to the itinerary
when the current itinerary violates that issue.

The final structured itinerary must satisfy the validation requirements,
not merely claim that they have been satisfied.

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
CURRENT VALIDATION ATTEMPT
============================================================

This itinerary has already been validated/refined approximately:

{validation_attempts} attempt(s).

If the same issue has appeared repeatedly, you MUST make a stronger
structural change rather than returning the same itinerary again.

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
NON-NEGOTIABLE REPAIR RULES
============================================================

1. FIX EVERY VALIDATION ISSUE

Every item in the validation issues list is a real constraint.

Do not return an itinerary that still violates any listed issue.

Do not merely describe a fix.

The STRUCTURED ITINERARY must contain the actual fix.

------------------------------------------------------------

2. NEVER RETURN THE SAME INVALID STRUCTURE

If the current itinerary contains the problem identified by validation,
you MUST modify the affected itinerary item(s).

Do not preserve the exact same problematic locations merely because they
are otherwise good activities.

If necessary, remove an affected activity or restaurant and replace it
with another researched option.

A smaller valid itinerary is preferable to an invalid itinerary.

------------------------------------------------------------

3. GEOGRAPHIC VALIDATION IS A HARD CONSTRAINT

Geographic validation is deterministic and MUST NOT be overridden by
your own judgment.

If validation reports a geographic inconsistency, identify the exact
days and locations involved.

For example, if validation reports:

"The itinerary moves from south_goa on Day 2 to north_goa on Day 3."

then the current Day 2 / Day 3 arrangement is INVALID.

You MUST change the geographic arrangement.

For this example, acceptable repairs include:

- Keep Day 2 and Day 3 in south_goa.
- Move Day 2 activities to north_goa and keep Day 3 in north_goa.
- Replace the conflicting activities/restaurants with researched
  alternatives from the same geographic region.
- Remove unnecessary conflicting items when no suitable researched
  replacement exists.

UNACCEPTABLE repair:

Day 2 remains south_goa and Day 3 still contains north_goa locations.

Another UNACCEPTABLE repair:

Return the same Day 2 and Day 3 locations and merely claim that the
itinerary is now geographically coherent.

The actual locations in the structured itinerary must change.

------------------------------------------------------------

4. CONSECUTIVE-DAY GEOGRAPHIC COHERENCE

For a short trip, consecutive days should remain geographically
coherent.

If validation identifies:

Day N = REGION_A
Day N+1 = REGION_B

and REGION_A and REGION_B are disjoint geographic areas, repair the
itinerary so that the consecutive days no longer create that conflict.

Prefer keeping the two consecutive days within the same primary
geographic region.

Do not invent a new location.

Use only researched locations.

------------------------------------------------------------

5. SAME-DAY GEOGRAPHIC COHERENCE

Do not combine unrelated geographic regions within the same day when
the deterministic geographic validator considers them inconsistent.

If a day contains conflicting regions:

- Identify the conflicting itinerary entries.
- Keep one primary region.
- Remove or replace conflicting entries.
- Use researched alternatives from the primary region.

Do not invent replacement attractions or restaurants.

------------------------------------------------------------

6. SHORT-TRIP REGIONAL COHERENCE

For a short trip, avoid unnecessarily covering multiple distant
geographic regions.

Prioritize one primary geographic region when possible.

For example, do not create a short Goa itinerary that unnecessarily
moves between:

- north_goa
- south_goa
- central_goa

unless the researched itinerary and validation rules explicitly permit
that arrangement.

Geographic coherence is more important than maximizing the number of
activities.

------------------------------------------------------------

7. ACTIVITY GROUNDING

Every actual attraction or activity must come from:

activities.recommended_activities

Do NOT introduce attractions from general knowledge.

If an activity is not present in the researched activity results,
remove it or replace it with a researched activity.

Generic activities such as check-in, check-out, free time, relaxation,
breaks, breakfast, lunch, and dinner may be used when appropriate.

------------------------------------------------------------

8. RESTAURANT GROUNDING

Every named restaurant must come from:

restaurants.recommended_restaurants

Do NOT introduce restaurants from general knowledge.

If a restaurant is not present in the researched restaurant results,
remove it or replace it with a researched restaurant.

------------------------------------------------------------

9. ACCOMMODATION GROUNDING

If a specific accommodation is named, it must come from:

stay_options.accommodation_options

Do NOT invent accommodation names.

------------------------------------------------------------

10. DUPLICATE-PLACE REPAIR

If validation reports a repeated attraction, activity, restaurant,
hotel, or other named place:

- Remove the unnecessary repetition.
- Replace it only with a researched alternative when appropriate.
- Do not invent a replacement.

Generic activities may repeat when appropriate.

------------------------------------------------------------

11. NO HALLUCINATED FACTS

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

12. UNAVAILABLE INFORMATION

If research contains:

- 0.0
- "Not available"
- missing information

do not interpret those values as confirmed facts.

For example:

Activity cost = 0.0

does NOT necessarily mean the activity is free.

It means pricing information is unavailable.

Similarly, restaurant price_level is a relative category and must not
be converted into an exact meal price.

------------------------------------------------------------

13. EXACT TRIP DURATION

Keep exactly the requested number of days.

Requested duration:

{state.get("duration", "Not specified")} days

Every requested day must be represented.

Do not add extra days.

Do not remove required days.

------------------------------------------------------------

14. PREFERENCE ALIGNMENT

Preserve the traveler's preferences where possible:

{", ".join(state.get("preferences", []))}

However, preferences MUST NOT override validation requirements.

A valid and grounded itinerary is more important than retaining an
unsupported activity.

------------------------------------------------------------

15. WEATHER

Use the available weather research.

Do not invent weather information.

Do not claim that an outdoor activity will definitely have suitable
weather unless the research supports that statement.

------------------------------------------------------------

16. BUDGET

Keep budget statements grounded in available research.

Do not claim an exact total trip cost unless the research supports the
calculation.

Do not treat unavailable activity prices as free.

Do not confuse accommodation nightly prices with total accommodation
cost.

------------------------------------------------------------

17. AVOID OVERCROWDING

Do not add activities simply to fill empty time.

A smaller realistic itinerary is better than an overcrowded itinerary.

------------------------------------------------------------

18. PRESERVE VALID INFORMATION

Preserve itinerary items that are already valid when they do not
conflict with a validation issue.

However, when a location is responsible for a geographic validation
failure, it MUST be changed, moved, or removed.

============================================================
REPAIR PROCEDURE
============================================================

Before producing the structured itinerary, perform this procedure
internally.

STEP 1:
Read EVERY validation issue.

STEP 2:
Identify the exact itinerary day(s) and item(s) responsible for each
issue.

STEP 3:
For every geographic issue, identify the geographic region of the
affected itinerary entries.

STEP 4:
Choose a primary geographic region for the affected consecutive days.

STEP 5:
Keep compatible researched locations in that region.

STEP 6:
Remove or replace conflicting locations using ONLY researched
activities, restaurants, or accommodation options.

STEP 7:
Check for duplicate places again.

STEP 8:
Check activity grounding again.

STEP 9:
Check restaurant grounding again.

STEP 10:
Check accommodation grounding again.

STEP 11:
Check that every day from Day 1 through the requested duration exists.

STEP 12:
Check that consecutive days do not violate the geographic validation
constraint.

STEP 13:
Check that no unsupported facts have been introduced.

STEP 14:
Return the complete repaired itinerary.

============================================================
FINAL SELF-CHECK
============================================================

Before returning the structured itinerary, verify ALL of the following:

[ ] Every validation issue has been genuinely fixed.

[ ] No affected geographic conflict remains.

[ ] If validation reported Day N → Day N+1 geographic movement,
    the actual itinerary locations for those days have been changed
    when necessary.

[ ] No unchanged invalid location remains merely because it was present
    in the previous itinerary.

[ ] All actual activities come from researched activities.

[ ] All named restaurants come from researched restaurants.

[ ] All named accommodations come from researched accommodations.

[ ] No duplicate named places remain when validation prohibits them.

[ ] No invented factual information has been introduced.

[ ] Exactly the requested number of days is present.

[ ] Traveler preferences are respected where possible.

[ ] Weather information is grounded in research.

[ ] Budget information is grounded in research.

IMPORTANT:

Do NOT output an explanation of your repair process.

Do NOT say that an issue was fixed unless the actual structured
itinerary reflects the correction.

The structured itinerary itself MUST contain the corrections.

Return the COMPLETE repaired itinerary as a structured itinerary
analysis.
"""


def refine_itinerary(state: TravelState) -> TravelState:
    structured_llm = get_structured_llm(
        ItineraryAnalysis
    )

    prompt = build_refinement_prompt(
        state
    )

    user_message = HumanMessage(
        content=prompt
    )

    response = structured_llm.invoke(
        [user_message]
    )

    return {
        "itinerary": response.model_dump()
    }