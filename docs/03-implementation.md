# AI Travel Planner — Implementation

## 1. Purpose

This document records the implementation completed so far for the **AI Travel Planner — Multi-Agent Travel Planning System**.

The current implementation focuses on establishing the project's core foundation:

- Python project environment
- Shared travel state
- LangGraph workflow
- Destination Agent
- Google Gemini integration
- Environment-based configuration
- LLM-powered destination analysis
- Prompt construction separation
- Automated testing

Only functionality that has actually been implemented is documented here.

---

## 2. Current Implementation

The current implementation contains five specialist travel agents:

- Destination Agent
- Stay Agent
- Activity Agent
- Weather Agent
- Food Agent

The current workflow is sequential while the parallel, conditional, and iterative workflow stages are being developed.

Current implemented flow:

    User Input
        ↓
    TravelState
        ↓
    LangGraph
        ↓
    Destination Agent
        ↓
    Stay Agent
        ↓
    Activity Agent
        ↓
    Weather Agent
        ↓
    Food Agent
        ↓
    Updated TravelState

The Destination Agent uses real Tavily web research.

The Stay Agent uses real SerpApi Google Hotels data.

The Activity Agent uses real SerpApi Google Maps data for activity and attraction discovery.

The Weather Agent uses real WeatherAPI.com forecast data.

The Food Agent uses real SerpApi Google Maps restaurant data.

The Itinerary Agent and Final Response Agent have not yet been implemented.

## 3. Project Environment

A Python virtual environment is used to isolate the project's dependencies.

    ai-travel-planner/
    └── venv/

The project currently uses Python 3.14.6.

The virtual environment is activated before running the project or tests.

Example:

    (venv) PS D:\ai-travel-planner>

---

## 4. Dependencies

The project dependencies are maintained in `requirements.txt`.

Current runtime dependencies include:

    langgraph
    langchain
    langchain-google-genai
    python-dotenv
    pydantic
    requests
    tavily-python

Pytest is also installed in the project environment for automated testing.

Current external services:

- Google Gemini for LLM operations
- Tavily for destination web research
- SerpApi Google Hotels for accommodation search
- SerpApi Google Maps for activity and attraction search
- WeatherAPI.com for weather forecasts
- SerpApi Google Maps for restaurant search

The same `SERPAPI_API_KEY` is reused for Stay, Activity, and Food integrations.

## 5. Shared Travel State

The project uses `TypedDict` to define the shared state passed between LangGraph nodes and agents.

File:

    src/state.py

Current state structure:

    class TravelState(TypedDict, total=False):
        # User input
        destination: str
        travel_dates: str
        duration: int
        travelers: int
        budget: float
        preferences: list[str]

        # Agent outputs
        destination_data: DestinationAnalysis
        stay_options: StayAnalysis
        activities: ActivityAnalysis
        weather: WeatherAnalysis
        restaurants: FoodAnalysis
        itinerary: dict

### Purpose

`TravelState` provides the common communication layer between specialist agents.

It contains:

### User Input

- Destination
- Travel dates
- Duration
- Number of travelers
- Budget
- Preferences

### Agent Outputs

- Destination analysis
- Accommodation analysis
- Activity analysis
- Weather analysis
- Restaurant analysis
- Itinerary

The specialist outputs are defined using Pydantic models.

The current agent implementations serialize the Pydantic results with `model_dump()` before storing them in the shared state.

This keeps the agent communication predictable while preserving a common workflow state.

## 6. LangGraph Workflow

The project uses LangGraph to orchestrate the specialist travel agents.

File:

    src/graph/travel_graph.py

### Current Sequential Workflow

    START
      ↓
    Destination Agent
      ↓
    Stay Agent
      ↓
    Activity Agent
      ↓
    Weather Agent
      ↓
    Food Agent
      ↓
    END

The current graph is intentionally sequential and acts as the stable baseline for the final hybrid architecture.

### Role of LangGraph

LangGraph manages:

- Shared `TravelState`
- Agent nodes
- Workflow edges
- Execution order
- Future parallel execution
- Future conditional routing
- Future iterative refinement

### Final Hybrid Workflow

The final system is designed to demonstrate all four workflow patterns:

- Sequential
- Parallel
- Conditional
- Iterative

Target architecture:

                         USER
                           │
                           ▼
                    ┌─────────────┐
                    │   FastAPI   │
                    └──────┬──────┘
                           │
                           ▼
                    ┌─────────────┐
                    │  LangGraph  │
                    │ Orchestrator│
                    └──────┬──────┘
                           │
                           ▼
                 ┌───────────────────┐
                 │ Destination Agent │
                 │ + Research Tool   │
                 └─────────┬─────────┘
                           │
                           ▼
                    Destination Data
                           │
              ┌────────────┼────────────┐
              │            │            │
              ▼            ▼            ▼
          Stay Agent   Activity Agent  Weather Agent
              │            │            │
              └────────────┼────────────┘
                           │
                     PARALLEL JOIN
                           │
                           ▼
                      Food Agent
                           │
                           ▼
                 ┌──────────────────┐
                 │ Itinerary Agent  │
                 └────────┬─────────┘
                          │
                          ▼
                 Itinerary Validation
                          │
                    ┌─────┴─────┐
                    │           │
                  Valid       Invalid
                    │           │
                    │           ▼
                    │      Refine Itinerary
                    │           │
                    │           └──────► Validator
                    │
                    ▼
              Final Response Agent
                    │
                    ▼
              FINAL TRAVEL PLAN
                    │
                    ▼
                 Streamlit
                    │
                    ▼
                   USER

The parallel, conditional, and iterative portions are planned next and are not yet represented by the current graph code.

## 7. Destination Agent

The first implemented agent is the Destination Agent.

File:

    src/agents/destination_agent.py

The Destination Agent is responsible for:

1. Reading travel information from `TravelState`
2. Building a destination research prompt
3. Obtaining the configured LLM
4. Invoking Gemini
5. Storing the generated analysis in `TravelState`

Current flow:

    TravelState
        ↓
    Destination Agent
        ↓
    Build Prompt
        ↓
    Gemini 3.5 Flash-Lite
        ↓
    Generated Analysis
        ↓
    destination_data

---

## 8. Destination Prompt Construction

Prompt construction has been separated into its own function:

    build_destination_prompt(state)

This function receives the current `TravelState` and constructs a prompt containing:

- Destination
- Duration
- Number of travelers
- Budget
- Preferences

The prompt asks Gemini to provide a concise destination overview covering:

1. Why the destination is suitable for the trip
2. Recommended areas to explore
3. Important travel considerations
4. Suggestions based on the traveler's preferences

This separation keeps prompt construction independent from the main agent execution logic.

---

## 9. LLM-Powered Destination Analysis

The Destination Agent now invokes the Gemini model using the shared LLM service.

The response is obtained using:

    response = llm.invoke(prompt)

The generated content is then stored in the shared state:

    state["destination_data"] = {
        "analysis": response.content
    }

This means the Destination Agent is now genuinely LLM-powered rather than returning a hard-coded placeholder message.

---

## 10. LLM Service

Google Gemini has been integrated through LangChain.

File:

    src/services/llm.py

The project currently uses:

    gemini-3.5-flash-lite

The integration uses:

    ChatGoogleGenerativeAI

The API key is loaded from environment variables using `python-dotenv`.

Current environment configuration:

    GOOGLE_API_KEY=<your-api-key>
    GEMINI_MODEL=gemini-3.5-flash-lite

The actual API key must never be committed to Git.

---

## 11. Environment-Based Model Configuration

The Gemini model name is configured through the environment rather than being hard-coded inside the LLM creation function.

The service reads:

    GEMINI_MODEL

from the environment.

A default model is provided:

    gemini-3.5-flash-lite

This allows the model to be changed without modifying the Python implementation.

Current configuration flow:

    .env
      │
      ├── GOOGLE_API_KEY
      │
      └── GEMINI_MODEL
              │
              ▼
        src/services/llm.py
              │
              ▼
    ChatGoogleGenerativeAI
              │
              ▼
    Gemini 3.5 Flash-Lite

---

## 12. API Key Validation

The LLM service checks whether `GOOGLE_API_KEY` is available.

If the API key is missing, the service raises:

    ValueError("GOOGLE_API_KEY is not set in the environment.")

This prevents the application from attempting to create the Gemini client without the required credentials.

---

## 13. LLM Service and Agent Separation

The project intentionally separates the LLM service from agent behavior.

### LLM Service

Responsible for:

- Loading configuration
- Validating the API key
- Creating the Gemini model client

### Destination Agent

Responsible for:

- Understanding the travel state
- Constructing the task-specific prompt
- Invoking the LLM
- Processing the response
- Updating the shared state

Architecture:

    Destination Agent
          │
          ▼
       get_llm()
          │
          ▼
    LLM Service
          │
          ▼
    Gemini 3.5 Flash-Lite

This separation will support the future LLM abstraction layer.

---

## 14. Testing

The project uses Pytest for automated testing.

Current test files:

    tests/
    ├── test_state.py
    ├── test_graph.py
    └── test_llm.py

---

## 15. State Test

File:

    tests/test_state.py

The state test verifies that `TravelState` can contain the expected travel information.

It currently checks values such as:

- Destination
- Duration
- Travelers
- Budget
- Preferences

---

## 16. Graph Test

File:

    tests/test_graph.py

The graph test verifies that:

1. The LangGraph workflow can be built.
2. The initial travel state can be passed into the graph.
3. The Destination Agent executes.
4. The destination remains available.
5. Gemini-generated analysis is stored in `destination_data`.

The test verifies the presence of generated analysis rather than matching exact LLM wording.

Current assertion:

    assert result["destination_data"]["analysis"]

This is important because LLM responses can vary between invocations.

---

## 17. LLM Connection Test

File:

    tests/test_llm.py

The LLM test verifies that:

1. The Gemini model can be created.
2. The configured API key is accepted.
3. Gemini can successfully process a prompt.
4. The response contains generated content.

The test uses:

    response = llm.invoke(
        "Say hello in one short sentence."
    )

The test currently passes successfully with:

    gemini-3.5-flash-lite

---

## 18. Current Test Result

The complete test suite was executed using:

    python -m pytest -v

Current result:

    3 passed, 1 warning

Tests:

    test_graph.py::test_travel_graph PASSED
    test_llm.py::test_llm_connection PASSED
    test_state.py::test_travel_state PASSED

The warning originates from a dependency used by the Google GenAI library and does not currently indicate a failure in the project code.

---

## 19. Current Project Structure

The current implementation structure includes specialist agents, schemas, tools, graph orchestration, services, tests, and documentation.

    ai-travel-planner/
    │
    ├── docs/
    │   ├── 01-project-overview.md
    │   ├── 02-research.md
    │   └── 03-implementation.md
    │
    ├── src/
    │   ├── __init__.py
    │   ├── state.py
    │   │
    │   ├── agents/
    │   │   ├── __init__.py
    │   │   ├── destination_agent.py
    │   │   ├── stay_agent.py
    │   │   ├── activity_agent.py
    │   │   ├── weather_agent.py
    │   │   └── food_agent.py
    │   │
    │   ├── graph/
    │   │   ├── __init__.py
    │   │   └── travel_graph.py
    │   │
    │   ├── schemas/
    │   │   ├── destination.py
    │   │   ├── stay.py
    │   │   ├── activity.py
    │   │   ├── weather.py
    │   │   └── food.py
    │   │
    │   ├── services/
    │   │   ├── __init__.py
    │   │   └── llm.py
    │   │
    │   └── tools/
    │       ├── destination.py
    │       ├── accommodation.py
    │       ├── activity.py
    │       ├── weather.py
    │       └── food.py
    │
    ├── tests/
    │   ├── test_state.py
    │   ├── test_graph.py
    │   ├── test_llm.py
    │   ├── test_destination_schema.py
    │   ├── test_accommodation_tool.py
    │   ├── test_stay_schema.py
    │   ├── test_weather_tool.py
    │   ├── test_weather_schema.py
    │   ├── test_weather_agent.py
    │   ├── test_food_schema.py
    │   ├── test_food_tool.py
    │   └── test_food_agent.py
    │
    ├── .gitignore
    ├── README.md
    └── requirements.txt

The Activity Agent currently has been validated through direct tool and agent execution. A dedicated automated Activity test file can be added as part of the next testing/refactoring pass.

## 20. Current Architecture

The current implementation can be represented as:

    User Travel Information
            │
            ▼
        TravelState
            │
            ▼
        LangGraph
            │
            ▼
    Destination Agent
            │
            ├── Tavily Research Tool
            │
            ▼
    DestinationAnalysis
            │
            ▼
        Stay Agent
            │
            ├── SerpApi Google Hotels
            │
            ▼
        StayAnalysis
            │
            ▼
    Activity Agent
            │
            ├── SerpApi Google Maps
            │
            ▼
    ActivityAnalysis
            │
            ▼
    Weather Agent
            │
            ├── WeatherAPI.com
            │
            ▼
    WeatherAnalysis
            │
            ▼
        Food Agent
            │
            ├── SerpApi Google Maps
            │
            ▼
        FoodAnalysis
            │
            ▼
        TravelState

The current graph is sequential. The final architecture will introduce parallel execution, conditional routing, and iterative itinerary refinement.

## 21. Current Capabilities

The current implementation can:

- Represent travel requirements using shared state
- Build and execute a LangGraph workflow
- Execute five specialist travel agents
- Research destinations using real Tavily web search
- Search real accommodation options using SerpApi Google Hotels
- Search real activities and attractions using SerpApi Google Maps
- Retrieve real weather forecasts using WeatherAPI.com
- Search real restaurant options using SerpApi Google Maps
- Use Gemini for agent reasoning
- Use Gemini tool calling for external data retrieval
- Produce Pydantic structured analysis
- Store specialist outputs in shared TravelState
- Execute multiple specialist agents through LangGraph
- Run the current automated test suite
- Validate real API integrations for Destination, Stay, Activity, Weather, and Food through direct/integration execution

The Activity Agent has replaced the previous mock activity dataset with real SerpApi Google Maps retrieval.

## 22. What Has Not Been Implemented Yet

The following features are part of the planned final system but are not yet implemented:

- Itinerary Agent
- Final Response Agent
- Itinerary validation
- Parallel workflows
- Conditional workflows
- Iterative workflows
- FastAPI backend
- Streamlit frontend
- MCP integration
- Persistence
- Global tool-calling refactor
- Centralized error handling
- LLM provider abstraction
- Dedicated automated Activity Agent tests
- Docker
- GitHub Actions
- Deployment

The core research-agent layer is now substantially implemented. The next major development stage is itinerary generation and the hybrid LangGraph workflow.

## 23. Development Principle

The project follows an incremental engineering approach.

Each major component follows:

    Understand
        ↓
    Research
        ↓
    Document Research
        ↓
    Learn Required Concept
        ↓
    Implement
        ↓
    Test
        ↓
    Refactor
        ↓
    Document
        ↓
    Git
        ↓
    GitHub

The current cycle successfully implemented and tested the connection between the Destination Agent and Gemini.

---

## 24. Next Implementation Goal

The next major goal is to introduce **structured output** for the Destination Agent.

Instead of storing unstructured generated text:

    destination_data = {
        "analysis": response.content
    }

the agent will eventually produce structured information that can be reliably consumed by later agents.

The intended direction is:

    Gemini
        ↓
    Structured Output
        ↓
    Pydantic Schema
        ↓
    destination_data
        ↓
    Future Travel Agents

This will provide a stronger foundation for the multi-agent travel-planning workflow.

## Structured Output with Pydantic

The Destination Agent initially returned free-form LLM text. This was changed to structured output so that the agent produces predictable, validated data that can be safely consumed by other parts of the travel-planning system.

### DestinationAnalysis Schema

The project defines a Pydantic model in:

`src/schemas/destination.py`

The schema contains four fields:

- `overview` — concise explanation of why the destination is suitable
- `recommended_areas` — recommended areas or locations to explore
- `travel_considerations` — important considerations for the trip
- `preference_suggestions` — suggestions based on traveler preferences

Conceptually:

    DestinationAnalysis
    ├── overview
    ├── recommended_areas
    ├── travel_considerations
    └── preference_suggestions

Pydantic provides runtime validation and gives the application a clearly defined data contract for the Destination Agent.

### Structured LLM Helper

The LLM service provides a reusable helper:

`get_structured_llm(schema)`

This helper creates the Gemini LLM and applies LangChain structured output support using the supplied Pydantic schema.

Conceptually:

    get_structured_llm(DestinationAnalysis)
                    ↓
             Gemini LLM
                    ↓
       Structured DestinationAnalysis

This keeps structured-output configuration inside the LLM service instead of duplicating it inside individual agents.

### Destination Agent Structured Output

The Destination Agent now uses:

    structured_llm = get_structured_llm(DestinationAnalysis)

The travel request is passed to the structured LLM, which returns a `DestinationAnalysis` Pydantic object.

The result is converted into a dictionary before being stored in the graph state:

    response.model_dump()

Therefore, the destination agent no longer stores an arbitrary text response under an `analysis` field.

The resulting state contains structured destination information:

    destination_data
    ├── overview
    ├── recommended_areas
    ├── travel_considerations
    └── preference_suggestions

### TravelState Integration

The `TravelState` definition was also updated so that `destination_data` is explicitly typed as:

    DestinationAnalysis

This creates a stronger contract between the graph state and the Destination Agent.

The relationship is:

    Destination Agent
            ↓
    DestinationAnalysis
            ↓
       TravelState
            ↓
      destination_data

This is preferable to using a generic `dict` because the expected structure is explicitly defined.

### Testing

Structured output is covered by automated tests.

The destination schema test verifies that a valid `DestinationAnalysis` object can be created and contains the expected fields.

The graph test invokes the complete travel graph and verifies that the Destination Agent produces:

- a destination overview
- recommended areas
- travel considerations
- preference suggestions

The complete test suite currently passes:

    4 passed

This confirms that the structured-output implementation works together with the existing TravelState, LangGraph workflow, and Gemini integration.

### Why Structured Output Matters

Structured output is important for the multi-agent architecture because future agents will need predictable information from previous agents.

For example:

    Destination Agent
            ↓
    DestinationAnalysis
            ↓
    Stay Agent
            ↓
    Activity Agent
            ↓
    Food Agent
            ↓
    Itinerary Agent

Instead of asking downstream agents to interpret arbitrary text, each agent can work with clearly defined data structures.

This improves:

- reliability
- validation
- maintainability
- testability
- agent-to-agent communication
- future API integration

### Current Architecture

The current implementation can be represented as:

    User Travel Request
            ↓
       TravelState
            ↓
    LangGraph Orchestrator
            ↓
    Destination Agent
            ↓
       Gemini LLM
            ↓
    Structured Output
            ↓
    DestinationAnalysis
            ↓
       TravelState
            ↓
           END

The system currently implements the first structured agent in the larger multi-agent travel-planning architecture.

### Current Implementation Status

Completed:

- Gemini LLM integration
- Environment-based API configuration
- LangGraph StateGraph
- TravelState
- Destination Agent
- Pydantic DestinationAnalysis schema
- Structured LLM helper
- Structured Destination Agent output
- Type-safe destination state
- Automated tests

Not yet implemented:

- Stay Agent
- Activity Agent
- Weather Agent
- Food Agent
- Itinerary Agent
- Parallel agent execution
- Conditional workflows
- External travel APIs/tools
- FastAPI
- Streamlit
- Persistence
- MCP
- LLM provider abstraction
- Docker
- GitHub Actions
- Deployment

## Stay / Hotel Agent Implementation

The Stay Agent is the second specialist agent implemented in the AI Travel Planner.

Its responsibility is to research accommodation options using:

- Destination
- Travel dates
- Duration
- Number of travelers
- Budget
- Preferences

The current implementation uses real accommodation data from SerpApi Google Hotels.

### Accommodation Schema

The accommodation data structure is defined in:

    src/schemas/stay.py

The `Accommodation` Pydantic model contains:

    name
    area
    price_per_night
    rating
    description

The `StayAnalysis` model contains:

    recommended_area
    accommodation_options
    budget_assessment
    stay_recommendation

### Accommodation Search Tool

The accommodation search tool is implemented in:

    src/tools/accommodation.py

Current interface:

    search_accommodations(
        destination,
        travel_dates,
        duration,
        travelers,
        budget,
        preferences
    )

The tool is exposed using LangChain's `@tool` decorator.

### SerpApi Google Hotels Integration

The Stay Agent uses the SerpApi Google Hotels engine:

    engine = google_hotels

The request includes:

    q
    check_in_date
    check_out_date
    adults
    currency
    gl
    hl
    sort_by
    api_key

The API key is loaded from:

    SERPAPI_API_KEY

The same SerpApi credential can be reused by the Food Agent.

### Travel Date Parsing

The accommodation tool expects:

    YYYY-MM-DD to YYYY-MM-DD

Example:

    2026-10-10 to 2026-10-12

The helper:

    parse_travel_dates(travel_dates)

splits the input into:

    check_in
    check_out

This keeps date parsing separate from API request construction.

### Accommodation Response Normalization

The SerpApi response is normalized into the application's internal representation:

    {
        "name": ...,
        "area": ...,
        "price_per_night": ...,
        "rating": ...,
        "description": ...
    }

The implementation extracts information from the Google Hotels response including:

- Property name
- Address
- Lowest extracted nightly price
- Overall rating
- Description

The first ten properties are normalized.

Provider-specific response structures therefore remain inside the tool layer.

### Provider Independence

The Stay Agent depends on:

    search_accommodations()

rather than directly depending on SerpApi.

Architecture:

    Stay Agent
        ↓
    Stable Tool Interface
        ↓
    Accommodation Provider
        ↓
    SerpApi Google Hotels

The provider can therefore be replaced later without changing the Stay Agent's overall design.

### Gemini Tool Calling

The Stay Agent binds the accommodation search tool to Gemini.

The implemented flow is:

    HumanMessage
        ↓
    Gemini
        ↓
    AIMessage
        ↓
    Tool Call
        ↓
    search_accommodations()
        ↓
    SerpApi Google Hotels
        ↓
    Tool Result
        ↓
    ToolMessage
        ↓
    Gemini Structured Output
        ↓
    StayAnalysis

The application executes the requested tool call and passes the result back to Gemini using `ToolMessage`.

### Stay Prompt

The Stay Agent prompt contains:

    Destination
    Travel Dates
    Duration
    Travelers
    Budget
    Preferences

Gemini is instructed to evaluate accommodation results based on:

1. Location
2. Budget
3. Rating
4. Traveler preferences

### Structured Output

After the tool result is received, the agent uses:

    get_structured_llm(StayAnalysis)

The Pydantic result is serialized with:

    final_response.model_dump()

and stored in:

    state["stay_options"]

This combines real external data retrieval with structured LLM reasoning.

### Real Accommodation Search Test

The real Google Hotels integration was tested with:

    Destination: Goa, India
    Travel Dates: 2026-10-10 to 2026-10-12
    Travelers: 2
    Budget: 50000
    Preferences:
    - beaches
    - food

The API successfully returned real accommodation results.

Examples included:

    Om Ganesh Naik Guest House
    om ganesh guest house cliffside
    OYO Aym Yoga Resort
    SanRit Hotel
    Mandala House - Party Hostel
    Baga Beach Way
    SUNNY CLIFF BEACH STAY
    Hotel El - Paso
    Hippie hostel Anjuna
    Red Monkeys Restaurant Bar and Hostel

The normalized records contained:

    name
    area
    price_per_night
    rating
    description

### Stay Agent Test

The complete Stay Agent was executed successfully using the real accommodation search.

Gemini:

1. Received the travel request.
2. Requested the accommodation search tool.
3. Executed the SerpApi Google Hotels request.
4. Received normalized accommodation results.
5. Produced a structured `StayAnalysis`.
6. Stored the result in shared state.

The test recommendation identified North Goa, particularly around Anjuna and Baga, as a suitable area for the supplied preferences.

### Automated Testing

Test file:

    tests/test_accommodation_tool.py

The test verifies:

- The tool returns a list.
- Results are available.
- `name` exists.
- `area` exists.
- `price_per_night` exists.
- `rating` exists.
- `description` exists.

The complete test suite after the Stay Agent implementation produced:

    12 passed
    0 failed
    1 warning

The warning originates from the Google GenAI dependency and is deferred to a later dependency/refactoring review.

### TravelState Integration

The Stay Agent writes its result to:

    state["stay_options"]

The shared state contains the outputs of the specialist agents:

    destination_data
    stay_options
    activities
    weather
    restaurants
    itinerary

### LangGraph Integration

The current sequential graph is:

    START
      ↓
    Destination Agent
      ↓
    Stay Agent
      ↓
    Activity Agent
      ↓
    Weather Agent
      ↓
    Food Agent
      ↓
    END

### Refactoring Decision

The Stay Agent currently contains explicit tool-calling logic.

The same pattern exists in the other tool-using agents.

A reusable tool-calling abstraction will be considered during the global refactoring stage after the remaining specialist agents are implemented.

The recurring Gemini Automatic Function Calling warning is also treated as a cross-cutting tool-calling concern rather than a Stay-specific failure.

### Current Implementation Status

Completed:

- Accommodation schema
- StayAnalysis schema
- Real SerpApi Google Hotels integration
- Travel date parsing
- Accommodation response normalization
- Gemini tool calling
- Structured StayAnalysis output
- TravelState integration
- LangGraph integration
- Real API testing
- Automated tests

The Stay Agent is functionally complete for the current development stage.

## Activity Agent Research

### Purpose

The Activity Agent is responsible for finding relevant activities, attractions, and experiences for a travel destination.

It considers:

- Destination
- Traveler preferences
- Trip duration
- Number of travelers
- Budget
- Available activity information

The Activity Agent is a specialized research component and does not generate the final itinerary.

### Why a Separate Activity Agent?

Activity planning is a distinct travel-planning responsibility.

A dedicated Activity Agent allows the system to:

- Search real activities and attractions
- Consider traveler preferences
- Categorize activity options
- Rank suitable candidates
- Provide structured activity information
- Supply activity data to the future Itinerary Agent

This follows the project principle:

    One specialized agent
        ↓
    One focused responsibility

### Selected Data Source

The initial Activity Agent used a controlled/mock activity dataset.

A real external activity data source was required for the current implementation.

Amadeus was initially considered because of its travel-related activity capabilities. However, the Amadeus for Developers self-service portal has been decommissioned, so it was not suitable for a new integration.

The selected provider is:

    SerpApi Google Maps

This provider is already used by the Stay and Food agents, allowing the project to reuse the existing:

    SERPAPI_API_KEY

### Why SerpApi Google Maps?

SerpApi Google Maps supports Google Maps-style local searches and can return structured local results for attractions, tourist locations, experiences, and other activity-related places.

The main advantages are:

1. Existing project provider
2. Existing API credential
3. Activity and attraction discovery
4. Structured JSON results
5. Simple REST integration
6. No additional provider-specific authentication
7. Consistent tool architecture with the Food Agent

### Activity Search Tool

The activity search tool is implemented in:

    src/tools/activity.py

The application-level interface is:

    search_activities(
        destination,
        preferences,
        limit
    )

The tool:

1. Loads `SERPAPI_API_KEY`.
2. Validates the key.
3. Builds an activity-focused Google Maps query.
4. Sends the request to SerpApi.
5. Validates the HTTP response.
6. Parses the JSON response.
7. Normalizes local results.
8. Returns activity candidates.

### Search Query

The tool constructs a query similar to:

    things to do, activities, attractions, and experiences in {destination}

Traveler preferences are appended when available.

Example:

    things to do, activities, attractions, and experiences in Goa, India for beaches, adventure, food

The request uses parameters equivalent to:

    engine = google_maps
    q = activity search query
    type = search
    limit = requested result count
    hl = en
    gl = in
    api_key = SERPAPI_API_KEY

### Activity Data Normalization

The external Google Maps result is normalized into the project's Activity structure:

    Activity
    ├── name
    ├── location
    ├── category
    ├── estimated_cost
    ├── duration
    └── description

Current mappings include:

    title       → name
    address     → location
    type        → category
    description → description

### Price and Duration Handling

Google Maps local search does not guarantee standardized activity prices or durations for every result.

The implementation therefore does not invent missing values.

When price information is unavailable:

    estimated_cost = 0.0

When duration information is unavailable:

    duration = "Not available"

This explicitly represents unavailable source information rather than fabricating factual values.

### API vs LLM Responsibilities

The external API is responsible for real-world activity discovery.

Gemini is responsible for:

- Understanding traveler preferences
- Categorizing retrieved activities
- Ranking candidates
- Summarizing retrieved information
- Producing structured recommendations
- Assessing the available activity information

The intended architecture is:

    External API
        ↓
    Real Activity Candidates
        ↓
    LLM Reasoning
        ↓
    Structured ActivityAnalysis

### Grounding Consideration

The Activity Agent prompt explicitly instructs Gemini to use retrieved tool results and not invent factual activity fields.

The model may:

- Categorize retrieved activities
- Rank them according to preferences
- Summarize retrieved descriptions
- Assess available activity information

The model should not invent:

- New activities
- Prices
- Durations
- Ratings
- Other unsupported factual details

A stricter grounding mechanism will be considered during the later global tool-calling/refactoring pass.

### Provider Independence

The Activity Agent depends on:

    search_activities()

rather than directly depending on SerpApi.

The provider-specific implementation remains inside:

    src/tools/activity.py

Therefore, the underlying activity provider can later be replaced without redesigning the Activity Agent.

Possible future providers include:

- Another Places/Maps API
- A dedicated experiences API
- An MCP-based activity tool
- Another suitable travel data provider

### Activity Structured Output

The Activity Agent uses the existing Pydantic models:

    Activity
    ActivityAnalysis

The structure is:

    ActivityAnalysis
    ├── recommended_activities
    ├── activities_by_category
    ├── budget_assessment
    └── activity_recommendation

Each activity contains:

    Activity
    ├── name
    ├── location
    ├── category
    ├── estimated_cost
    ├── duration
    └── description

### Activity Tool-Calling Flow

The Activity Agent follows the project's established tool-calling pattern:

    HumanMessage
        ↓
    Gemini
        ↓
    AIMessage
        ↓
    Tool Call
        ↓
    search_activities()
        ↓
    SerpApi Google Maps
        ↓
    Tool Result
        ↓
    ToolMessage
        ↓
    Structured Gemini
        ↓
    ActivityAnalysis
        ↓
    TravelState["activities"]

### Testing Research Decision

The Activity tool was tested directly with a real SerpApi request.

Example:

    Destination: Goa, India
    Preferences:
    - beaches
    - adventure
    - food
    Limit: 5

The real response returned activity/attraction candidates including examples such as:

- Parental Umbrage boat-trip-related attraction
- Butterfly Beach Goa
- Thunder World Goa Amusement Parks
- Goosebumps Virtual Escape
- Velsao Beach

The Activity Agent was then executed using a real tool call and successfully returned a structured `ActivityAnalysis`.

The current full automated suite remains:

    12 passed
    1 warning

The Activity Agent itself has been validated through direct execution; a dedicated automated Activity test file is a planned testing improvement.

### LangGraph Role

The Activity Agent is currently a node in the sequential graph:

    START
      ↓
    Destination Agent
      ↓
    Stay Agent
      ↓
    Activity Agent
      ↓
    Weather Agent
      ↓
    Food Agent
      ↓
    END

The final architecture will execute Activity in parallel with Stay and Weather after Destination research.

### Relationship with Itinerary Agent

The Activity Agent does not generate the final itinerary.

It provides:

    TravelState["activities"]

The future Itinerary Agent will combine:

    DestinationAnalysis
        +
    StayAnalysis
        +
    ActivityAnalysis
        +
    WeatherAnalysis
        +
    FoodAnalysis
        ↓
    Day-by-Day Itinerary

### Research Conclusion

The Activity Agent has been upgraded from mock data to a real SerpApi Google Maps integration.

The final research architecture is:

    Activity Agent
        ↓
    search_activities()
        ↓
    SerpApi Google Maps
        ↓
    Real Activity Candidates
        ↓
    Gemini
        ↓
    ActivityAnalysis
        ↓
    TravelState

---

## Activity Agent Implementation

### Overview

The Activity Agent is the third specialist research agent implemented in the AI Travel Planner.

Its responsibility is to retrieve and recommend activities and attractions based on:

- Destination
- Trip duration
- Number of travelers
- Budget
- Traveler preferences

The implementation follows the same tool-calling and structured-output pattern established by the Stay Agent.

### Activity Schema

The schema is implemented in:

    src/schemas/activity.py

The `Activity` model contains:

    name: str
    location: str
    category: str
    estimated_cost: float
    duration: str
    description: str

The `ActivityAnalysis` model contains:

    recommended_activities: list[Activity]
    activities_by_category: dict[str, list[str]]
    budget_assessment: str
    activity_recommendation: str

### Real Activity Search Tool

The real activity search tool is implemented in:

    src/tools/activity.py

It uses:

    requests
    python-dotenv
    LangChain @tool
    SerpApi Google Maps

The tool validates:

    SERPAPI_API_KEY

and raises a clear configuration error when the key is missing.

### Current Tool Implementation Behavior

The tool builds an activity query from:

    destination
    +
    preferences

and requests Google Maps local results.

The tool normalizes each result into:

    {
        "name": ...,
        "location": ...,
        "category": ...,
        "estimated_cost": 0.0,
        "duration": "Not available",
        "description": ...
    }

The default values for price and duration are intentional because the source does not guarantee standardized values for every activity.

### Real API Test

The activity tool was tested with:

    Destination: Goa, India
    Preferences:
    - beaches
    - adventure
    - food
    Limit: 5

The request successfully returned real Google Maps results.

The test returned real places such as:

    Butterfly Beach Goa
    Velsao Beach
    Thunder World Goa Amusement Parks
    Goosebumps Virtual Escape
    Boat-trip-related attractions

This confirms that the Activity Agent no longer depends on the previous mock dataset.

### Activity Agent

The Activity Agent is implemented in:

    src/agents/activity_agent.py

The main function is:

    activity_agent(state: TravelState) -> TravelState

The agent:

1. Reads travel requirements from `TravelState`.
2. Builds the Activity prompt.
3. Obtains Gemini through the shared LLM service.
4. Binds `search_activities`.
5. Invokes Gemini.
6. Executes the requested tool call.
7. Creates a `ToolMessage`.
8. Invokes structured Gemini output.
9. Stores the resulting `ActivityAnalysis` in `TravelState`.

### Activity Prompt Construction

The prompt contains:

    Destination
    Travel Dates
    Duration
    Travelers
    Budget
    Preferences

The prompt also contains explicit data-grounding instructions:

1. Use only retrieved activity information.
2. Do not introduce activities that are not present in tool results.
3. Do not invent prices, durations, ratings, or other factual details.
4. Use `0.0` when price information is unavailable.
5. Use `"Not available"` when duration information is unavailable.
6. Base descriptions on retrieved information.
7. Categorize and rank retrieved activities according to preferences.
8. Acknowledge unavailable pricing in the budget assessment.

### Gemini Tool Calling

The Activity Agent binds:

    search_activities

to Gemini.

The flow is:

    llm = get_llm()

    llm_with_tools = llm.bind_tools(
        [search_activities]
    )

Gemini can then request the activity search tool.

The application executes:

    search_activities.invoke(
        tool_call["args"]
    )

### Tool Message Flow

The tool result is passed back through `ToolMessage`.

The message sequence is:

    HumanMessage
        ↓
    AIMessage
    (tool call)
        ↓
    ToolMessage
    (tool result)
        ↓
    Structured LLM
        ↓
    ActivityAnalysis

This is consistent with the Stay, Food, and Destination tool-calling architecture.

### Structured Activity Output

After receiving the tool result, the agent creates:

    get_structured_llm(ActivityAnalysis)

The structured model receives the user message, AI response, and tool result.

The final result is serialized with:

    final_response.model_dump()

and stored in:

    state["activities"]

### Activity Agent Validation

The Activity Agent was executed directly using:

    Destination: Goa, India
    Travel Dates: 2026-10-10 to 2026-10-12
    Duration: 2
    Travelers: 2
    Budget: 50000
    Preferences:
    - beaches
    - adventure
    - food

The agent successfully returned:

    recommended_activities
    activities_by_category
    budget_assessment
    activity_recommendation

The grounding prompt successfully prevented the model from inventing activity prices or durations when those values were unavailable from the tool.

A remaining limitation is that LLM grounding is prompt-based rather than enforced by a deterministic source-ID validation layer. This is scheduled for the later global tool-calling/refactoring pass.

### TravelState Integration

The Activity Agent reads:

    destination
    travel_dates
    duration
    travelers
    budget
    preferences

and writes:

    state["activities"]

The state progression is:

    TravelState
        |
        ├── destination
        ├── travel_dates
        ├── duration
        ├── travelers
        ├── budget
        ├── preferences
        |
        ├── destination_data
        ├── stay_options
        └── activities

### LangGraph Integration

The Activity Agent is registered in:

    src/graph/travel_graph.py

The current graph contains:

    graph.add_node("destination", destination_agent)
    graph.add_node("stay", stay_agent)
    graph.add_node("activity", activity_agent)
    graph.add_node("weather", weather_agent)
    graph.add_node("food", food_agent)

The current execution order is:

    graph.add_edge(START, "destination")
    graph.add_edge("destination", "stay")
    graph.add_edge("stay", "activity")
    graph.add_edge("activity", "weather")
    graph.add_edge("weather", "food")
    graph.add_edge("food", END)

Therefore:

    START
      ↓
    Destination Agent
      ↓
    Stay Agent
      ↓
    Activity Agent
      ↓
    Weather Agent
      ↓
    Food Agent
      ↓
    END

### Full Current Multi-Agent Architecture

The current specialist-agent layer is:

    Destination Agent
        ↓
    Tavily
        ↓
    DestinationAnalysis

    Stay Agent
        ↓
    SerpApi Google Hotels
        ↓
    StayAnalysis

    Activity Agent
        ↓
    SerpApi Google Maps
        ↓
    ActivityAnalysis

    Weather Agent
        ↓
    WeatherAPI.com
        ↓
    WeatherAnalysis

    Food Agent
        ↓
    SerpApi Google Maps
        ↓
    FoodAnalysis

All outputs are stored in the shared `TravelState`.

### Current Automated Test Result

The current automated suite was executed using:

    python -m pytest

Result:

    12 passed, 1 warning

The warning is:

    DeprecationWarning:
    '_UnionGenericAlias' is deprecated and slated for removal in Python 3.17

It originates from the installed Google GenAI dependency and is not currently a project-code failure.

The Activity tool and Activity Agent have also been manually validated through real API/LLM execution.

### Refactoring Decision

The Activity Agent uses the same explicit tool-calling pattern as other tool-using agents.

The recurring Google GenAI Automatic Function Calling warning is also present during direct Activity Agent execution.

These concerns are being treated as cross-cutting issues.

A global tool-calling/refactoring pass will later evaluate:

- Reusable tool execution helpers
- More deterministic tool-result grounding
- Error handling
- Automatic Function Calling usage
- Shared agent utilities

The current implementation intentionally avoids premature abstraction.

### Current Implementation Status

Completed:

- Activity Pydantic schemas
- Real SerpApi Google Maps activity search
- Activity data normalization
- Gemini tool calling
- Grounding-oriented Activity prompt
- Structured ActivityAnalysis output
- TravelState integration
- LangGraph integration
- Real API testing
- Direct Activity Agent testing
- Implementation documentation

The Activity Agent is functionally complete for the current development stage.

The remaining improvement is stronger deterministic grounding and dedicated automated tests, which can be addressed during the later refactoring/testing pass.

---

## Weather Agent Implementation

### 1. Purpose

The Weather Agent retrieves real weather forecast data for the travel destination and uses the LLM to interpret that data into practical travel recommendations.

The Weather Agent follows the same architecture used by the Stay Agent and Activity Agent:

    TravelState
        ↓
    Weather Agent
        ↓
    Gemini Tool Calling
        ↓
    Weather Tool
        ↓
    WeatherAPI.com
        ↓
    Raw Forecast Data
        ↓
    Gemini Structured Output
        ↓
    WeatherAnalysis
        ↓
    TravelState["weather"]

The agent is responsible for weather-related analysis only. It does not generate the complete travel itinerary.

---

### 2. Weather API Integration

For real weather data, the project uses WeatherAPI.com.

The WeatherAPI forecast endpoint is used to retrieve forecast information for the requested destination.

The Weather Tool sends:

    destination
    duration

to the API.

The API returns information such as:

    Date
    Average temperature
    Maximum temperature
    Minimum temperature
    Weather condition
    Rain probability
    Total precipitation
    Maximum wind speed

Only the information required by the travel planning system is extracted from the API response.

---

### 3. Environment Configuration

The WeatherAPI key is stored in the `.env` file.

    GOOGLE_API_KEY=...
    WEATHER_API_KEY=...

The API key is loaded using `python-dotenv`.

The `.env` file is excluded from Git using `.gitignore` so that API credentials are not committed to the repository.

---

### 4. Weather Tool

File:

    src/tools/weather.py

The Weather Tool is implemented using the LangChain `@tool` decorator.

Its responsibility is to communicate with WeatherAPI.com and return normalized forecast data to the Weather Agent.

Tool interface:

    search_weather(
        destination: str,
        duration: int
    )

The tool:

1. Loads the WeatherAPI key.
2. Validates that the key exists.
3. Calls the WeatherAPI forecast endpoint.
4. Sends the destination and forecast duration.
5. Validates the HTTP response.
6. Parses the JSON response.
7. Extracts the required forecast information.
8. Returns a list of daily forecast dictionaries.

Example normalized result:

    [
        {
            "date": "...",
            "temperature_c": 27.0,
            "max_temperature_c": 28.0,
            "min_temperature_c": 25.0,
            "condition": "...",
            "rain_probability": 70,
            "precipitation_mm": 2.5,
            "max_wind_kph": 18.0
        }
    ]

The Weather Tool is responsible for data retrieval, while the LLM is responsible for interpretation.

---

### 5. Weather Analysis Schema

File:

    src/schemas/weather.py

A Pydantic model is used to define the expected structured output from the Weather Agent.

    WeatherAnalysis

Fields:

    forecast_summary
    temperature_summary
    precipitation_summary
    travel_assessment
    weather_recommendation

The schema ensures that the LLM produces a predictable structure instead of an uncontrolled text response.

---

### 6. Weather Agent

File:

    src/agents/weather_agent.py

The Weather Agent combines:

    Gemini
    LangChain Tool Calling
    Weather Tool
    Pydantic Structured Output
    TravelState

The agent first creates a travel-specific weather analysis prompt using information from `TravelState`.

The prompt includes:

    Destination
    Duration
    Travelers
    Budget
    Preferences

The LLM is then provided with the `search_weather` tool.

---

### 7. Tool Calling Flow

The Weather Agent follows the standard tool-calling sequence.

    HumanMessage
        ↓
    Gemini
        ↓
    Tool Call
        ↓
    search_weather()
        ↓
    WeatherAPI.com
        ↓
    Tool Result
        ↓
    Gemini
        ↓
    Structured WeatherAnalysis

The first Gemini call determines that weather information is required and generates a tool call.

The application executes the tool call.

The tool result is then sent back to Gemini using a `ToolMessage`.

The conversation therefore contains:

    HumanMessage
    AIMessage
    ToolMessage

This allows Gemini to interpret the actual weather data returned by the external API.

---

### 8. Structured Weather Output

After receiving the WeatherAPI result, the agent creates a structured LLM using:

    get_structured_llm(WeatherAnalysis)

The conversation containing the original request, tool call, and tool result is then passed to the structured LLM.

The final response is converted into a dictionary using:

    final_response.model_dump()

The result is stored in the shared state:

    state["weather"] = final_response.model_dump()

This allows downstream agents to access the weather analysis.

---

### 9. Weather Agent and Shared State

The Weather Agent reads information from:

    TravelState

and writes its result to:

    TravelState["weather"]

Conceptually:

    TravelState
        │
        ├── destination
        ├── duration
        ├── travelers
        ├── budget
        └── preferences
                ↓
          Weather Agent
                ↓
          Weather Analysis
                ↓
        state["weather"]

This follows the shared-state architecture used throughout the project.

---

### 10. LLM vs Weather API Responsibilities

The system separates factual weather retrieval from AI interpretation.

#### WeatherAPI.com

Responsible for:

    Weather forecast
    Temperature
    Rain probability
    Precipitation
    Weather conditions
    Wind information

#### Gemini

Responsible for:

    Understanding the travel context
    Interpreting weather conditions
    Assessing travel suitability
    Identifying potential activity impacts
    Generating practical recommendations

This separation prevents the LLM from being treated as the source of real-time weather data.

---

### 11. Example Weather Analysis

For a three-day trip to Goa, the Weather Agent may produce:

    Forecast Summary:
    Expect warm tropical weather with a mixture of cloudy conditions
    and passing showers.

    Temperature Summary:
    Temperatures remain around 25–28°C.

    Precipitation Summary:
    Rain probability is higher during the first two days and lower
    on the third day.

    Travel Assessment:
    Travel is moderately suitable, although some outdoor activities
    may be affected by rain.

    Weather Recommendation:
    Carry waterproof clothing and schedule weather-sensitive outdoor
    activities during the drier periods.

The exact output is generated dynamically from the real forecast returned by WeatherAPI.com.

---

### 12. Weather Agent Testing

Test file:

    tests/test_weather_agent.py

The test provides a sample travel state:

    destination = "Goa"
    duration = 3
    travelers = 2
    budget = 15000
    preferences = ["beach", "adventure"]

The test executes:

    weather_agent(state)

It then verifies that the Weather Agent produces:

    weather
    forecast_summary
    temperature_summary
    precipitation_summary
    travel_assessment
    weather_recommendation

The Weather Agent test successfully completed with:

    1 passed

The test also confirmed the complete integration between:

    Gemini
        ↓
    Weather Tool
        ↓
    WeatherAPI.com
        ↓
    Structured WeatherAnalysis
        ↓
    TravelState

---

### 13. Current Weather Agent Status

The Weather Agent is now independently implemented and tested.

Current status:

    Weather API integration        → Complete
    Weather Tool                   → Complete
    Weather schema                 → Complete
    Gemini tool calling            → Complete
    Structured output              → Complete
    Shared state integration       → Complete
    Weather Agent test             → Passed

The Weather Agent is currently tested independently.

It has not yet been added to the main LangGraph workflow.

---

### 14. Next Implementation Step

The next step is to integrate the Weather Agent into the existing LangGraph workflow.

Current workflow:

    START
      ↓
    Destination Agent
      ↓
    Stay Agent
      ↓
    Activity Agent
      ↓
    END

After Weather Agent integration:

    START
      ↓
    Destination Agent
      ↓
    Stay Agent
      ↓
    Activity Agent
      ↓
    Weather Agent
      ↓
    END

This will allow the complete graph to carry destination, accommodation, activity, and weather information through the shared `TravelState`.

## 8. Food / Restaurant Agent Implementation

### 8.1 Purpose

The Food Agent is responsible for finding and evaluating restaurant options for the traveler's destination.

Its responsibilities are:

1. Search real restaurant data.
2. Evaluate restaurants based on traveler requirements.
3. Consider budget and preferences.
4. Analyze ratings and categories.
5. Produce structured restaurant recommendations.
6. Store the result in shared `TravelState`.

The implemented flow is:

    TravelState
        ↓
    Food Agent
        ↓
    Gemini
        ↓
    Restaurant Search Tool
        ↓
    SerpApi Google Maps
        ↓
    Restaurant Results
        ↓
    ToolMessage
        ↓
    Gemini Structured Output
        ↓
    FoodAnalysis
        ↓
    TravelState

### 8.2 Restaurant API Selection

Foursquare Places API was initially considered for restaurant discovery.

During implementation, the available Foursquare account returned HTTP 429 because the account had no API credits remaining.

SerpApi Google Maps was therefore selected.

The existing SerpApi key is reused for restaurant search.

The selected engine is:

    engine = google_maps

The returned local results provide useful fields including:

- Restaurant name
- Address
- Category/type
- Rating
- Distance
- Description

### 8.3 Environment Configuration

The SerpApi API key is stored in:

    SERPAPI_API_KEY=...

The key is loaded through environment variables.

The `.env` file is excluded from Git.

### 8.4 Restaurant Search Tool

The restaurant search functionality is implemented in:

    src/tools/food.py

Current interface:

    search_restaurants(
        destination: str,
        price_level: int = 2,
        limit: int = 5
    )

The tool sends a request to the SerpApi search endpoint using:

    engine = google_maps

The request includes:

    q = "restaurants in <destination>"
    type = "search"
    limit = limit
    api_key = SERPAPI_API_KEY

### 8.5 Restaurant Data Normalization

The Food Tool converts the external response into the application's internal restaurant representation.

Mapping:

    SerpApi field          Application field
    ------------------------------------------
    title                  name
    address                location
    type                   category
    rating                 rating
    distance               distance
    description            description

The tool passes through the requested `price_level`.

Distance is represented as a string because Google Maps results can return values such as:

    5 km
    850 m

If distance is unavailable:

    Not available

### 8.6 Food Schema

The Food Agent uses Pydantic structured output.

File:

    src/schemas/food.py

Models:

    Restaurant
        ↓
    FoodAnalysis

`Restaurant` contains:

    name
    location
    category
    price_level
    rating
    distance
    description

`FoodAnalysis` contains:

    recommended_restaurants
    restaurants_by_category
    budget_assessment
    food_recommendation

### 8.7 Food Agent

The Food Agent is implemented in:

    src/agents/food_agent.py

The workflow is:

    TravelState
        ↓
    Build Food Prompt
        ↓
    Gemini with search_restaurants
        ↓
    AIMessage containing tool call
        ↓
    Execute search_restaurants
        ↓
    SerpApi Google Maps
        ↓
    ToolMessage
        ↓
    Structured Gemini Output
        ↓
    FoodAnalysis
        ↓
    state["restaurants"]

The LLM is responsible for deciding when restaurant search is required and interpreting the returned restaurant information.

The Python tool is responsible for the external API request.

### 8.8 Food Agent Prompt

The prompt provides:

    Destination
    Duration
    Travelers
    Budget
    Preferences

Gemini evaluates restaurant candidates based on:

1. Traveler preferences
2. Budget
3. Rating
4. Cuisine/category
5. Location
6. Overall suitability

The goal is to recommend practical restaurants for the specific travel request rather than simply returning the highest-rated results.

### 8.9 Structured Output

The Food Agent uses:

    get_structured_llm(FoodAnalysis)

The result is serialized with:

    final_response.model_dump()

and stored in:

    state["restaurants"]

This gives downstream agents predictable restaurant data.

### 8.10 Shared State Integration

The Food Agent writes to:

    TravelState["restaurants"]

Agents communicate through shared state rather than directly calling one another.

    Agent
      ↓
    Shared TravelState
      ↓
    Next Agent

This maintains loose coupling.

### 8.11 LangGraph Integration

The current sequential graph is:

    START
      ↓
    Destination
      ↓
    Stay
      ↓
    Activity
      ↓
    Weather
      ↓
    Food
      ↓
    END

The Food Agent is the latest completed research agent.

### 8.12 Testing

The Food Agent is covered by:

    tests/test_food_schema.py
    tests/test_food_tool.py
    tests/test_food_agent.py
    tests/test_graph.py

Testing covers:

- Pydantic schema creation
- Restaurant schema creation
- Tool registration
- Food Agent execution
- SerpApi restaurant retrieval
- Structured state output
- Graph integration

### 8.13 Real API Test

A real SerpApi Google Maps request was successfully executed using:

    Destination: Mumbai
    Price level: 2
    Limit: 5

The API returned real restaurant data.

The normalized results included fields such as:

    name
    location
    category
    price_level
    rating
    distance
    description

The complete Food Agent was also executed successfully through the LangGraph workflow.

### 8.14 Test Results

After Food Agent integration:

    12 passed
    0 failed
    1 warning

The warning originates from the external `google.genai` dependency:

    DeprecationWarning:
    '_UnionGenericAlias' is deprecated and slated for removal in Python 3.17

This is currently outside the project's application code and is deferred to a later dependency/refactoring review.

### 8.15 Current Status

The Food Agent implementation is complete.

Completed:

- Food schema
- Restaurant search tool
- SerpApi Google Maps integration
- Restaurant response normalization
- Gemini tool calling
- Structured FoodAnalysis
- Shared state integration
- LangGraph integration
- Unit testing
- Integration testing
- Real API testing

Current workflow:

    Destination Agent
            ↓
    Stay Agent
            ↓
    Activity Agent
            ↓
    Weather Agent
            ↓
    Food Agent
            ↓
    END

The next major feature is itinerary generation.

## Destination Research Agent Implementation

### Purpose

The Destination Research Agent is responsible for researching the requested destination using real web information and generating a structured destination analysis tailored to the traveler's requirements.

The original Destination Agent used Gemini alone.

It has now been upgraded to use Tavily for external web research.

### Architecture

The implemented flow is:

    Destination Agent
            |
            v
        Gemini
            |
            v
    Destination Research Tool
            |
            v
       Tavily Search API
            |
            v
       Web Search Results
            |
            v
        Gemini Analysis
            |
            v
    DestinationAnalysis
            |
            v
        TravelState

### Tavily Configuration

The Tavily Python client is used to communicate with the Tavily Search API.

The API key is stored in:

    TAVILY_API_KEY=...

The `.env` file is excluded from Git.

### Destination Research Tool

File:

    src/tools/destination.py

The `search_destination` function is exposed as a LangChain tool.

Its responsibilities are:

1. Read `TAVILY_API_KEY`.
2. Create a Tavily client.
3. Build a destination-focused search query.
4. Include traveler preferences.
5. Search the web.
6. Retrieve relevant results.
7. Normalize the results.

The normalized result structure is:

    [
        {
            "title": "...",
            "url": "...",
            "content": "..."
        }
    ]

The tool performs information retrieval; it does not generate the final recommendation.

### Search Configuration

The implementation uses:

    search_depth = "advanced"
    max_results = 5

This keeps the amount of retrieved research manageable for the LLM.

### Destination Query

The query combines:

    destination
    +
    traveler preferences
    +
    travel research requirements

For example:

    Destination: Goa
    Preferences: beaches, adventure, food

The resulting search focuses on destination travel information, recommended areas, attractions, travel considerations, and preference-specific recommendations.

### Destination Agent Tool Calling

The Destination Agent binds:

    search_destination

to Gemini.

The flow is:

    HumanMessage
         |
         v
       Gemini
         |
         v
      Tool Call
         |
         v
    search_destination
         |
         v
       Tavily
         |
         v
     Tool Result
         |
         v
       Gemini
         |
         v
    Structured Output

The application executes the requested tool call and passes the result back to Gemini using a `ToolMessage`.

### Structured Output

The final response uses:

    DestinationAnalysis

with:

    overview
    recommended_areas
    travel_considerations
    preference_suggestions

The result is converted using:

    final_response.model_dump()

and stored in:

    state["destination_data"]

### Real API Testing

The destination search tool was tested using a real Tavily request.

Example:

    Destination: Goa
    Preferences:
    - beaches
    - adventure

The tool successfully returned multiple web results containing:

- Title
- URL
- Content

The complete Destination Agent was then tested using:

    Destination: Goa
    Duration: 5 days
    Travelers: 2
    Budget: 50000
    Preferences:
    - beaches
    - adventure
    - food

The agent successfully:

1. Received the travel requirements.
2. Called the Tavily search tool.
3. Retrieved real web information.
4. Passed the research back to Gemini.
5. Generated structured `DestinationAnalysis`.
6. Stored the result in `destination_data`.

### LangGraph Integration

The Destination Agent is registered as the first specialist agent.

Current sequential graph:

    START
      ↓
    Destination Agent
      ↓
    Stay Agent
      ↓
    Activity Agent
      ↓
    Weather Agent
      ↓
    Food Agent
      ↓
    END

The Destination Agent therefore provides destination research before the downstream specialist agents execute.

### LangGraph Integration Test

The Destination Agent was tested through the compiled LangGraph.

The graph successfully returned:

    result["destination_data"]

with valid structured destination analysis.

This confirms that the Tavily-powered Destination Agent works inside the existing travel workflow.

### Error Handling

The Destination Research Tool validates that:

    TAVILY_API_KEY

exists before creating the Tavily client.

If the key is missing, the tool raises a clear configuration error.

More advanced retry, fallback, and centralized error handling remain future engineering work.

### Current Status

The Destination Research Agent is functionally complete.

Completed:

- Tavily destination research
- Destination research tool
- Gemini tool calling
- Structured DestinationAnalysis
- TravelState integration
- LangGraph integration
- Real API testing
- Agent testing
- Documentation

The recurring Gemini Automatic Function Calling warning is deferred to the global tool-calling refactor.

---

## End-to-End Implementation Status

The current core implementation contains five specialist research agents.

### Completed

- Python project environment
- Gemini LLM service
- Environment-based configuration
- Shared TravelState
- LangGraph sequential orchestration
- Pydantic structured output
- Destination Agent
- Tavily destination research
- Stay Agent
- SerpApi Google Hotels integration
- Travel date parsing
- Accommodation response normalization
- Activity Agent
- SerpApi Google Maps activity and attraction integration
- Activity response normalization
- Weather Agent
- WeatherAPI.com integration
- Food Agent
- SerpApi Google Maps restaurant integration
- Restaurant response normalization
- Gemini tool calling
- Real API testing for Destination, Stay, Activity, Weather, and Food
- Current automated test suite with 12 passing tests
- Research and implementation documentation

### Current Sequential Workflow

    START
      ↓
    Destination Agent
      ↓
    Stay Agent
      ↓
    Activity Agent
      ↓
    Weather Agent
      ↓
    Food Agent
      ↓
    END

### Current Core Capabilities

The system can currently:

- Accept structured travel requirements.
- Maintain shared travel state.
- Research destinations using real web search.
- Search real accommodation options.
- Search real activities and attractions.
- Retrieve real weather forecasts.
- Search real restaurant options.
- Use Gemini to reason over retrieved information.
- Call external tools from specialist agents.
- Produce structured Pydantic analysis.
- Execute multiple specialist agents through LangGraph.
- Run the current automated test suite.

### Pending Core Features

The following major features are not yet implemented:

- Itinerary Agent
- Final Response Agent
- Itinerary validation
- Parallel workflow
- Conditional workflow
- Iterative workflow
- FastAPI backend
- Streamlit frontend
- MCP integration
- Persistence
- Global tool-calling refactor
- Deterministic tool-result grounding
- Centralized error handling
- LLM provider abstraction
- Dedicated Activity automated tests
- Docker
- GitHub Actions
- Deployment

### Final Hybrid Workflow

The final architecture will combine all four workflow patterns.

#### Sequential

Sequential execution will be used where later work depends on earlier results.

Examples:

    User
      ↓
    Destination Research
      ↓
    Parallel Research Completion
      ↓
    Food
      ↓
    Itinerary
      ↓
    Validation
      ↓
    Final Response

#### Parallel

Stay, Activity, and Weather research can execute independently after destination information is available.

    Destination Agent
           |
       +---+---+---+
       |   |   |   |
       v   v   v
     Stay Activity Weather
     Agent Agent   Agent
       |   |   |
       +---+---+
           |
       Parallel Join
           |
           v
       Food Agent

#### Conditional

The validator will decide whether the generated itinerary is acceptable.

    Itinerary
        |
        v
    Validator
       / \
   Valid Invalid
     |      |
     |      v
     |   Refine
     |      |
     |      └──→ Validator
     |
     v
    Final Response

Conditional routing may also be used for budget or weather-related decisions when useful.

#### Iterative

An invalid itinerary will be sent back for refinement.

    Itinerary Agent
         |
         v
    Itinerary Validator
         |
      Invalid
         |
         v
    Refine Itinerary
         |
         v
    Validator
         |
      Valid
         |
         v
       Continue

A maximum iteration limit will be used to prevent an endless refinement loop.

### Final Target Architecture

                          USER
                            │
                            ▼
                     ┌─────────────┐
                     │   FastAPI   │
                     └──────┬──────┘
                            │
                            ▼
                     ┌─────────────┐
                     │  LangGraph  │
                     │ Orchestrator│
                     └──────┬──────┘
                            │
                            ▼
                 ┌───────────────────┐
                 │ Destination Agent │
                 │ + Tavily Research │
                 └─────────┬─────────┘
                           │
                           ▼
                    Destination Data
                           │
              ┌────────────┼────────────┐
              │            │            │
              ▼            ▼            ▼
          Stay Agent   Activity Agent  Weather Agent
              │            │            │
              │       SerpApi Maps      │
              │            │            │
              └────────────┼────────────┘
                           │
                     PARALLEL JOIN
                           │
                           ▼
                      Food Agent
                           │
                     SerpApi Maps
                           │
                           ▼
                 ┌──────────────────┐
                 │ Itinerary Agent  │
                 └────────┬─────────┘
                          │
                          ▼
                 Itinerary Validation
                          │
                    ┌─────┴─────┐
                    │           │
                  Valid       Invalid
                    │           │
                    │           ▼
                    │      Refine Itinerary
                    │           │
                    │           └──────► Validator
                    │
                    ▼
              Final Response Agent
                    │
                    ▼
              FINAL TRAVEL PLAN
                    │
                    ▼
                 Streamlit
                    │
                    ▼
                   USER

### Development Workflow

The project continues to follow:

    Understand
        ↓
    Research
        ↓
    Document Research
        ↓
    Learn Required Concept
        ↓
    Implement
        ↓
    Test
        ↓
    Refactor
        ↓
    Document
        ↓
    Git
        ↓
    GitHub

The workflow is completed for each major project stage before moving to the next stage.

### Current Next Step

The next implementation stage is:

    Itinerary Agent

The Itinerary Agent will combine:

    DestinationAnalysis
        +
    StayAnalysis
        +
    ActivityAnalysis
        +
    WeatherAnalysis
        +
    FoodAnalysis
        ↓
    Day-by-Day Itinerary

After the Itinerary Agent is complete, the project will implement:

    Validation
        ↓
    Conditional Routing
        ↓
    Iterative Refinement
        ↓
    Final Response Agent
        ↓
    FastAPI
        ↓
    Streamlit
        ↓
    MCP / Persistence / Productionization
