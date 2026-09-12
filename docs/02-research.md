# AI Travel Planner — Research

## 1. Purpose of This Research

Before implementing AI Travel Planner, we need to understand the technologies, architectural patterns, and Agentic AI concepts that will be used in the project.

The purpose of this research is to answer:

- What technologies should we use?
- Why are they suitable for this project?
- How will the technologies work together?
- Which Agentic AI concepts will we demonstrate?
- Which technologies should be introduced later instead of from the beginning?

The project is intentionally designed as an intermediate Agentic AI project, so every technology should have a practical purpose.

---

## 2. Proposed Technology Stack

The initial technology stack is:

### Frontend

- Streamlit

### Backend

- FastAPI
- Pydantic

### AI / LLM

- Google Gemini
- LangChain
- LangGraph

### Agentic AI

- AI Agents
- Multi-Agent Architecture
- Agent Orchestration
- Shared State
- Tool Calling
- Structured Output
- Conditional Workflows
- Parallel Workflows
- MCP

### External Services

- Web Search
- Weather API
- Places / Maps API
- Other travel-related APIs where useful

### Engineering

- Python
- Pytest
- Git
- GitHub
- Docker
- GitHub Actions

### Persistence

- PostgreSQL
- LangGraph persistence/checkpointing where appropriate

---

## 3. Why Python?

Python will be the primary programming language.

Reasons:

- Strong ecosystem for AI and Machine Learning
- Excellent support for LLM applications
- Strong LangChain and LangGraph ecosystem
- Large number of API and automation libraries
- Easy integration with FastAPI
- Good testing ecosystem
- Suitable for rapid development

The project will use modern Python practices such as:

- Type hints
- Functions and classes
- Modular code
- Environment variables
- Exception handling
- Pydantic models
- Testing

---

## 4. Why Gemini?

Google Gemini will be the initial LLM provider.

Gemini will be responsible for tasks such as:

- Understanding travel requirements
- Reasoning about travel preferences
- Generating recommendations
- Summarizing external information
- Producing itinerary content
- Generating structured travel-planning information

Gemini is our initial provider because the project is being designed around Google Gemini.

However, the architecture should avoid unnecessary provider lock-in.

The project should separate:

    Agent Logic
        |
        v
    LLM Interface
        |
        v
    Gemini

This allows the provider layer to be changed later if required.

---

## 5. Why LangChain?

LangChain provides abstractions and integrations for working with:

- Language models
- Tools
- Agents
- Structured output
- Agent workflows

For this project, LangChain will mainly help us connect the LLM with tools and create reusable AI components.

Conceptually:

    Agent
      |
      +----> LLM
      |
      +----> Tools
      |
      +----> Structured Output

LangChain will therefore act as an important building block inside the Agentic AI layer.

---

## 6. Why LangGraph?

LangGraph will be one of the most important technologies in this project.

LangGraph is designed for building stateful, multi-step agent workflows and provides orchestration capabilities.

Our project needs an orchestration layer because multiple agents need to work together.

Conceptually:

    User Request
         |
         v
    LangGraph
    Orchestrator
         |
    +----+----+----+
    |    |    |    |
    v    v    v    v
   Agent Agent Agent Agent
    |    |    |    |
    +----+----+----+
         |
         v
    Final Result

LangGraph will manage:

- Nodes
- Edges
- State
- Workflow execution
- Conditional routing
- Parallel execution
- Agent coordination
- Persistence/checkpointing where required

---

## 7. LangGraph as the Orchestrator

The orchestrator is responsible for controlling the workflow.

In our project, LangGraph will determine:

- Which agent executes
- Which agents can execute independently
- What information is passed to the next agent
- When the workflow should continue
- When a different path should be taken
- When the final itinerary should be generated

The orchestrator can be thought of as the workflow manager.

    User
      |
      v
    Orchestrator
      |
      +--> Destination Agent
      |
      +--> Stay Agent
      |
      +--> Activity Agent
      |
      +--> Weather Agent
      |
      +--> Food Agent
      |
      +--> Itinerary Agent
      |
      v
    Final Response

---

## 8. AI Agent

An AI agent combines a language model with tools and task-specific instructions.

An agent can:

1. Understand a task
2. Reason about what needs to be done
3. Decide whether a tool is required
4. Use a tool
5. Process the result
6. Produce a result

Conceptually:

    Task
      |
      v
    LLM
      |
      v
    Reason
      |
      v
    Select Tool
      |
      v
    Execute Tool
      |
      v
    Observe Result
      |
      v
    Final Result

Our agents will be specialized rather than making one large general-purpose travel agent.

---

## 9. Multi-Agent System

A multi-agent system contains multiple specialized agents that collaborate to solve a larger problem.

Our travel planning problem can be divided into:

    Travel Planning
    |
    +-- Destination Research
    |
    +-- Stay Research
    |
    +-- Activity Research
    |
    +-- Food Research
    |
    +-- Weather Research
    |
    +-- Itinerary Generation

Each responsibility can be handled by a specialized agent.

Example:

    Travel Request
         |
         v
    +----+----+----+----+
    |    |    |    |    |
    v    v    v    v    v
   Dest Stay Activity Food Weather
   Agent Agent Agent   Agent Agent
    |    |    |    |    |
    +----+----+----+----+
              |
              v
        Itinerary Agent
              |
              v
        Final Travel Plan

This is the main reason AI Travel Planner qualifies as a Multi-Agent Agentic AI project.

---

## 10. Shared State

Multiple agents need access to common information.

A shared state allows the workflow to maintain information throughout execution.

A simplified TravelState may contain:

    TravelState

    destination
    travel_dates
    duration
    travelers
    budget
    preferences
    destination_data
    stay_options
    activities
    restaurants
    weather
    itinerary

Example flow:

    User Input
        |
        v
    TravelState
        |
        +--> Destination Agent
        |       |
        |       v
        |   destination_data
        |
        +--> Stay Agent
        |       |
        |       v
        |   stay_options
        |
        +--> Activity Agent
        |       |
        |       v
        |    activities
        |
        +--> Weather Agent
                |
                v
             weather

The Itinerary Agent can use the information collected in the state.

---

## 11. Nodes and Edges

LangGraph represents workflows as graphs.

A graph contains:

- Nodes
- Edges
- State

### Nodes

A node represents a unit of work.

Examples:

    Destination Agent
    Stay Agent
    Activity Agent
    Weather Agent
    Itinerary Agent

### Edges

An edge defines how the workflow moves from one node to another.

Example:

    Destination Agent
            |
            v
       Activity Agent
            |
            v
       Itinerary Agent

Edges can also be conditional.

---

## 12. Conditional Workflow

A conditional workflow allows the system to choose the next step based on the current state or result.

Example:

    Weather Agent
          |
          v
    Is weather suitable?
       /          \
     Yes           No
      |             |
      v             v
   Outdoor       Indoor
   Activities    Activities

Another example:

    Budget Check
       |
    +--+--+
    |     |
    v     v
  Valid  Invalid
    |       |
    v       v
 Continue  Adjust
 Planning  Recommendations

Conditional routing will make the travel planner more intelligent than a fixed sequence of functions.

---

## 13. Parallel Workflow

Some travel-planning tasks do not depend on one another.

For example:

- Hotel research
- Weather research
- Activity research
- Food research

may be performed independently.

Instead of:

    Hotel
      |
      v
    Weather
      |
      v
    Activities
      |
      v
    Food

we can design:

    Travel Request
         |
         v
    Orchestrator
         |
    +----+----+----+
    |    |    |    |
    v    v    v    v
   Stay Weather Activity Food
   Agent Agent   Agent   Agent
    |    |    |    |
    +----+----+----+
         |
         v
    Itinerary Agent

Parallel execution can reduce unnecessary waiting and demonstrates an important orchestration pattern.

---

## 14. Tool Calling

Tools allow agents to interact with external systems.

Without tools:

    User
      |
      v
    LLM
      |
      v
    Answer

With tools:

    User
      |
      v
    Agent
      |
      v
    LLM
      |
      v
    Tool Selection
      |
      v
    External Tool
      |
      v
    Result
      |
      v
    Agent
      |
      v
    Answer

Potential tools for AI Travel Planner:

- Web search
- Weather lookup
- Places search
- Restaurant search
- Location lookup

Tools will provide real-world information that should not be generated purely from the LLM.

---

## 15. External APIs

External APIs will provide real-world travel information.

Potential categories include:

### Search API

Used for:

- Destination research
- Travel information
- Recommendations
- Current information

### Weather API

Used for:

- Temperature
- Weather conditions
- Rain probability
- Forecast information

### Places / Maps API

Used for:

- Locations
- Attractions
- Restaurants
- Nearby places
- Geographic information

The exact providers will be selected during implementation based on:

- API availability
- Free-tier availability
- Reliability
- Documentation
- Ease of integration
- Project requirements

---

## 16. Structured Output

LLMs normally generate free-form text.

For an application, this can become difficult to process reliably.

Example of free-form output:

    The hotel looks good and costs around ₹5000.
    It is near the beach and has good reviews.

Structured output instead provides predictable fields.

Example:

    hotel:
        name: Example Hotel
        price_per_night: 5000
        location: Near Beach
        rating: 4.3

Structured output is important because the result of one agent may become input for another agent.

Possible structured models:

    DestinationResult
    StayResult
    ActivityResult
    WeatherResult
    RestaurantResult
    ItineraryResult

Pydantic models can be used to validate these structures.

---

## 17. Pydantic

Pydantic will be used for validation and structured data models.

For example, the travel request may contain:

    destination
    duration
    travelers
    budget
    preferences

Pydantic can validate whether the input has the expected structure and data types.

This will be especially useful with FastAPI.

Conceptually:

    User Input
        |
        v
    Pydantic Validation
        |
        +---- Valid ----> Continue
        |
        +---- Invalid --> Error Response

---

## 18. FastAPI

FastAPI will provide the backend API.

The backend will sit between the frontend and the Agentic AI workflow.

Architecture:

    Streamlit
        |
        v
    FastAPI
        |
        v
    LangGraph
        |
        v
    Agents
        |
        v
    Tools / APIs
        |
        v
    Final Result

FastAPI will handle:

- HTTP requests
- Request validation
- API endpoints
- Error responses
- Calling the LangGraph workflow
- Returning structured results

---

## 19. Streamlit

Streamlit will be used for the initial frontend.

The frontend should remain simple.

Possible inputs:

    Destination
    Travel Dates
    Duration
    Number of Travelers
    Budget
    Preferences

Possible outputs:

    Destination Overview
    Stay Recommendations
    Weather
    Activities
    Restaurants
    Day-by-Day Itinerary
    Estimated Budget

The main purpose of the frontend is to provide an easy way to interact with the Agentic AI system.

The project focus remains on the backend and Agentic AI architecture.

---

## 20. MCP

MCP stands for **Model Context Protocol**.

MCP provides a standardized approach for connecting AI applications with external tools and resources.

Conceptually:

    AI Application
          |
          v
         MCP
          |
    +-----+-----+-----+
    |           |     |
    v           v     v
  Search     Weather  Places

MCP will be introduced after the basic tool-calling architecture is understood.

The learning order will therefore be:

    Normal Tool
        |
        v
    Tool Calling
        |
        v
    External API
        |
        v
    Understand MCP
        |
        v
    MCP Integration

This prevents MCP from becoming a black-box technology in the project.

---

## 21. LLM Abstraction

The application should not tightly couple all agents to Gemini-specific implementation details.

The desired architecture is:

    Agent
      |
      v
    LLM Interface
      |
      +---------> Gemini
      |
      +---------> OpenAI
      |
      +---------> Anthropic

The first implementation will use Gemini.

The abstraction exists so that changing the provider later does not require rewriting every agent.

---

## 22. Persistence

The project may need to persist:

- Conversation state
- Travel planning state
- User requests
- Workflow checkpoints
- Previous planning sessions

PostgreSQL is the planned persistence layer if persistence is required by the final architecture.

LangGraph also provides persistence/checkpointing capabilities that can be used for stateful workflows.

Persistence will be introduced after the basic workflow is functioning.

---

## 23. Error Handling

Agentic systems interact with external services, so failures are expected.

Potential failures include:

- API timeout
- Invalid API response
- Rate limit
- Tool failure
- LLM failure
- Invalid structured output
- Missing user input
- Network error

The system should not simply crash.

Conceptually:

    Agent
      |
      v
    Tool
      |
    +--+----------------+
    |                   |
  Success              Failure
    |                   |
    v                   v
 Continue          Retry / Fallback
                        |
                        v
                  Error Response

Error handling will be added progressively.

---

## 24. Testing

Testing will be performed at different levels.

### Unit Testing

Test individual functions and components.

Examples:

- Input validation
- Budget calculations
- Data transformations
- Tool wrappers

### Agent Testing

Test whether an agent produces the expected structured result.

### Workflow Testing

Test whether the LangGraph workflow moves through the expected nodes.

### API Testing

Test FastAPI endpoints.

### Integration Testing

Test interactions with selected external services where practical.

Pytest will be used as the primary testing framework.

---

## 25. Docker

Docker will be introduced during the production-polish stage.

The objective is to make the application environment reproducible.

Conceptually:

    Source Code
        |
        v
      Docker
        |
        v
    Application
        |
        +--> FastAPI
        +--> Streamlit
        +--> Agentic Workflow

Docker will not be introduced before the application is stable enough to containerize.

---

## 26. GitHub Actions

GitHub Actions will be used for basic CI/CD automation.

Potential workflow:

    Git Push
       |
       v
    GitHub Actions
       |
       +--> Install Dependencies
       |
       +--> Run Tests
       |
       +--> Check Code
       |
       v
    Build / Deploy

The initial goal is reliable automated testing rather than a complicated CI/CD pipeline.

---

## 27. Deployment

Deployment will be considered after the application is stable.

The deployment target will be selected based on:

- Cost
- Simplicity
- Python/FastAPI support
- Streamlit support
- Project requirements

Deployment is a final-stage activity and should not distract from learning the core Agentic AI architecture.

---

## 28. Technology Relationship

The technologies have different responsibilities.

    Streamlit
    Frontend
        |
        v
    FastAPI
    Backend API
        |
        v
    LangGraph
    Orchestration
        |
        v
    LangChain
    Agent / Tool / LLM Integration
        |
        v
    Gemini
    Language Model
        |
        v
    Tools / APIs
    Real-World Information

Additional engineering:

    Pydantic
    Validation / Structured Data

    PostgreSQL
    Persistence

    Pytest
    Testing

    Docker
    Containerization

    GitHub Actions
    CI/CD

    MCP
    Standardized Tool / Resource Integration

---

## 29. Why We Are Not Using Everything Immediately

Although the final project may contain many technologies, they will not all be introduced on the first day.

The learning order is intentional.

### Phase 1

Understand:

    LLM
    Agent
    Tool
    LangChain
    LangGraph
    State

### Phase 2

Build:

    Single Agent
        |
        v
    Tool Calling
        |
        v
    External API

### Phase 3

Expand:

    Multiple Agents
        |
        v
    Shared State
        |
        v
    LangGraph Orchestration

### Phase 4

Improve:

    Structured Output
    Conditional Workflow
    Parallel Workflow
    Error Handling

### Phase 5

Add advanced capabilities:

    MCP
    LLM Abstraction
    Persistence

### Phase 6

Production engineering:

    Testing
    Docker
    GitHub Actions
    Deployment

This sequence allows each concept to be understood before it becomes part of the implementation.

---

## 30. Reference Architecture

The current target architecture is:

    +---------------------------------------------------+
    |                   Streamlit UI                   |
    +-------------------------+-------------------------+
                              |
                              v
    +---------------------------------------------------+
    |                     FastAPI                      |
    +-------------------------+-------------------------+
                              |
                              v
    +---------------------------------------------------+
    |                LangGraph Orchestrator             |
    +-------------------------+-------------------------+
                              |
                              v
    +---------------------------------------------------+
    |                  Shared Travel State              |
    +-------------------------+-------------------------+
                              |
              +---------------+---------------+
              |               |               |
              v               v               v
        Destination        Stay           Activity
           Agent           Agent             Agent
              |               |               |
              +---------------+---------------+
                              |
              +---------------+---------------+
              |               |
              v               v
          Weather           Food
           Agent            Agent
              |               |
              +---------------+
                      |
                      v
              Itinerary Agent
                      |
                      v
              Structured Output
                      |
                      v
                Final Response

External capabilities:

    Agents
      |
      +--> Web Search
      +--> Weather API
      +--> Places / Maps API
      +--> MCP Tools
      |
      v
    Real-World Information

LLM layer:

    Agents
      |
      v
    LLM Interface
      |
      v
    Gemini

Future provider support:

    LLM Interface
      |
      +--> Gemini
      +--> OpenAI
      +--> Anthropic

---

## 31. Research Conclusions

The research indicates that the selected technologies fit the requirements of AI Travel Planner.

### LangGraph

Best suited for:

- Workflow orchestration
- Stateful workflows
- Multi-step agent execution
- Conditional routing
- Parallel workflow design
- Persistence capabilities

### LangChain

Best suited for:

- Model integration
- Tool integration
- Agent abstractions
- Structured output
- LLM application components

### Gemini

Best suited as:

- Initial LLM provider
- Reasoning and generation layer
- Travel recommendation generation

### FastAPI

Best suited for:

- Backend API
- Request validation
- Integration between frontend and Agentic workflow

### Streamlit

Best suited for:

- Rapid frontend development
- Simple user interaction
- Displaying travel-planning results

### Pydantic

Best suited for:

- Input validation
- Structured data
- Agent output schemas

### MCP

Best suited as:

- Advanced standardized tool/resource integration
- A later-stage Agentic AI feature

### PostgreSQL

Best suited for:

- Persistence
- Conversation/workflow data
- Future application state

### Docker

Best suited for:

- Reproducible environments
- Application packaging

### GitHub Actions

Best suited for:

- Automated testing
- CI/CD

---

## 32. Research Sources

The primary research sources for this document are official documentation from:

- LangGraph Documentation
- LangChain Documentation
- Google Gemini / Google AI Documentation
- Model Context Protocol Documentation
- FastAPI Documentation
- Pydantic Documentation
- Streamlit Documentation
- PostgreSQL Documentation
- Docker Documentation
- GitHub Actions Documentation

Official documentation should be preferred over tutorials or third-party explanations when making implementation decisions.

---

## 33. Research Decision

Based on the research, the project will proceed with:

    Python
      +
    Streamlit
      +
    FastAPI
      +
    Pydantic
      +
    LangChain
      +
    LangGraph
      +
    Gemini
      +
    External Tools / APIs
      +
    PostgreSQL
      +
    Pytest
      +
    MCP
      +
    Docker
      +
    GitHub Actions

The technologies will be introduced progressively according to the project's development workflow.

The project will prioritize understanding and implementation over adding unnecessary technologies.

## Structured Output

### What is Structured Output?

Structured output allows an LLM to return information according to a predefined schema instead of returning only free-form text.

Without structured output:

    Gemini
       ↓
    Free-form text
       ↓
    Application must interpret the text

With structured output:

    Gemini
       ↓
    Predefined schema
       ↓
    Structured data
       ↓
    Application can consume predictable fields

For the AI Travel Planner, structured output is important because multiple agents will exchange information through the shared `TravelState`.

---

### Why Structured Output is Important for AI Travel Planner

The current Destination Agent stores the Gemini response as:

    destination_data = {
        "analysis": response.content
    }

This works for basic experimentation, but it is not ideal for a multi-agent system.

Future agents should be able to consume specific information without parsing an arbitrary paragraph.

For example:

    destination_data
        ├── overview
        ├── recommended_areas
        ├── travel_considerations
        └── preference_suggestions

This makes communication between agents more predictable and easier to validate.

---

### Structured Output vs Free-Form Output

| Aspect | Free-Form Output | Structured Output |
|---|---|---|
| Response format | Unpredictable text | Predefined structure |
| Application parsing | More difficult | Easier |
| Validation | Limited | Schema-based |
| Agent-to-agent communication | Less reliable | More predictable |
| Data extraction | Requires parsing | Direct field access |
| Maintainability | Lower | Higher |

---

## Pydantic

### What is Pydantic?

Pydantic is a Python library used to define and validate structured data using Python type annotations.

For our project, Pydantic will be used to define the expected structure of agent responses.

Example conceptual model:

    class DestinationAnalysis(BaseModel):
        overview: str
        recommended_areas: list[str]
        travel_considerations: list[str]
        preference_suggestions: list[str]

This model defines exactly what information the Destination Agent should produce.

---

### Why Pydantic?

Pydantic provides:

- Explicit data models
- Python type hints
- Runtime validation
- Predictable data structures
- Easier integration with structured LLM output
- Better maintainability

This is especially useful when multiple agents exchange data through a shared state.

---

## Planned DestinationAnalysis Schema

The first structured response model will be:

    DestinationAnalysis
    ├── overview: str
    ├── recommended_areas: list[str]
    ├── travel_considerations: list[str]
    └── preference_suggestions: list[str]

### Field Descriptions

#### overview

A concise explanation of why the destination is suitable for the user's trip.

#### recommended_areas

A list of areas or locations that are relevant to the user's trip.

#### travel_considerations

Important considerations related to visiting the destination.

#### preference_suggestions

Suggestions specifically related to the traveler's stated preferences.

---

## LangChain Structured Output

Because the project uses LangChain, structured output will be integrated through the LangChain LLM abstraction rather than creating a separate Google-specific implementation inside the agent.

Conceptually:

    Destination Agent
            ↓
        LLM Service
            ↓
    ChatGoogleGenerativeAI
            ↓
    Structured Output
            ↓
    DestinationAnalysis
            ↓
       TravelState

This maintains separation between:

- Agent logic
- LLM configuration
- Response schema

---

## Gemini Structured Output

Gemini supports structured output using a defined response schema.

For this project, the schema will be represented using a Pydantic model and connected to the LangChain Gemini model.

The intended implementation direction is:

    Pydantic Model
          ↓
    Structured Output Configuration
          ↓
    Gemini 3.5 Flash-Lite
          ↓
    Structured Response
          ↓
    Pydantic Validation

---

## Structured Output Validation

Structured output does not automatically guarantee that the generated information is factually correct.

Two different concerns must be considered:

### Schema Validation

Does the response follow the expected structure?

Example:

    overview → string
    recommended_areas → list of strings

### Semantic Correctness

Is the information actually useful and accurate?

For example, a response can follow the correct schema but still contain an incorrect recommendation.

Therefore, structured output solves the **format and validation problem**, but it does not by itself solve the **factual accuracy problem**.

External tools and APIs will later be introduced to provide real travel information.

---

## Structured Output in the Multi-Agent Architecture

The structured Destination Agent will eventually provide information that other agents can consume.

    Destination Agent
            │
            ▼
    DestinationAnalysis
            │
            ▼
       TravelState
            │
      ┌─────┼─────┐
      ▼     ▼     ▼
    Stay  Activity Food
    Agent   Agent  Agent

This creates a predictable data flow between specialized agents.

---

## Implementation Decision

For the first structured-output implementation:

- Use Pydantic models
- Use LangChain structured output capabilities
- Continue using Gemini 3.5 Flash-Lite
- Keep the existing LLM service abstraction
- Keep the Destination Agent as the first consumer
- Store structured destination information in `TravelState`

The implementation will remain intentionally small before adding external tools or additional agents.

---

## Research Conclusion

Structured output is an important transition point for the AI Travel Planner.

The project will move from:

    LLM
      ↓
    Free-form text
      ↓
    destination_data["analysis"]

to:

    LLM
      ↓
    Structured Output
      ↓
    Pydantic Model
      ↓
    destination_data

This provides a stronger foundation for reliable multi-agent communication and future tool integration.

## Stay / Hotel Agent Research

The Stay Agent is responsible for researching and evaluating accommodation options based on the traveler's requirements.

The agent will consider information such as:

- destination
- travel dates
- duration
- number of travelers
- budget
- preferred areas
- traveler preferences

The goal is to provide useful accommodation recommendations while keeping the agent focused on the accommodation domain.

### Why a Separate Stay Agent?

The Destination Agent is responsible for understanding the destination, while the Stay Agent focuses specifically on accommodation.

Separating these responsibilities follows the multi-agent design principle of giving each agent a focused task.

    Travel Request
          |
          v
    LangGraph Orchestrator
          |
          +-------------------+
          |                   |
          v                   v
    Destination Agent     Stay Agent
          |                   |
          v                   v
    Destination Data      Stay Data

This separation improves:

- responsibility isolation
- maintainability
- testing
- scalability
- agent-to-agent communication

### Stay Agent and Tool Calling

The Stay Agent will introduce tool calling into the AI Travel Planner.

Structured output and tool calling solve different problems.

#### Structured Output

Structured output controls the format of the final model response.

    Gemini
       |
       v
    Pydantic Schema
       |
       v
    Structured Result

For example, the Destination Agent produces a `DestinationAnalysis` object with predefined fields.

#### Tool Calling

Tool calling allows the LLM to request an external function when it needs additional information or needs to perform an operation.

    Stay Agent
         |
         v
      Gemini
         |
         v
     Tool Call
         |
         v
    Search Tool
         |
         v
    External Data
         |
         v
      Gemini
         |
         v
    Final Response

The application, rather than the LLM itself, executes the requested tool and provides the tool result back to the model.

### Difference Between Structured Output and Tool Calling

| Concept | Purpose |
|---|---|
| Structured Output | Controls the format of model output |
| Tool Calling | Allows the model to request an external function |
| Pydantic | Defines and validates structured data |
| External Tool/API | Provides external information or performs an operation |
| LangChain | Connects the LLM with tools and model capabilities |
| LangGraph | Orchestrates the overall application workflow |

Both structured output and tool calling will be used together in the Stay Agent.

### Accommodation Search Tool

The initial tool interface will be designed around a focused function such as:

    search_accommodations(
        destination,
        check_in,
        check_out,
        travelers,
        budget
    )

The tool should return accommodation-related information that the Stay Agent can evaluate.

A conceptual result may contain:

    [
        {
            name: "...",
            area: "...",
            price: ...,
            rating: ...,
            url: "..."
        }
    ]

The exact external provider will be selected during implementation after evaluating API availability, access requirements, reliability, and project complexity.

### Provider Independence

The Stay Agent should not be tightly coupled to a specific accommodation provider.

The application should interact with a tool interface such as:

    search_accommodations()

The underlying implementation can later use:

- a hotel/accommodation API
- a web search provider
- an MCP-based tool
- another suitable external travel data source

This provides flexibility and allows the external provider to be changed without redesigning the agent.

### StayAnalysis Schema

The Stay Agent will use structured output similar to the Destination Agent.

A proposed schema is:

    StayAnalysis
    ├── recommended_area
    ├── accommodation_options
    ├── budget_assessment
    └── stay_recommendation

Individual accommodation records may contain:

    Accommodation
    ├── name
    ├── area
    ├── price
    ├── rating
    ├── description
    └── url

The exact fields will be finalized before implementation.

### LangChain and Tool Calling

LangChain will provide the model/tool integration layer.

Conceptually:

    LangChain
        |
        +── LLM
        |
        +── Tools
        |
        +── Tool Calling

LangGraph will remain responsible for the larger travel-planning workflow:

    LangGraph
        |
        +── Destination Agent
        |
        +── Stay Agent
        |
        +── Activity Agent
        |
        +── Food Agent
        |
        +── Weather Agent
        |
        +── Itinerary Agent

This maintains a clear separation between model/tool interaction and workflow orchestration.

### Planned Stay Agent Flow

The planned implementation is:

    User Travel Request
            |
            v
       TravelState
            |
            v
       Stay Agent
            |
            v
        Gemini LLM
            |
            v
        Tool Calling
            |
            v
    Accommodation Search Tool
            |
            v
      External Data
            |
            v
        Gemini LLM
            |
            v
     Pydantic StayAnalysis
            |
            v
       TravelState

This will be the first agent in the project that combines:

- LLM reasoning
- external tool usage
- structured output
- shared graph state

### Accommodation Data Source Strategy

The project will avoid introducing a complex hotel-booking integration at this stage.

The first implementation will focus on understanding and implementing the tool-calling architecture with a clean tool interface.

The external data source can then be replaced or upgraded without changing the overall agent architecture.

This approach keeps the project intermediate in scope while still demonstrating an important Agentic AI pattern.

### Research Decision

The Stay Agent will use the following design:

    Stay Agent
         |
         +── Gemini
         |
         +── Accommodation Search Tool
         |
         +── Pydantic Structured Output
         |
         v
      TravelState

The implementation will be provider-independent where practical.

MCP may be introduced later as part of the project's advanced Agentic AI features rather than being forced into the first Stay Agent implementation.

### Research Conclusion

The Stay Agent will extend the current AI Travel Planner architecture from a single structured-output agent to an agent capable of interacting with external tools.

The key architectural progression is:

    Destination Agent

        LLM
         |
         v
    Structured Output
         |
         v
    DestinationAnalysis

    Stay Agent

        LLM
         |
         v
    Tool Calling
         |
         v
    External Data
         |
         v
    Structured Output
         |
         v
    StayAnalysis

This progression establishes the foundation for future Activity, Food, Weather, and Itinerary agents while keeping each component focused and independently testable.

### Research Sources

- Gemini Function Calling documentation — Google AI
- Gemini Tools documentation — Google AI
- Gemini Structured Output documentation — Google AI
- LangChain Agents and Tool Calling documentation — LangChain
- LangGraph documentation — LangChain

## Weather Agent Research

### 1. Purpose

The Weather Agent is responsible for retrieving and interpreting weather information relevant to a travel plan.

Weather is different from destination, accommodation, and activity research because it is **time-sensitive external information**.

The Weather Agent should therefore not rely on the LLM's internal knowledge to provide current or forecast weather information.

The architecture should be:

    Weather API
        ↓
    Weather Tool
        ↓
    Weather Agent / LLM
        ↓
    Structured Weather Analysis
        ↓
    TravelState

The Weather API provides factual weather data, while the LLM interprets that information in the context of the traveler's trip.

---

### 2. Why a Separate Weather Agent?

Weather affects several travel-planning decisions:

- Whether outdoor activities are suitable
- Whether beach activities should be recommended
- Whether alternative indoor activities are needed
- Whether rain may affect the itinerary
- Whether particular travel days require flexibility
- Whether weather conditions are generally suitable for the planned trip

A dedicated Weather Agent keeps this responsibility separate from other agents.

This follows the multi-agent design principle used throughout the project:

    One agent = one specialized responsibility

The Weather Agent focuses specifically on weather analysis and travel-related weather recommendations.

---

### 3. Weather Data Source

Several weather APIs were considered:

- WeatherAPI.com
- Open-Meteo
- OpenWeatherMap

For the initial implementation, **WeatherAPI.com** is selected.

Reasons:

- Simple REST API
- Supports city-name input
- Provides current weather information
- Provides forecast information
- Provides daily and hourly forecast data
- Supports forecasts for multiple days
- Returns structured JSON data
- Easy to integrate with a Python tool

The API can therefore act as the factual data source for the Weather Tool.

---

### 4. Weather Tool

The Weather Agent should use a dedicated LangChain tool to retrieve weather information.

Conceptually:

    search_weather(
        destination,
        travel_dates,
        duration
    )

The tool will:

1. Receive the destination and travel requirements.
2. Call the weather API.
3. Extract relevant weather information.
4. Return useful weather data to the Weather Agent.

The tool should avoid returning unnecessary API fields.

Relevant information may include:

- Date
- Temperature
- Feels-like temperature
- Weather condition
- Rain probability
- Precipitation
- Wind

The Weather Tool is responsible for **retrieving factual information**, not making the final travel recommendation.

---

### 5. API Data vs LLM Interpretation

An important architectural principle is:

    API = factual information
    LLM = interpretation

The application should not ask the LLM to directly predict weather.

Incorrect approach:

    User
      ↓
    Gemini
      ↓
    "What will the weather be in Goa?"

This could result in outdated or hallucinated information.

Instead:

    User
      ↓
    Weather Agent
      ↓
    Weather Tool
      ↓
    Weather API
      ↓
    Actual Weather Data
      ↓
    Gemini
      ↓
    Travel-oriented interpretation

For example:

    Weather API

    Day 1 → 29°C, Sunny, 10% rain
    Day 2 → 28°C, Cloudy, 35% rain
    Day 3 → 26°C, Heavy Rain, 80% rain

The LLM can then interpret the information:

    Day 1 → Good for outdoor activities
    Day 2 → Suitable with some flexibility
    Day 3 → Prefer indoor activities

This separation improves reliability because the LLM does not generate the underlying weather facts.

---

### 6. Weather Analysis

The Weather Agent should transform raw weather information into a structured travel-oriented analysis.

A possible structure is:

    WeatherAnalysis

        forecast_summary
        temperature_summary
        precipitation_summary
        travel_assessment
        weather_recommendation

#### Forecast Summary

Provides a concise overview of the expected weather during the trip.

#### Temperature Summary

Summarizes temperature conditions relevant to the traveler.

#### Precipitation Summary

Highlights rain probability and precipitation conditions.

#### Travel Assessment

Explains how the weather may affect travel and planned activities.

#### Weather Recommendation

Provides practical recommendations such as:

- Suitable days for outdoor activities
- Days requiring flexibility
- Possible indoor alternatives
- General weather-related travel advice

---

### 7. Structured Output

The Weather Agent should use Pydantic structured output, consistent with the other agents.

Conceptually:

    Weather API
        ↓
    Weather Tool
        ↓
    Weather Data
        ↓
    Gemini
        ↓
    WeatherAnalysis
        ↓
    TravelState

Structured output provides a predictable format for the rest of the LangGraph workflow.

This is important because the Itinerary Agent will eventually consume information from multiple agents, including weather information.

---

### 8. Weather Information in Shared State

The existing TravelState already contains a weather field:

    weather: dict

The Weather Agent will populate this field after processing the weather information.

Conceptually:

    TravelState

        destination
        travel_dates
        duration
        travelers
        budget
        preferences

        destination_data
        stay_options
        activities
        weather
        restaurants
        itinerary

This allows later agents, especially the Itinerary Agent, to use weather information when constructing the final itinerary.

---

### 9. Forecast Limitations

Weather forecasts are time-dependent and become less certain further into the future.

Therefore, the system should not present long-range forecasts as guaranteed facts.

The Weather Agent should work with whatever forecast information is available from the selected weather API.

The application should also distinguish between:

- Available forecast information
- Travel interpretation based on that information

Forecast uncertainty can be improved later, but it is not necessary to over-engineer the first implementation.

---

### 10. LangGraph Integration

The Weather Agent will be added as another node in the existing LangGraph workflow.

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

After adding the Weather Agent:

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

The Weather Agent receives the shared TravelState, retrieves weather information, generates structured analysis, stores the result in the state, and passes the updated state to the next node.

---

### 11. Weather Agent Workflow

The complete Weather Agent workflow is:

    TravelState
        ↓
    Weather Agent
        ↓
    Weather Tool
        ↓
    Weather API
        ↓
    Weather Data
        ↓
    Structured LLM
        ↓
    WeatherAnalysis
        ↓
    TravelState["weather"]

This follows the same architecture already established for the Stay and Activity Agents:

    Agent
      ↓
    Tool
      ↓
    External Data
      ↓
    LLM Interpretation
      ↓
    Structured Output
      ↓
    Shared State

---

### 12. Initial Implementation Decision

For the first implementation:

- WeatherAPI.com will be used as the weather data source.
- A LangChain `search_weather` tool will retrieve weather data.
- The Weather Agent will interpret the retrieved information.
- Pydantic will define the structured WeatherAnalysis output.
- Weather information will be stored in TravelState.
- The Weather Agent will be integrated into the existing sequential LangGraph workflow.

The implementation will initially remain simple.

Future improvements may include:

- More weather APIs
- Better location resolution
- Weather alerts
- More detailed hourly analysis
- Weather-based itinerary adjustments
- MCP-based weather tools
- More advanced conditional workflows

These features will be considered later as the project evolves.

---

### 13. Research Conclusion

The Weather Agent introduces an important capability to the AI Travel Planner: **using external, time-sensitive information and allowing the LLM to interpret that information instead of generating factual data itself.**

The selected architecture is:

    Weather API
        ↓
    Weather Tool
        ↓
    Weather Agent
        ↓
    Structured WeatherAnalysis
        ↓
    TravelState
        ↓
    Itinerary Agent

This design keeps responsibilities separated, improves reliability, and prepares the system for future itinerary optimization based on real-world weather conditions.

### Sources

- WeatherAPI.com Documentation
- Open-Meteo Documentation
- OpenWeatherMap API Documentation
- LangChain Tools Documentation
- LangChain Structured Output Documentation
- LangGraph Documentation

## Food / Restaurant Agent Research

### 1. Purpose

The Food / Restaurant Agent is responsible for finding suitable restaurants and food experiences for the travel destination.

The agent should consider:

    Destination
    Budget
    Traveler preferences
    Food interests
    Location
    Restaurant category
    Ratings
    Price range

The Food Agent should not generate restaurant information purely from the LLM's internal knowledge.

Instead, it should retrieve real place data from an external Places API and then use the LLM to analyze and personalize those results.

The overall architecture is:

    TravelState
        ↓
    Food Agent
        ↓
    Gemini Tool Calling
        ↓
    Restaurant Search Tool
        ↓
    Foursquare Places API
        ↓
    Restaurant Data
        ↓
    Gemini Structured Output
        ↓
    FoodAnalysis
        ↓
    TravelState["restaurants"]

---

### 2. Why a Separate Food Agent?

Food recommendations are an important part of travel planning.

However, restaurant discovery has different requirements from:

    Destination research
    Accommodation search
    Activity research
    Weather analysis

A dedicated Food Agent allows the system to:

    Search restaurants using real location data
    Filter restaurants by price range
    Consider restaurant categories
    Consider traveler preferences
    Rank suitable options
    Generate practical food recommendations

Separating this responsibility also keeps the multi-agent architecture modular.

---

### 3. Selected External API

The project will use the current Foursquare Places API.

Foursquare provides global point-of-interest data and supports place search, discovery, ranking, and location-based queries.

The current Places API provides a dedicated Place Search endpoint:

    https://places-api.foursquare.com/places/search

The API supports searching for places using:

    Query
    Locality
    Latitude/longitude
    Radius
    Category
    Price range
    Rating
    Distance
    Popularity

This makes it suitable for restaurant discovery in a travel planning application.

---

### 4. Why Foursquare Places API?

Foursquare is suitable for this project because its Place Search endpoint supports location-aware place discovery.

The API can search using a locality such as a city or destination and can also use latitude/longitude with a radius.

It supports restaurant-related filtering and ranking through query, category, price, and sorting parameters.

Available sorting options include:

    RELEVANCE
    RATING
    DISTANCE
    POPULARITY

The API also allows limiting the number of returned results.

This gives the Food Agent enough real-world information to retrieve candidate restaurants before the LLM performs the final reasoning.

---

### 5. Current Places API Endpoint

The Food Agent will initially use:

    GET https://places-api.foursquare.com/places/search

The current API version is:

    2025-06-17

The request must include:

    X-Places-Api-Version: 2025-06-17

Authentication is performed using a Foursquare Service Key through:

    Authorization: Bearer <SERVICE_API_KEY>

The API documentation identifies Service Keys as the authentication mechanism for Places API requests.

---

### 6. Authentication

The Foursquare Service API key will be stored in the project's `.env` file.

Example:

    FOURSQUARE_API_KEY=...

The key must never be hardcoded into the source code.

The `.env` file will remain excluded from Git through `.gitignore`.

The application will load the key using `python-dotenv`.

The expected architecture is:

    .env
      ↓
    python-dotenv
      ↓
    Restaurant Search Tool
      ↓
    Authorization: Bearer <API_KEY>
      ↓
    Foursquare Places API

---

### 7. Restaurant Search Tool

A dedicated LangChain tool will be created for restaurant discovery.

Planned file:

    src/tools/restaurant.py

Planned tool:

    search_restaurants()

The tool will receive information required to search for restaurants.

Initial conceptual interface:

    search_restaurants(
        destination: str,
        preferences: list[str],
        max_price: int
    )

The exact interface may be refined during implementation.

The tool will:

1. Load the Foursquare API key.
2. Validate that the API key exists.
3. Build the Places API request.
4. Search for restaurants near the destination.
5. Apply appropriate filters.
6. Request only the fields required by the application.
7. Validate the HTTP response.
8. Parse the API response.
9. Normalize restaurant information.
10. Return restaurant candidates to the Food Agent.

---

### 8. Location Search

The Places API supports multiple ways of specifying the search area.

The Food Agent can use:

    near

for a geocodable locality.

Alternatively, the application can use:

    ll + radius

where:

    ll = latitude,longitude
    radius = search radius in meters

For the initial implementation, the Food Agent will prefer destination-based locality search because our current TravelState contains a destination string but does not yet contain latitude/longitude coordinates.

Example conceptual request:

    destination = "Goa"

The tool can translate this into a locality-based Places API search.

Later, the project can introduce a dedicated location/geocoding capability if more precise geographic searching becomes necessary.

---

### 9. Restaurant Search Query

The Food Agent should not blindly search for the word "restaurant" in every situation.

The search query can incorporate traveler preferences.

Examples:

    vegetarian restaurants
    seafood restaurants
    budget restaurants
    family restaurants
    romantic restaurants
    local cuisine
    cafes
    street food

The LLM can determine the appropriate search intent based on the user's preferences and pass that intent to the Restaurant Search Tool.

This creates the following flow:

    User Preferences
          ↓
    Food Agent
          ↓
    Search Intent
          ↓
    Restaurant Tool
          ↓
    Foursquare

---

### 10. Price Filtering

Foursquare Place Search supports price filtering.

The API defines four price levels:

    1 → Most affordable
    2 → Moderate
    3 → Expensive
    4 → Most expensive

The API supports:

    min_price
    max_price

The Food Agent can use these values to narrow restaurant candidates according to the traveler's budget.

However, the application should not assume that the Foursquare price level directly represents an exact monetary meal cost.

The price level should therefore be treated as a relative affordability signal rather than an exact rupee amount.

---

### 11. Restaurant Ranking

The Places API supports several sorting strategies:

    RELEVANCE
    RATING
    DISTANCE
    POPULARITY

The Food Agent can use these results as candidate rankings.

The final recommendation should still be performed by the LLM because the best restaurant for a traveler is not necessarily the highest-rated restaurant.

For example:

    Traveler preference → vegetarian
    Budget → moderate
    Destination → Goa

The Food Agent should consider all these constraints instead of simply selecting the first API result.

---

### 12. Data Retrieved from the API

The Restaurant Search Tool should normalize only the information required by the application.

Potential restaurant fields include:

    Name
    Address
    Locality
    Categories
    Price level
    Rating
    Distance
    Latitude
    Longitude
    Foursquare place ID

The exact fields requested from the API will be finalized during implementation based on the current Places API response schema.

The tool should avoid unnecessarily passing large raw API responses to the LLM.

---

### 13. API Data vs LLM Responsibilities

The system should clearly separate factual restaurant retrieval from AI reasoning.

#### Foursquare Places API

Responsible for:

    Restaurant discovery
    Location information
    Categories
    Price level
    Ratings
    Distance
    Place identifiers

#### Gemini

Responsible for:

    Understanding traveler preferences
    Comparing restaurant candidates
    Interpreting price levels
    Selecting suitable restaurants
    Explaining why restaurants are recommended
    Producing personalized food recommendations

This follows the same architecture used by the Weather Agent.

The external API provides real-world data.

The LLM provides reasoning and personalization.

---

### 14. Food Analysis Schema

A dedicated Pydantic schema will be created.

Planned file:

    src/schemas/food.py

Planned schema:

    FoodAnalysis

The schema should provide predictable structured output.

Initial conceptual fields:

    recommended_restaurants
    restaurants_by_category
    budget_assessment
    food_recommendation

Each recommended restaurant should contain structured information such as:

    name
    location
    category
    price_level
    rating
    description

The exact schema will be finalized during the implementation stage.

---

### 15. Shared State Integration

The Food Agent will read from:

    TravelState

Relevant inputs include:

    destination
    budget
    travelers
    preferences
    duration

The Food Agent will write its result to:

    state["restaurants"]

The current state contains:

    restaurants: list[dict]

This type will be updated to a dedicated `FoodAnalysis` type after the Pydantic schema is implemented.

The expected architecture will become:

    destination_data → DestinationAnalysis
    stay_options     → StayAnalysis
    activities       → ActivityAnalysis
    weather          → WeatherAnalysis
    restaurants      → FoodAnalysis

This keeps the shared state strongly typed and consistent.

---

### 16. Food Agent Tool Calling

The Food Agent will follow the same tool-calling architecture used by the Stay, Activity, and Weather Agents.

Conceptual flow:

    HumanMessage
        ↓
    Gemini
        ↓
    Tool Call
        ↓
    search_restaurants()
        ↓
    Foursquare Places API
        ↓
    Tool Result
        ↓
    Gemini
        ↓
    Structured FoodAnalysis

The conversation will contain:

    HumanMessage
    AIMessage
    ToolMessage

The ToolMessage will contain the normalized restaurant candidates returned by the Restaurant Search Tool.

Gemini will then analyze those candidates using the travel context.

---

### 17. Structured Output

The Food Agent will use Pydantic structured output through the existing LLM abstraction.

The architecture will follow:

    get_structured_llm(FoodAnalysis)

The final response will then be converted using:

    final_response.model_dump()

and stored in:

    state["restaurants"]

This provides predictable downstream data for the Itinerary Agent.

---

### 18. Why We Do Not Use the Foursquare Ask Endpoint Initially

Foursquare also provides an Ask endpoint that supports natural-language place search and contextual information.

For example, the endpoint can accept a natural-language query and additional context such as traveler preferences.

However, the initial Food Agent will use the standard Place Search endpoint instead.

Reasons:

    1. It gives us explicit control over search parameters.
    2. It exposes price filtering directly.
    3. It supports explicit sorting.
    4. It makes the tool-calling workflow easier to understand.
    5. It keeps retrieval separate from LLM reasoning.
    6. It provides a clearer learning experience for the project.

The Ask endpoint can be evaluated later as an advanced enhancement.

---

### 19. API Usage and Cost Considerations

Foursquare's current pricing changes provide 500 free Pro calls.

After the free allowance, paid usage is charged according to the applicable Places API pricing.

Because the Food Agent is being developed and tested locally, the initial implementation should keep API usage low.

Development practices should include:

    Small result limits
    Avoiding unnecessary repeated API calls
    Testing tool definitions without calling the external API
    Separating unit tests from real API integration tests

The real API integration test should only be executed when required.

---

### 20. Error Handling Requirements

The Restaurant Search Tool should handle common API failures.

Potential cases include:

    Missing API key
    Invalid API key
    Unauthorized request
    Invalid destination
    Invalid parameters
    Rate limit
    Network failure
    API server failure

The tool should use an HTTP timeout and raise meaningful errors rather than silently returning invalid data.

This will be improved further during the engineering/refactoring stage.

---

### 21. Testing Strategy

The Food Agent will follow the testing pattern already established by the other agents.

Tests should cover:

    Restaurant tool definition
    FoodAnalysis schema
    Food Agent behavior
    API response normalization
    Shared state integration
    Graph integration

The initial tests should avoid unnecessary real API calls.

A separate integration test can be used to verify the actual Foursquare API connection.

Expected development cycle:

    Implement
        ↓
    Unit Test
        ↓
    Integration Test
        ↓
    Refactor
        ↓
    Document
        ↓
    Git
        ↓
    GitHub

---

### 22. Integration into LangGraph

The Food Agent will initially be added after the Weather Agent.

Current workflow:

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

Target workflow:

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

The Food Agent will receive the accumulated `TravelState` from previous agents.

This means it can use information such as destination, budget, and preferences while generating food recommendations.

---

### 23. Relationship with the Future Itinerary Agent

The Food Agent should not create the final day-by-day itinerary.

Its responsibility is to provide structured restaurant recommendations.

The future Itinerary Agent will consume:

    Destination Analysis
    Stay Analysis
    Activity Analysis
    Weather Analysis
    Food Analysis

and combine them into a complete travel schedule.

Therefore:

    Food Agent
        ↓
    Food Recommendations
        ↓
    Itinerary Agent
        ↓
    Day-by-Day Travel Plan

This separation keeps the architecture modular.

---

### 24. Initial Implementation Decision

The initial Food Agent implementation will use:

    LLM:
        Gemini

    Framework:
        LangChain

    Orchestration:
        LangGraph

    External API:
        Foursquare Places API

    API Endpoint:
        /places/search

    Authentication:
        Bearer Service API Key

    Tool:
        search_restaurants

    Structured Output:
        Pydantic

    Shared State:
        TravelState

    Testing:
        Pytest

The implementation will initially focus on restaurant retrieval and structured recommendation generation.

More advanced functionality such as geocoding, precise coordinates, opening-hour-aware planning, restaurant details, caching, and the Foursquare Ask endpoint can be added later if they provide meaningful value.

---

### 25. Research Conclusion

The Food / Restaurant Agent will extend the AI Travel Planner with real-world restaurant discovery.

The architecture maintains the project's core design principles:

    External APIs provide real-world information.
    Tools provide controlled access to external systems.
    Gemini performs reasoning and personalization.
    Pydantic provides structured output.
    TravelState provides shared agent state.
    LangGraph orchestrates the workflow.

The Food Agent therefore becomes another specialized component in the multi-agent travel planning system rather than a generic LLM response generator.

Official References:

    Foursquare Places API Overview:
    https://docs.foursquare.com/fsq-developers-places/reference/places-api-overview

    Foursquare Place Search:
    https://docs.foursquare.com/fsq-developers-places/reference/place-search

    Foursquare Authentication:
    https://docs.foursquare.com/fsq-developers-places/reference/authentication

    Foursquare Ask:
    https://docs.foursquare.com/fsq-developers-places/reference/ask

    Foursquare Pricing / Upcoming Changes:
    https://docs.foursquare.com/developer/reference/upcoming-changes