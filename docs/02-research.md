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