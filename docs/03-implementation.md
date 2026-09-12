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

The current system follows this flow:

    User Input
        ↓
    TravelState
        ↓
    LangGraph
        ↓
    Destination Agent
        ↓
    Gemini 3.5 Flash-Lite
        ↓
    Destination Analysis
        ↓
    Updated TravelState

---

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

The initial project dependencies are maintained in `requirements.txt`.

    langgraph
    langchain
    langchain-google-genai
    python-dotenv
    pydantic

Pytest is also installed in the project environment for automated testing.

---

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
        destination_data: dict
        stay_options: list[dict]
        activities: list[dict]
        weather: dict
        restaurants: list[dict]
        itinerary: dict

### Purpose

`TravelState` provides a common structure for information flowing through the travel-planning workflow.

It contains two major categories.

### User Input

- Destination
- Travel dates
- Duration
- Number of travelers
- Budget
- Preferences

### Agent Outputs

- Destination information
- Stay options
- Activities
- Weather information
- Restaurants
- Itinerary

Not all fields are populated yet. They have been defined as part of the planned shared state.

---

## 6. LangGraph Workflow

The project uses LangGraph to define the travel-planning workflow.

File:

    src/graph/travel_graph.py

Current workflow:

    START
      ↓
    destination
      ↓
     END

The graph is created using `StateGraph` with `TravelState` as the shared state.

Current implementation:

    from langgraph.graph import StateGraph, START, END

    from src.state import TravelState
    from src.agents.destination_agent import destination_agent


    def build_travel_graph():
        graph = StateGraph(TravelState)

        graph.add_node("destination", destination_agent)

        graph.add_edge(START, "destination")
        graph.add_edge("destination", END)

        return graph.compile()

### Why LangGraph?

LangGraph provides the workflow orchestration layer for the project.

The current graph is intentionally simple and contains one implemented agent.

Additional agents and workflow patterns will be added incrementally.

---

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

The current implementation structure is:

    ai-travel-planner/
    │
    ├── docs/
    │   ├── 01-project-overview.md
    │   ├── 02-research.md
    │   └── 03-implementation.md
    │
    ├── src/
    │   ├── __init__.py
    │   │
    │   ├── state.py
    │   │
    │   ├── agents/
    │   │   ├── __init__.py
    │   │   └── destination_agent.py
    │   │
    │   ├── graph/
    │   │   ├── __init__.py
    │   │   └── travel_graph.py
    │   │
    │   └── services/
    │       ├── __init__.py
    │       └── llm.py
    │
    ├── tests/
    │   ├── test_graph.py
    │   ├── test_llm.py
    │   └── test_state.py
    │
    ├── .gitignore
    ├── README.md
    └── requirements.txt

---

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
            ├── Build Prompt
            │
            ▼
        LLM Service
            │
            ▼
    Gemini 3.5 Flash-Lite
            │
            ▼
    Destination Analysis
            │
            ▼
       TravelState

The LLM service is shared independently from the agent logic.

---

## 21. Current Capabilities

The current implementation can:

- Represent travel requirements using shared state
- Build and execute a LangGraph workflow
- Execute a Destination Agent
- Construct a destination-specific prompt
- Connect to Gemini 3.5 Flash-Lite
- Generate destination analysis using the LLM
- Store the generated analysis in the shared state
- Configure the Gemini model through environment variables
- Validate the Gemini API key
- Automatically test the core components

---

## 22. What Has Not Been Implemented Yet

The following features are part of the planned project but are not yet implemented:

- Structured output
- Pydantic travel response schemas
- Real destination research tools
- Hotel/Stay Agent
- Activity Agent
- Weather Agent
- Food/Restaurant Agent
- Itinerary Agent
- External travel APIs
- Tool calling
- Parallel workflows
- Conditional workflows
- MCP integration
- LLM provider abstraction
- FastAPI backend
- Streamlit frontend
- PostgreSQL persistence
- Advanced error handling
- Full test coverage for agents and tools
- Docker
- GitHub Actions
- GCP deployment

These features will be implemented incrementally.

---

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

The Stay Agent is the second agent implemented in the AI Travel Planner.

Its responsibility is to research accommodation options based on the traveler's destination, budget, duration, number of travelers, and preferences.

### Accommodation Schema

The accommodation data structure is defined in:

`src/schemas/stay.py`

The `Accommodation` Pydantic model contains:

- `name`
- `area`
- `price_per_night`
- `rating`
- `description`

This provides a consistent structure for individual accommodation options.

### StayAnalysis Schema

The Stay Agent uses the `StayAnalysis` Pydantic model as its structured output.

It contains:

- `recommended_area`
- `accommodation_options`
- `budget_assessment`
- `stay_recommendation`

The relationship is:

    StayAnalysis
    ├── recommended_area
    ├── accommodation_options
    │   └── Accommodation
    ├── budget_assessment
    └── stay_recommendation

This ensures that the Stay Agent produces predictable output that can be consumed by the rest of the application.

### Accommodation Search Tool

The project implements an accommodation search tool in:

`src/tools/accommodation.py`

The tool is exposed using LangChain's tool interface.

Its current interface is conceptually:

    search_accommodations(
        destination,
        budget
    )

The current implementation uses sample accommodation data so that the tool-calling architecture can be developed and tested independently of an external hotel provider.

The tool returns information such as:

- accommodation name
- area
- price per night
- rating
- description

The tool implementation can later be replaced with a real external travel or accommodation data source without changing the overall Stay Agent design.

### Gemini Tool Calling

The Stay Agent makes the accommodation search tool available to Gemini using LangChain tool binding.

Conceptually:

    Gemini
       |
       +── search_accommodations()
       |
       +── Tool Schema

The model can determine when accommodation information is required and request the tool.

Binding the tool does not execute the Python function. The application is responsible for executing the requested tool call.

### Tool Calling Message Flow

The Stay Agent implements the required conversational sequence:

    HumanMessage
          |
          v
    Gemini / AIMessage
          |
          v
      Tool Call
          |
          v
    Accommodation Tool
          |
          v
      Tool Result
          |
          v
     ToolMessage
          |
          v
        Gemini
          |
          v
     Final Response

The original user message, AI tool-call message, and tool result are provided to Gemini in the correct order.

This allows Gemini to use the external tool result when producing the final response.

### Structured Final Response

After the accommodation tool returns its result, the Stay Agent uses the structured LLM helper with `StayAnalysis`.

The flow is:

    Accommodation Tool
            |
            v
       Tool Result
            |
            v
      Structured LLM
            |
            v
       StayAnalysis
            |
            v
       model_dump()
            |
            v
       TravelState

This combines two important Agentic AI capabilities:

- tool calling for obtaining external information
- structured output for producing predictable application data

### Stay Agent

The Stay Agent is implemented in:

`src/agents/stay_agent.py`

Its responsibilities are separated into:

1. Building the accommodation research prompt
2. Binding the accommodation search tool
3. Sending the travel request to Gemini
4. Detecting the requested tool call
5. Executing the accommodation tool
6. Returning the tool result to Gemini
7. Generating structured `StayAnalysis` output
8. Storing the result in `TravelState`

### TravelState Integration

The shared graph state was updated so that:

    stay_options: StayAnalysis

The current state therefore contains typed outputs from both implemented agents:

    TravelState
    ├── destination_data: DestinationAnalysis
    └── stay_options: StayAnalysis

This creates a clear data contract between agents and the LangGraph workflow.

### LangGraph Integration

The Stay Agent was added as the second node in the travel graph.

The current graph is:

    START
      |
      v
    Destination Agent
      |
      v
    Stay Agent
      |
      v
    END

The Destination Agent executes first, followed by the Stay Agent.

Both agents operate on the shared `TravelState`.

### Current Multi-Agent Architecture

The current implementation can be represented as:

    User Travel Request
            |
            v
       TravelState
            |
            v
    LangGraph Orchestrator
            |
            v
    Destination Agent
            |
            | Structured Output
            v
    DestinationAnalysis
            |
            v
        Stay Agent
            |
            | Tool Calling
            v
    Accommodation Tool
            |
            | Tool Result
            v
        Gemini
            |
            | Structured Output
            v
       StayAnalysis
            |
            v
       TravelState
            |
            v
           END

### Testing

The Stay Agent implementation is covered by automated tests.

Current tests include:

- accommodation tool test
- destination schema test
- travel graph test
- LLM connection test
- TravelState test
- StayAnalysis schema test

The complete test suite currently passes:

    6 passed

This confirms that the accommodation tool, schemas, Gemini integration, and two-agent LangGraph workflow are functioning together.

### Current Implementation Status

Completed:

- Gemini LLM integration
- TravelState
- LangGraph orchestration
- Destination Agent
- DestinationAnalysis schema
- Structured destination output
- Accommodation search tool
- Accommodation schema
- StayAnalysis schema
- Gemini tool calling
- Tool execution flow
- Structured Stay Agent output
- Two-agent sequential workflow
- Automated tests

Not yet implemented:

- Activity Agent
- Weather Agent
- Food Agent
- Itinerary Agent
- Parallel workflows
- Conditional workflows
- Real external accommodation API
- FastAPI
- Streamlit
- Persistence
- MCP
- LLM provider abstraction
- Docker
- GitHub Actions
- Deployment

## Activity Agent Research

### Purpose

The Activity Agent is a specialized AI agent responsible for finding, evaluating, and recommending activities and experiences for the traveler's destination.

Instead of asking one general-purpose agent to handle destination research, accommodation, activities, food, weather, and itinerary planning, each responsibility is separated into a focused agent.

The Activity Agent will therefore focus specifically on:

- Things to do
- Places and experiences to visit
- Adventure activities
- Cultural experiences
- Sightseeing
- Entertainment
- Activities matching traveler preferences
- Activities appropriate for the trip duration and budget

The Activity Agent will eventually provide activity information to the Itinerary Agent.

---

### Why a Separate Activity Agent?

A travel planner needs more than destination information.

For example, a user may request:

    Plan a 5-day Goa trip for 2 people with a ₹30,000 budget.
    We enjoy beaches, adventure, and local food.

The Destination Agent can determine suitable areas and destination information.

The Stay Agent can determine suitable accommodation.

However, determining what the traveler should actually do during the trip is a separate responsibility.

The Activity Agent handles this responsibility.

The separation provides:

- Clear responsibilities
- Easier testing
- Better maintainability
- Independent tool integration
- Better personalization
- Reusable activity data
- Cleaner communication between agents

The architectural principle is:

    One specialized agent
            |
            v
    One focused responsibility

---

### Activity Agent Responsibilities

The Activity Agent will be responsible for:

1. Understanding the destination.
2. Understanding the trip duration.
3. Understanding the number of travelers.
4. Understanding the traveler's budget.
5. Understanding traveler preferences.
6. Searching for relevant activities.
7. Evaluating available activities.
8. Selecting suitable activities.
9. Organizing activities by category.
10. Producing structured activity recommendations.

The Activity Agent should not be responsible for:

- Accommodation booking
- Restaurant selection
- Weather forecasting
- Final itinerary generation
- General application API handling

Those responsibilities belong to other components or agents.

---

### Activity Agent Inputs

The Activity Agent will consume information from the shared `TravelState`.

Relevant inputs include:

    TravelState
        |
        ├── destination
        ├── duration
        ├── travelers
        ├── budget
        └── preferences

Example:

    destination = "Goa"
    duration = 5
    travelers = 2
    budget = 30000
    preferences = [
        "beaches",
        "adventure",
        "local food"
    ]

These values allow the Activity Agent to generate personalized recommendations instead of generic activity suggestions.

---

### Activity Agent Output

The Activity Agent should not return unrestricted natural-language text.

Instead, it should produce structured information that can be consumed by other agents.

The conceptual output is:

    ActivityAnalysis
        |
        ├── recommended_activities
        ├── activities_by_category
        ├── budget_assessment
        └── activity_recommendation

Each individual activity can contain:

    Activity
        |
        ├── name
        ├── location
        ├── category
        ├── estimated_cost
        ├── duration
        └── description

Structured output makes the Activity Agent easier to test and allows the future Itinerary Agent to consume activity information programmatically.

---

### Activity Agent and Activity Tool

The Activity Agent and Activity Search Tool have different responsibilities.

The Activity Agent is responsible for reasoning and recommendation.

The Activity Tool is responsible for retrieving activity information.

Conceptually:

    Activity Agent
          |
          v
         LLM
          |
          v
    Tool Calling
          |
          v
    Activity Search Tool
          |
          v
    Activity Data
          |
          v
         LLM
          |
          v
    ActivityAnalysis

This separation follows the same architectural principle established by the Stay Agent.

---

### Activity Search Tool

The Activity Search Tool will provide activity information to the Activity Agent.

Conceptually:

    search_activities(
        destination,
        budget,
        preferences
    )

The tool should return structured activity information.

Example:

    [
        {
            "name": "Scuba Diving",
            "location": "Grande Island",
            "category": "Adventure",
            "estimated_cost": 2500,
            "duration": "Half day",
            "description": "Scuba diving experience suitable for adventure-focused travelers."
        }
    ]

Returning structured information gives the LLM explicit fields for evaluating and comparing activities.

---

### Activity Data Source Strategy

The Activity Agent will use a two-stage data-source strategy.

#### Initial Implementation

The first implementation will use a controlled activity dataset behind a LangChain tool.

    Activity Agent
          |
          v
    search_activities()
          |
          v
    Controlled Activity Data

This approach allows the project to focus on learning and implementing:

- Tool calling
- Agent reasoning
- Structured output
- Pydantic validation
- LangGraph integration
- Testing

without making the initial implementation dependent on an external activity API.

#### Future Implementation

The same tool interface can later be connected to a real external data source.

    Activity Agent
          |
          v
    search_activities()
          |
          v
    External API / Search / MCP
          |
          v
    Real Activity Information

The Activity Agent should not need to change when the underlying data provider changes.

This provides provider independence and cleaner architecture.

---

### Activity Tool Provider Independence

The tool interface should be separated from its implementation.

The Activity Agent should conceptually depend on:

    search_activities()

rather than directly depending on:

    SpecificActivityProvider()

This allows the implementation to evolve from:

    Controlled Data
          |
          v
    External API
          |
          v
    Search
          |
          v
    MCP Tool

while keeping the Activity Agent interface stable.

This is an important engineering principle for the project:

    Agent
      |
      v
    Stable Tool Interface
      |
      v
    Replaceable Data Provider

---

### Activity Tool Calling Flow

The Activity Agent will use the standard tool-calling pattern.

The conceptual flow is:

    HumanMessage
         |
         v
        LLM
         |
         v
    AIMessage
    (tool call)
         |
         v
    Application executes tool
         |
         v
    ToolMessage
    (tool result)
         |
         v
        LLM
         |
         v
    Final Structured Output

The tool call contains the required tool arguments.

The application executes the tool and sends the result back to the model.

The model can then evaluate the retrieved activity information and produce the final structured response.

---

### Structured Output

The Activity Agent will use Pydantic models for structured output.

The planned schema contains two conceptual models.

#### Activity

The `Activity` model represents an individual activity.

Expected fields:

    Activity
        |
        ├── name
        ├── location
        ├── category
        ├── estimated_cost
        ├── duration
        └── description

#### ActivityAnalysis

The `ActivityAnalysis` model represents the complete analysis produced by the Activity Agent.

Expected fields:

    ActivityAnalysis
        |
        ├── recommended_activities
        ├── activities_by_category
        ├── budget_assessment
        └── activity_recommendation

Structured output provides predictable information for downstream components.

---

### Why Structured Output Matters

Without structured output, an Activity Agent might return:

    Goa has many great activities.
    You can try scuba diving, visit beaches,
    explore forts, and take a sunset cruise.

This is difficult for another program or agent to reliably consume.

With structured output:

    ActivityAnalysis
        |
        ├── recommended_activities
        ├── activities_by_category
        ├── budget_assessment
        └── activity_recommendation

the Itinerary Agent can programmatically use the activity information.

Therefore:

    Free-form response
          |
          v
    Difficult to process

    Structured response
          |
          v
    Easy to validate and consume

---

### Activity Agent and Shared State

The Activity Agent will communicate with other agents through `TravelState`.

The relevant state progression is:

    TravelState
        |
        ├── destination
        ├── duration
        ├── travelers
        ├── budget
        ├── preferences
        |
        ├── destination_data
        ├── stay_options
        |
        └── activities

The Activity Agent reads the travel requirements and writes its activity analysis into:

    state["activities"]

This allows future agents to consume the activity information without directly depending on the Activity Agent implementation.

---

### Activity Agent in LangGraph

The current graph is:

    START
      |
      v
    Destination Agent
      |
      v
    Stay Agent
      |
      v
    END

After implementing the Activity Agent:

    START
      |
      v
    Destination Agent
      |
      v
    Stay Agent
      |
      v
    Activity Agent
      |
      v
    END

The Activity Agent will therefore become another node in the LangGraph workflow.

The graph is responsible for orchestration, while the Activity Agent is responsible for activity-specific reasoning.

---

### Activity Agent Workflow

The planned Activity Agent workflow is:

    TravelState
         |
         v
    Activity Agent
         |
         v
    Build Activity Prompt
         |
         v
        Gemini
         |
         v
    Tool Calling?
       /     \
     Yes      No
      |        |
      v        v
    Activity   Handle
    Search     response
      |
      v
    Activity Data
      |
      v
    ToolMessage
      |
      v
    Gemini
      |
      v
    Structured Output
      |
      v
    ActivityAnalysis
      |
      v
    TravelState

This workflow follows the same tool-calling and structured-output pattern established by the Stay Agent.

---

### Activity Agent and Future Itinerary Agent

One of the most important reasons for creating structured ActivityAnalysis is future interoperability.

The Activity Agent produces:

    ActivityAnalysis
          |
          v
    TravelState.activities
          |
          v
    Itinerary Agent

The Itinerary Agent can later combine:

    Destination Data
          +
    Stay Options
          +
    Activities
          +
    Weather
          +
    Restaurants
          |
          v
    Final Itinerary

Therefore, the Activity Agent is not an isolated feature.

It is a building block for the final multi-agent travel planning workflow.

---

### Activity Agent Architectural Progression

The project architecture is progressively becoming more capable.

#### Destination Agent

    Destination Agent
          |
          v
         LLM
          |
          v
    Structured Output
          |
          v
    DestinationAnalysis

#### Stay Agent

    Stay Agent
          |
          v
         LLM
          |
          v
    Tool Calling
          |
          v
    External / Controlled Data
          |
          v
    Structured Output
          |
          v
    StayAnalysis

#### Activity Agent

    Activity Agent
          |
          v
         LLM
          |
          v
    Tool Calling
          |
          v
    Activity Data
          |
          v
    Structured Output
          |
          v
    ActivityAnalysis

This progression establishes a reusable pattern for future Food, Weather, and Itinerary agents.

---

### Research Decision

The Activity Agent will be implemented using:

- Gemini as the LLM
- LangChain for LLM and tool integration
- LangGraph for orchestration
- Pydantic for structured output
- A controlled activity search tool for the initial implementation
- Shared `TravelState` for inter-agent communication

The first implementation will prioritize architecture and correctness rather than immediately integrating a real external activity provider.

A real external data source can be introduced later without changing the core Activity Agent architecture.

---

### Research Conclusion

The Activity Agent should be implemented as a specialized LangGraph node that:

1. Reads travel requirements from `TravelState`.
2. Uses Gemini for reasoning.
3. Calls an activity search tool when activity information is required.
4. Receives structured activity data from the tool.
5. Evaluates activities according to destination, budget, duration, travelers, and preferences.
6. Produces validated Pydantic structured output.
7. Stores the resulting activity analysis in `TravelState`.

The Activity Agent therefore extends the project's existing architecture from:

    Structured Destination Research

to:

    Structured Research
          +
    Tool Calling
          +
    External / Controlled Data
          +
    Structured Output

This establishes the foundation for future activity-aware itinerary generation.

---

### Research Sources

- LangChain Tools documentation — LangChain
- LangChain Tool Calling documentation — LangChain
- LangChain Structured Output documentation — LangChain
- LangGraph documentation — LangChain
- Gemini Function Calling documentation — Google AI
- Gemini Structured Output documentation — Google AI

## Activity Agent Implementation

### Overview

The Activity Agent is the third specialized agent implemented in the AI Travel Planner.

Its responsibility is to research and recommend activities based on:

- Destination
- Trip duration
- Number of travelers
- Budget
- Traveler preferences

The Activity Agent follows the same agentic pattern established by the Stay Agent:

    TravelState
         |
         v
    Activity Agent
         |
         v
    Gemini
         |
         v
    Tool Calling
         |
         v
    Activity Search Tool
         |
         v
    Activity Data
         |
         v
    Structured Output
         |
         v
    ActivityAnalysis
         |
         v
    TravelState

---

### Activity Schema

A new Pydantic schema was created at:

    src/schemas/activity.py

The schema contains two models:

- `Activity`
- `ActivityAnalysis`

#### Activity

The `Activity` model represents an individual activity.

    class Activity(BaseModel):
        name: str
        location: str
        category: str
        estimated_cost: float
        duration: str
        description: str

The fields represent:

- `name` — activity name
- `location` — activity location
- `category` — activity category
- `estimated_cost` — estimated activity cost
- `duration` — expected activity duration
- `description` — activity description

Example:

    Activity(
        name="Scuba Diving",
        location="Grande Island",
        category="Adventure",
        estimated_cost=2500,
        duration="Half day",
        description="Scuba diving experience suitable for adventure-focused travelers."
    )

---

### ActivityAnalysis

The `ActivityAnalysis` model represents the complete output of the Activity Agent.

    class ActivityAnalysis(BaseModel):
        recommended_activities: list[Activity]
        activities_by_category: dict[str, list[str]]
        budget_assessment: str
        activity_recommendation: str

The output contains:

- `recommended_activities` — recommended activity objects
- `activities_by_category` — activities grouped by category
- `budget_assessment` — assessment of activity costs against the travel budget
- `activity_recommendation` — overall recommendation

Using Pydantic provides predictable and validated output for downstream agents.

---

### Activity Search Tool

A new activity search tool was created at:

    src/tools/activity.py

The tool is implemented using LangChain's `@tool` decorator.

    @tool
    def search_activities(
        destination: str,
        budget: float,
        preferences: list[str],
    ) -> list[dict]:

The tool currently returns a controlled set of activity data.

Example activities include:

    Baga Beach
    Scuba Diving
    Parasailing
    Fort Aguada
    Sunset Cruise

Each activity contains structured fields:

    name
    location
    category
    estimated_cost
    duration
    description

The initial implementation intentionally uses controlled data rather than a real external API.

This allows the Activity Agent architecture to be tested independently before introducing external data providers.

---

### Activity Tool Testing

The Activity Search Tool was tested independently using:

    search_activities.invoke(
        {
            "destination": "Goa",
            "budget": 5000,
            "preferences": ["beaches", "adventure"]
        }
    )

The tool successfully returned a list of structured activity dictionaries.

Example result:

    [
        {
            "name": "Baga Beach",
            "location": "Baga",
            "category": "Beach",
            "estimated_cost": 0,
            "duration": "2-3 hours",
            "description": "Popular beach suitable for relaxation and water activities."
        },
        {
            "name": "Scuba Diving",
            "location": "Grande Island",
            "category": "Adventure",
            "estimated_cost": 2500,
            "duration": "Half day",
            "description": "Scuba diving experience suitable for adventure-focused travelers."
        }
    ]

A dedicated test was added:

    tests/test_accommodation_tool.py

The tool test verifies that:

- The tool returns data.
- The result is a list.
- Activity names are present.
- Returned activity costs satisfy the test budget.

---

### Activity Agent

The Activity Agent was created at:

    src/agents/activity_agent.py

The agent uses:

- `TravelState`
- Gemini
- LangChain tool calling
- `search_activities`
- Pydantic structured output

The main function is:

    activity_agent(state: TravelState) -> TravelState

---

### Activity Prompt Construction

The Activity Agent builds a prompt from the current travel state.

The prompt includes:

    Destination
    Duration
    Travelers
    Budget
    Preferences

Example:

    Destination: Goa
    Duration: 5 days
    Travelers: 2
    Budget: 30000.0
    Preferences: beaches, adventure

The prompt instructs Gemini to evaluate available activities based on:

1. Traveler preferences
2. Budget
3. Duration
4. Activity category
5. Location

This allows the LLM to make recommendations based on the complete travel context.

---

### Gemini Tool Calling

The Activity Agent binds the activity search tool to Gemini.

    llm = get_llm()

    llm_with_tools = llm.bind_tools(
        [search_activities]
    )

The Activity Agent then sends the travel request to Gemini.

If Gemini decides that the activity search tool is required, it produces a tool call.

The implementation retrieves the first tool call:

    tool_call = response.tool_calls[0]

The tool arguments are then passed to:

    search_activities.invoke(
        tool_call["args"]
    )

---

### Tool Message Flow

The tool result is converted into a `ToolMessage`.

The complete message sequence is:

    HumanMessage
         |
         v
    AIMessage
    (tool call)
         |
         v
    ToolMessage
    (tool result)
         |
         v
    Structured LLM
         |
         v
    ActivityAnalysis

This follows the same successful tool-calling pattern implemented by the Stay Agent.

---

### Structured Activity Output

After receiving the activity tool result, the Activity Agent creates a structured LLM using:

    get_structured_llm(ActivityAnalysis)

The model is then invoked with:

    [
        user_message,
        response,
        tool_message,
    ]

Gemini converts the retrieved activity information into the `ActivityAnalysis` Pydantic structure.

The resulting model is stored in the shared state using:

    state["activities"] = final_response.model_dump()

This allows the rest of the travel planning graph to access the activity information.

---

### Activity Agent Testing

The Activity Agent was first tested independently before integrating it into LangGraph.

The test request used:

    Destination: Goa
    Duration: 5 days
    Travelers: 2
    Budget: 30000
    Preferences:
    - beaches
    - adventure

The agent successfully returned:

    recommended_activities

    activities_by_category

    budget_assessment

    activity_recommendation

Example categories returned included:

    Beach
    Adventure
    Culture
    Experience

The output demonstrated that the agent could combine the retrieved activity data with the traveler's preferences and produce structured recommendations.

---

### Activity Agent and TravelState

The Activity Agent uses the existing shared `TravelState`.

Relevant inputs include:

    destination
    duration
    travelers
    budget
    preferences

The Activity Agent produces:

    activities

The state now contains:

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

This provides a consistent communication mechanism between agents.

---

### LangGraph Integration

The Activity Agent was added as a new node in:

    src/graph/travel_graph.py

The graph now contains:

    graph.add_node("destination", destination_agent)
    graph.add_node("stay", stay_agent)
    graph.add_node("activity", activity_agent)

The execution order was updated to:

    graph.add_edge(START, "destination")
    graph.add_edge("destination", "stay")
    graph.add_edge("stay", "activity")
    graph.add_edge("activity", END)

The resulting workflow is:

    START
      |
      v
    Destination Agent
      |
      v
    Stay Agent
      |
      v
    Activity Agent
      |
      v
    END

---

### Complete Multi-Agent Progression

The project has now progressed from one agent to three specialized agents.

#### Destination Agent

    TravelState
         |
         v
    Destination Agent
         |
         v
    Gemini
         |
         v
    DestinationAnalysis
         |
         v
    destination_data

#### Stay Agent

    TravelState
         |
         v
    Stay Agent
         |
         v
    Gemini
         |
         v
    Tool Calling
         |
         v
    Accommodation Tool
         |
         v
    Accommodation Data
         |
         v
    Structured Output
         |
         v
    StayAnalysis
         |
         v
    stay_options

#### Activity Agent

    TravelState
         |
         v
    Activity Agent
         |
         v
    Gemini
         |
         v
    Tool Calling
         |
         v
    Activity Search Tool
         |
         v
    Activity Data
         |
         v
    Structured Output
         |
         v
    ActivityAnalysis
         |
         v
    activities

---

### Full Current Graph

The current travel planning graph is:

                         START
                           |
                           v
                  Destination Agent
                           |
                           v
                     Stay Agent
                           |
                           v
                   Activity Agent
                           |
                           v
                          END

The three agents communicate through the shared `TravelState`.

---

### Activity Agent Test Coverage

The existing graph test was extended to verify the Activity Agent output.

The test now verifies:

    result["activities"]["recommended_activities"]

    result["activities"]["activities_by_category"]

    result["activities"]["budget_assessment"]

    result["activities"]["activity_recommendation"]

The complete test suite was executed using:

    python -m pytest

Result:

    6 passed, 1 warning

The warning originates from the installed Google GenAI dependency and is a deprecation warning rather than a failure in the project code.

---

### Refactoring Decision

The Activity Agent and Stay Agent currently contain similar tool-calling patterns.

Both agents perform:

    Build Prompt
        |
        v
    Bind Tool
        |
        v
    Invoke LLM
        |
        v
    Execute Tool
        |
        v
    Create ToolMessage
        |
        v
    Structured Output

A reusable abstraction could eventually reduce this duplication.

However, only two tool-using agents currently exist.

Creating a generic abstraction at this stage would introduce additional complexity without enough evidence that the abstraction is necessary.

Therefore, the current implementation intentionally keeps the logic explicit.

A reusable helper can be introduced later when more tool-using agents such as Food, Weather, or other specialized agents are implemented.

This avoids premature abstraction while keeping the architecture easy to understand.

---

### Current Implementation Status

The Activity Agent implementation is complete for the current development stage.

Completed:

- Activity Pydantic schemas
- Activity Search Tool
- Activity Agent
- Gemini tool calling
- Structured ActivityAnalysis output
- TravelState integration
- LangGraph integration
- Activity tool testing
- Activity agent testing
- Full graph testing
- Implementation documentation

Current architecture:

    START
      |
      v
    Destination Agent
      |
      v
    Stay Agent
      |
      v
    Activity Agent
      |
      v
    END

The Activity Agent currently uses controlled activity data.

A real external activity data source will be introduced later as the project progresses toward more realistic travel planning.

---

### Next Planned Features

The next stages of the project can extend the graph with additional specialized agents and capabilities.

Planned future agents include:

    Weather Agent
    Food Agent
    Itinerary Agent

Future engineering improvements include:

    Real external APIs
    Parallel workflows
    Conditional workflows
    MCP integration
    Persistence
    Error handling
    FastAPI integration
    Streamlit frontend
    Testing improvements
    Docker
    CI/CD

These features will be implemented progressively rather than introduced all at once.

---

### Implementation Conclusion

The Activity Agent extends the AI Travel Planner from a two-agent workflow to a three-agent workflow.

The current architecture demonstrates:

    Specialized Agents
          +
    Shared State
          +
    Tool Calling
          +
    Structured Output
          +
    LangGraph Orchestration

The Activity Agent also establishes an important foundation for the future Itinerary Agent.

The future Itinerary Agent will be able to consume:

    destination_data
          +
    stay_options
          +
    activities
          |
          v
    Day-by-Day Travel Itinerary

This makes the Activity Agent an important intermediate component in the overall multi-agent travel planning system.

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