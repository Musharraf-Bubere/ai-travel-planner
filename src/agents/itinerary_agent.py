from langchain_core.messages import HumanMessage

from src.schemas.itinerary import ItineraryAnalysis
from src.services.llm import get_structured_llm
from src.state import TravelState


def build_itinerary_prompt(state: TravelState) -> str:
    return f"""
You are a strict travel itinerary planning assistant.

Create a practical day-by-day itinerary using ONLY the information
available in the provided travel research.

You are responsible for PLANNING, not researching.

Do not introduce information from your general knowledge.

============================================================
TRAVEL REQUEST
============================================================

Destination: {state["destination"]}
Travel Dates: {state.get("travel_dates", "Not specified")}
Duration: {state.get("duration", "Not specified")} days
Travelers: {state.get("travelers", "Not specified")}
Budget: {state.get("budget", "Not specified")}
Preferences: {", ".join(state.get("preferences", []))}

============================================================
DESTINATION RESEARCH
============================================================

{state.get("destination_data", {})}

============================================================
ACCOMMODATION OPTIONS
============================================================

{state.get("stay_options", {})}

============================================================
ACTIVITIES
============================================================

{state.get("activities", {})}

============================================================
WEATHER
============================================================

{state.get("weather", {})}

============================================================
RESTAURANTS
============================================================

{state.get("restaurants", {})}

============================================================
ITINERARY PLANNING RULES
============================================================

1. EXACT DURATION

Create an itinerary for exactly the requested number of days.

Every day from day 1 through the requested duration must be represented.

------------------------------------------------------------

2. STRICT RESEARCH GROUNDING

Use ONLY activities, restaurants, and accommodations present in the
provided research.

Do not invent:

- attractions
- restaurants
- accommodations
- prices
- ratings
- durations
- distances
- travel times
- locations
- amenities
- factual descriptions

If information is unavailable, state that it is unavailable.

------------------------------------------------------------

3. ACTIVITY SELECTION

Select activities that best match the user's preferences.

Prioritize quality and relevance over trying to include every researched
activity.

Do not include an activity merely because it exists in the research.

------------------------------------------------------------

4. GEOGRAPHIC COHERENCE — HARD PLANNING CONSTRAINT

This is a short {state.get("duration", "Not specified")}-day trip.

Geographic coherence is a HARD planning constraint, not merely a
preference.

Before constructing the itinerary, first inspect the geographic
information contained in the research.

Identify the broad geographic regions represented by the researched
locations.

For Goa, when identifiable from the provided locations, treat these as
broad regions:

- North Goa
- Central Goa
- South Goa

The exact location information from the research must be used when
making this determination.

------------------------------------------------------------

5. SELECT A PRIMARY REGION

For a short trip, select ONE primary geographic region that best
supports the user's preferences and the available research.

Prefer the region that:

- contains several suitable researched activities,
- contains suitable researched restaurants,
- aligns with the user's preferences,
- is reasonably compatible with the selected accommodation,
- and minimizes unnecessary geographic movement.

Once a primary region has been selected, prefer researched activities
and restaurants from that region.

Do NOT try to visit North Goa, Central Goa, and South Goa simply because
the research contains options in all three regions.

------------------------------------------------------------

6. DAILY GEOGRAPHIC COHERENCE

Activities and restaurants scheduled on the same day should be
geographically compatible whenever the available location information
allows this to be determined.

Do NOT deliberately combine clearly separated geographic regions on
the same day.

For example, if one day contains South Goa locations, do not add a
Central or North Goa location merely to fill an empty time slot when
another suitable researched option exists.

If there are not enough suitable researched locations in one region,
prefer fewer activities rather than creating unnecessary geographic
movement.

Do NOT invent travel distances or travel times.

------------------------------------------------------------

7. CROSS-REGION MOVEMENT

For a short trip, avoid unnecessary movement between distant regions.

A single transition between regions may be acceptable only when it is
necessary for the itinerary and supported by the available research.

However, repeatedly moving between North, Central, and South Goa across
multiple days is NOT acceptable.

If the available research supports a coherent single-region itinerary,
the itinerary MUST remain within that region.

------------------------------------------------------------

8. ACCOMMODATION

If including check-in or accommodation-related activities, select the
accommodation from the researched accommodation options.

Prefer the accommodation that best matches:

- traveler preferences
- rating
- budget
- location

If the accommodation's exact geographic area is unavailable, do not
invent its location.

Do not invent accommodation details.

------------------------------------------------------------

9. RESTAURANTS

Use only restaurants present in the restaurant research.

Prefer restaurants that:

- match the traveler's food preferences,
- fit the selected itinerary region where possible,
- are geographically compatible with the day's activities,
- have useful research information,
- and provide variety across the trip.

Do not select a restaurant from a distant region merely because it has
a high rating when a suitable researched restaurant exists closer to
the selected itinerary region.

Do not invent restaurant names or details.

------------------------------------------------------------

10. WEATHER

Use the provided weather research when deciding when to schedule
outdoor activities.

If rain probability or unfavorable weather is present, provide flexible
planning such as indoor dining or relaxation alternatives.

Do not claim that weather will definitely be favorable.

Do not invent weather information.

------------------------------------------------------------

11. USER PREFERENCES

The user's preferences are:

{", ".join(state.get("preferences", []))}

The itinerary should clearly reflect these preferences.

For this trip, prioritize the user's preferences over unrelated
activities.

However, preferences must not override grounding or geographic
constraints.

------------------------------------------------------------

12. AVOID OVERCROWDING

Keep the itinerary realistic.

Do not fill every available time slot simply because research contains
many options.

Prefer a small number of meaningful activities each day.

Allow reasonable time for:

- meals
- relaxation
- transitions
- weather changes
- check-in/check-out

Do not invent exact transition times.

------------------------------------------------------------

13. BUDGET

The total trip budget is:

{state.get("budget", "Not specified")}

Do NOT claim that the complete trip is within budget unless the
available research actually supports that conclusion.

Important:

- An activity cost of 0.0 may mean pricing information is unavailable.
- A restaurant price level is not an exact meal price.
- Accommodation nightly rates do not represent the complete trip cost.

Therefore, if the complete trip cost cannot be reliably calculated,
state that the final total cost is unavailable and provide a cautious
budget assessment instead.

Never interpret unavailable pricing as free.

------------------------------------------------------------

14. DESCRIPTIONS

Every description must be based only on the corresponding research.

Do not add unsupported claims about:

- facilities
- atmosphere
- accessibility
- travel duration
- ticket prices
- opening hours
- transportation
- popularity
- reservations

unless that information exists in the provided research.

------------------------------------------------------------

15. REQUIRED ITEM FIELDS

For every itinerary item provide:

- day
- time
- activity
- location
- description

------------------------------------------------------------

16. PLANNING NOTES

Planning notes should summarize only information supported by:

- destination research
- accommodation research
- activity research
- restaurant research
- weather research
- original travel request

Do not introduce new factual claims.

============================================================
MANDATORY PLANNING PROCEDURE
============================================================

Before producing the final structured itinerary, internally perform
these planning steps:

STEP 1 — IDENTIFY REGIONS

Determine the broad geographic region of each researched activity and
restaurant from the available location information.

Do not invent geographic information.

STEP 2 — SELECT PRIMARY REGION

Select the single region that provides the strongest combination of:

- user preference alignment,
- researched activities,
- researched restaurants,
- accommodation compatibility,
- and geographic coherence.

STEP 3 — SELECT ACTIVITIES

Select activities primarily from the chosen region.

Do not select distant activities merely because they are available in
the research.

STEP 4 — SELECT RESTAURANTS

Select restaurants that are geographically compatible with the chosen
region and the day's activities.

STEP 5 — BUILD DAILY GROUPS

Group activities and restaurants into days so that each day remains
geographically coherent.

STEP 6 — CHECK CROSS-REGION MOVEMENT

Before returning the itinerary, inspect every day.

If a day combines clearly separated geographic regions, change the
itinerary.

Remove or replace the conflicting item using another researched option
when possible.

If no suitable replacement exists, prefer fewer activities.

STEP 7 — FINAL GROUNDING CHECK

Before returning the itinerary, verify that every:

- activity
- restaurant
- accommodation

comes from the supplied research.

STEP 8 — FINAL DURATION CHECK

Verify that every requested day is present and that the itinerary has
exactly the requested duration.

============================================================
FINAL OBJECTIVE
============================================================

Generate the most practical itinerary possible for this traveler.

The priority order is:

1. Research grounding
2. Geographic coherence
3. Exact duration
4. User preference alignment
5. Weather suitability
6. Realistic pacing
7. Budget consistency

A simple, geographically coherent itinerary is better than a larger
itinerary containing unnecessary cross-region travel.

Do not add an item simply because it makes the itinerary look fuller.

Return a structured itinerary analysis.
"""


def itinerary_agent(state: TravelState) -> TravelState:
    structured_llm = get_structured_llm(
        ItineraryAnalysis
    )

    prompt = build_itinerary_prompt(state)

    user_message = HumanMessage(
        content=prompt
    )

    response = structured_llm.invoke(
        [user_message]
    )

    return {
        "itinerary": response.model_dump()
    }