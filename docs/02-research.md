# AI Travel Planner — Research

## 1. Purpose of This Research

Before implementing AI Travel Planner, we need to understand the technologies, architectural patterns, and Agentic AI concepts that will be used in the project.

The purpose of this research is to answer:

* What technologies should we use?
* Why are they suitable for this project?
* How will the technologies work together?
* Which Agentic AI concepts will we demonstrate?
* Which technologies should be introduced later instead of from the beginning?

The project is intentionally designed as an intermediate Agentic AI project, so every technology should have a practical purpose.

---

## 2. Proposed Technology Stack

The initial technology stack is:

### Frontend

* Streamlit

### Backend

* FastAPI
* Pydantic

### AI / LLM

* Google Gemini
* LangChain
* LangGraph

### Agentic AI

* AI Agents
* Multi-Agent Architecture
* Agent Orchestration
* Shared State
* Tool Calling
* Structured Output
* Conditional Workflows
* Parallel Workflows
* MCP

### External Services

* Tavily Search — Destination Research
* SerpApi Google Hotels — Accommodation Research
* SerpApi Google Maps — Activity / Attraction Research
* WeatherAPI.com — Weather Forecasts
* SerpApi Google Maps — Restaurant Research
* Other travel-related APIs where useful

### Engineering

* Python
* Pytest
* Git
* GitHub
* Docker
* GitHub Actions

### Persistence

* PostgreSQL
* LangGraph persistence/checkpointing where appropriate

---

## 3. Why Python?

Python will be the primary programming language.

Reasons:

* Strong ecosystem for AI and Machine Learning
* Excellent support for LLM applications
* Strong LangChain and LangGraph ecosystem
* Large number of API and automation libraries
* Easy integration with FastAPI
* Good testing ecosystem
* Suitable for rapid development

The project will use modern Python practices such as:

* Type hints
* Functions and classes
* Modular code
* Environment variables
* Exception handling
* Pydantic models
* Testing

---

## 4. Why Gemini?

Google Gemini will be the initial LLM provider.

Gemini will be responsible for tasks such as:

* Understanding travel requirements
* Reasoning about travel preferences
* Generating recommendations
* Summarizing external information
* Producing itinerary content
* Generating structured travel-planning information

Gemini is our initial provider because the project is being designed around Google Gemini.

However, the architecture should avoid unnecessary provider lock-in.

The project should separate:

```
Agent Logic
    |
    v
LLM Interface
    |
    v
Gemini
```

This allows the provider layer to be changed later if required.

---

## 5. Why LangChain?

LangChain provides abstractions and integrations for working with:

* Language models
* Tools
* Agents
* Structured output
* Agent workflows

For this project, LangChain will mainly help us connect the LLM with tools and create reusable AI components.

Conceptually:

```
Agent
  |
  +----> LLM
  |
  +----> Tools
  |
  +----> Structured Output
```

LangChain will therefore act as an important building block inside the Agentic AI layer.

---

## 6. Why LangGraph?

LangGraph will be one of the most important technologies in this project.

LangGraph is designed for building stateful, multi-step agent workflows and provides orchestration capabilities.

Our project needs an orchestration layer because multiple agents need to work together.

Conceptually:

```
User Request
     |
     v
LangGraph
Orchestrator
     |
+----+----+----+
|    |    |    |
v    v    v    v
```

Agent Agent Agent Agent
|    |    |    |
+----+----+----+
|
v
Final Result

LangGraph will manage:

* Nodes
* Edges
* State
* Workflow execution
* Conditional routing
* Parallel execution
* Agent coordination
* Persistence/checkpointing where required

---

## 7. LangGraph as the Orchestrator

The orchestrator is responsible for controlling the workflow.

In our project, LangGraph will determine:

* Which agent executes
* Which agents can execute independently
* What information is passed to the next agent
* When the workflow should continue
* When a different path should be taken
* When the final itinerary should be generated

The orchestrator can be thought of as the workflow manager.

```
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
```

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

```
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
```

Our agents will be specialized rather than making one large general-purpose travel agent.

---

## 9. Multi-Agent System

A multi-agent system contains multiple specialized agents that collaborate to solve a larger problem.

Our travel planning problem can be divided into:

```
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
```

Each responsibility can be handled by a specialized agent.

Example:

```
Travel Request
     |
     v
+----+----+----+----+
|    |    |    |    |
v    v    v    v    v
```

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

```
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
```

Example flow:

```
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
```

The Itinerary Agent can use the information collected in the state.

---

## 11. Nodes and Edges

LangGraph represents workflows as graphs.

A graph contains:

* Nodes
* Edges
* State

### Nodes

A node represents a unit of work.

Examples:

```
Destination Agent
Stay Agent
Activity Agent
Weather Agent
Itinerary Agent
```

### Edges

An edge defines how the workflow moves from one node to another.

Example:

```
Destination Agent
        |
        v
   Activity Agent
        |
        v
   Itinerary Agent
```

Edges can also be conditional.

---

## 12. Conditional Workflow

A conditional workflow allows the system to choose the next step based on the current state or result.

Example:

```
Weather Agent
      |
      v
Is weather suitable?
   /          \
 Yes           No
  |             |
  v             v
```

Outdoor       Indoor
Activities    Activities

Another example:

```
Budget Check
   |
+--+--+
|     |
v     v
```

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

* Hotel research
* Weather research
* Activity research
* Food research

may be performed independently.

Instead of:

```
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
```

we can design:

```
Travel Request
     |
     v
Orchestrator
     |
+----+----+----+
|    |    |    |
v    v    v    v
```

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

```
User
  |
  v
LLM
  |
  v
Answer
```

With tools:

```
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
```

Potential tools for AI Travel Planner:

* Web search
* Weather lookup
* Places search
* Restaurant search
* Location lookup

Tools will provide real-world information that should not be generated purely from the LLM.

---

## 15. External APIs

External APIs will provide real-world travel information.

Potential categories include:

### Search API

Used for:

* Destination research
* Travel information
* Recommendations
* Current information

### Weather API

Used for:

* Temperature
* Weather conditions
* Rain probability
* Forecast information

### Places / Maps API

Used for:

* Locations
* Attractions
* Restaurants
* Nearby places
* Geographic information

The exact providers will be selected during implementation based on:

* API availability
* Free-tier availability
* Reliability
* Documentation
* Ease of integration
* Project requirements

---

## 16. Structured Output

LLMs normally generate free-form text.

For an application, this can become difficult to process reliably.

Example of free-form output:

```
The hotel looks good and costs around ₹5000.
It is near the beach and has good reviews.
```

Structured output instead provides predictable fields.

Example:

```
hotel:
    name: Example Hotel
    price_per_night: 5000
    location: Near Beach
    rating: 4.3
```

Structured output is important because the result of one agent may become input for another agent.

Possible structured models:

```
DestinationResult
StayResult
ActivityResult
WeatherResult
RestaurantResult
ItineraryResult
```

Pydantic models can be used to validate these structures.

---

## 17. Pydantic

Pydantic will be used for validation and structured data models.

For example, the travel request may contain:

```
destination
duration
travelers
budget
preferences
```

Pydantic can validate whether the input has the expected structure and data types.

This will be especially useful with FastAPI.

Conceptually:

```
User Input
    |
    v
Pydantic Validation
    |
    +---- Valid ----> Continue
    |
    +---- Invalid --> Error Response
```

---

## 18. FastAPI

FastAPI will provide the backend API.

The backend will sit between the frontend and the Agentic AI workflow.

Architecture:

```
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
```

FastAPI will handle:

* HTTP requests
* Request validation
* API endpoints
* Error responses
* Calling the LangGraph workflow
* Returning structured results

---

## 19. Streamlit

Streamlit will be used for the initial frontend.

The frontend should remain simple.

Possible inputs:

```
Destination
Travel Dates
Duration
Number of Travelers
Budget
Preferences
```

Possible outputs:

```
Destination Overview
Stay Recommendations
Weather
Activities
Restaurants
Day-by-Day Itinerary
Estimated Budget
```

The main purpose of the frontend is to provide an easy way to interact with the Agentic AI system.

The project focus remains on the backend and Agentic AI architecture.

---

## 20. MCP

MCP stands for **Model Context Protocol**.

MCP provides a standardized approach for connecting AI applications with external tools and resources.

Conceptually:

```
AI Application
      |
      v
     MCP
      |
+-----+-----+-----+
|           |     |
v           v     v
```

Search     Weather  Places

MCP will be introduced after the basic tool-calling architecture is understood.

The learning order will therefore be:

```
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
```

This prevents MCP from becoming a black-box technology in the project.

---

## 21. LLM Abstraction

The application should not tightly couple all agents to Gemini-specific implementation details.

The desired architecture is:

```
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
```

The first implementation will use Gemini.

The abstraction exists so that changing the provider later does not require rewriting every agent.

---

## 22. Persistence

The project may need to persist:

* Conversation state
* Travel planning state
* User requests
* Workflow checkpoints
* Previous planning sessions

PostgreSQL is the planned persistence layer if persistence is required by the final architecture.

LangGraph also provides persistence/checkpointing capabilities that can be used for stateful workflows.

Persistence will be introduced after the basic workflow is functioning.

---

## 23. Error Handling

Agentic systems interact with external services, so failures are expected.

Potential failures include:

* API timeout
* Invalid API response
* Rate limit
* Tool failure
* LLM failure
* Invalid structured output
* Missing user input
* Network error

The system should not simply crash.

Conceptually:

```
Agent
  |
  v
Tool
  |
+--+----------------+
|                   |
```

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

* Input validation
* Budget calculations
* Data transformations
* Tool wrappers

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

```
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
```

Docker will not be introduced before the application is stable enough to containerize.

---

## 26. GitHub Actions

GitHub Actions will be used for basic CI/CD automation.

Potential workflow:

```
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
```

The initial goal is reliable automated testing rather than a complicated CI/CD pipeline.

---

## 27. Deployment

Deployment will be considered after the application is stable.

The deployment target will be selected based on:

* Cost
* Simplicity
* Python/FastAPI support
* Streamlit support
* Project requirements

Deployment is a final-stage activity and should not distract from learning the core Agentic AI architecture.

---

## 28. Technology Relationship

The technologies have different responsibilities.

```
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
```

Additional engineering:

```
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
```

---

## 29. Why We Are Not Using Everything Immediately

Although the final project may contain many technologies, they will not all be introduced on the first day.

The learning order is intentional.

### Phase 1

Understand:

```
LLM
Agent
Tool
LangChain
LangGraph
State
```

### Phase 2

Build:

```
Single Agent
    |
    v
Tool Calling
    |
    v
External API
```

### Phase 3

Expand:

```
Multiple Agents
    |
    v
Shared State
    |
    v
LangGraph Orchestration
```

### Phase 4

Improve:

```
Structured Output
Conditional Workflow
Parallel Workflow
Error Handling
```

### Phase 5

Add advanced capabilities:

```
MCP
LLM Abstraction
Persistence
```

### Phase 6

Production engineering:

```
Testing
Docker
GitHub Actions
Deployment
```

This sequence allows each concept to be understood before it becomes part of the implementation.

---

## 30. Reference Architecture

The current target architecture is:

```
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
```

External capabilities:

```
Agents
  |
  +--> Web Search
  +--> Weather API
  +--> Places / Maps API
  +--> MCP Tools
  |
  v
Real-World Information
```

LLM layer:

```
Agents
  |
  v
LLM Interface
  |
  v
Gemini
```

Future provider support:

```
LLM Interface
  |
  +--> Gemini
  +--> OpenAI
  +--> Anthropic
```

---

## 31. Research Conclusions

The research indicates that the selected technologies fit the requirements of AI Travel Planner.

### LangGraph

Best suited for:

* Workflow orchestration
* Stateful workflows
* Multi-step agent execution
* Conditional routing
* Parallel workflow design
* Persistence capabilities

### LangChain

Best suited for:

* Model integration
* Tool integration
* Agent abstractions
* Structured output
* LLM application components

### Gemini

Best suited as:

* Initial LLM provider
* Reasoning and generation layer
* Travel recommendation generation

### FastAPI

Best suited for:

* Backend API
* Request validation
* Integration between frontend and Agentic workflow

### Streamlit

Best suited for:

* Rapid frontend development
* Simple user interaction
* Displaying travel-planning results

### Pydantic

Best suited for:

* Input validation
* Structured data
* Agent output schemas

### MCP

Best suited as:

* Advanced standardized tool/resource integration
* A later-stage Agentic AI feature

### PostgreSQL

Best suited for:

* Persistence
* Conversation/workflow data
* Future application state

### Docker

Best suited for:

* Reproducible environments
* Application packaging

### GitHub Actions

Best suited for:

* Automated testing
* CI/CD

---

## 32. Research Sources

The primary research sources for this document are official documentation from:

* LangGraph Documentation
* LangChain Documentation
* Google Gemini / Google AI Documentation
* Model Context Protocol Documentation
* FastAPI Documentation
* Pydantic Documentation
* Streamlit Documentation
* PostgreSQL Documentation
* Docker Documentation
* GitHub Actions Documentation

Official documentation should be preferred over tutorials or third-party explanations when making implementation decisions.

---

## 33. Research Decision

Based on the research, the project will proceed with:

```
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
```

The technologies will be introduced progressively according to the project's development workflow.

The project will prioritize understanding and implementation over adding unnecessary technologies.

## Structured Output

### What is Structured Output?

Structured output allows an LLM to return information according to a predefined schema instead of returning only free-form text.

Without structured output:

```
Gemini
   ↓
Free-form text
   ↓
Application must interpret the text
```

With structured output:

```
Gemini
   ↓
Predefined schema
   ↓
Structured data
   ↓
Application can consume predictable fields
```

For the AI Travel Planner, structured output is important because multiple agents will exchange information through the shared `TravelState`.

---

### Why Structured Output is Important for AI Travel Planner

The current Destination Agent stores the Gemini response as:

```
destination_data = {
    "analysis": response.content
}
```

This works for basic experimentation, but it is not ideal for a multi-agent system.

Future agents should be able to consume specific information without parsing an arbitrary paragraph.

For example:

```
destination_data
    ├── overview
    ├── recommended_areas
    ├── travel_considerations
    └── preference_suggestions
```

This makes communication between agents more predictable and easier to validate.

---

### Structured Output vs Free-Form Output

| Aspect                       | Free-Form Output   | Structured Output    |
| ---------------------------- | ------------------ | -------------------- |
| Response format              | Unpredictable text | Predefined structure |
| Application parsing          | More difficult     | Easier               |
| Validation                   | Limited            | Schema-based         |
| Agent-to-agent communication | Less reliable      | More predictable     |
| Data extraction              | Requires parsing   | Direct field access  |
| Maintainability              | Lower              | Higher               |

---

## Pydantic

### What is Pydantic?

Pydantic is a Python library used to define and validate structured data using Python type annotations.

For our project, Pydantic will be used to define the expected structure of agent responses.

Example conceptual model:

```
class DestinationAnalysis(BaseModel):
    overview: str
    recommended_areas: list[str]
    travel_considerations: list[str]
    preference_suggestions: list[str]
```

This model defines exactly what information the Destination Agent should produce.

---

### Why Pydantic?

Pydantic provides:

* Explicit data models
* Python type hints
* Runtime validation
* Predictable data structures
* Easier integration with structured LLM output
* Better maintainability

This is especially useful when multiple agents exchange data through a shared state.

---

## Planned DestinationAnalysis Schema

The first structured response model will be:

```
DestinationAnalysis
├── overview: str
├── recommended_areas: list[str]
├── travel_considerations: list[str]
└── preference_suggestions: list[str]
```

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

```
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
```

This maintains separation between:

* Agent logic
* LLM configuration
* Response schema

---

## Gemini Structured Output

Gemini supports structured output using a defined response schema.

For this project, the schema will be represented using a Pydantic model and connected to the LangChain Gemini model.

The intended implementation direction is:

```
Pydantic Model
      ↓
Structured Output Configuration
      ↓
Gemini 3.5 Flash-Lite
      ↓
Structured Response
      ↓
Pydantic Validation
```

---

## Structured Output Validation

Structured output does not automatically guarantee that the generated information is factually correct.

Two different concerns must be considered:

### Schema Validation

Does the response follow the expected structure?

Example:

```
overview → string
recommended_areas → list of strings
```

### Semantic Correctness

Is the information actually useful and accurate?

For example, a response can follow the correct schema but still contain an incorrect recommendation.

Therefore, structured output solves the **format and validation problem**, but it does not by itself solve the **factual accuracy problem**.

External tools and APIs will later be introduced to provide real travel information.

---

## Structured Output in the Multi-Agent Architecture

The structured Destination Agent will eventually provide information that other agents can consume.

```
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
```

This creates a predictable data flow between specialized agents.

---

## Implementation Decision

For the first structured-output implementation:

* Use Pydantic models
* Use LangChain structured output capabilities
* Continue using Gemini 3.5 Flash-Lite
* Keep the existing LLM service abstraction
* Keep the Destination Agent as the first consumer
* Store structured destination information in `TravelState`

The implementation will remain intentionally small before adding external tools or additional agents.

---

## Research Conclusion

Structured output is an important transition point for the AI Travel Planner.

The project will move from:

```
LLM
  ↓
Free-form text
  ↓
destination_data["analysis"]
```

to:

```
LLM
  ↓
Structured Output
  ↓
Pydantic Model
  ↓
destination_data
```

This provides a stronger foundation for reliable multi-agent communication and future tool integration.

## Stay / Hotel Agent Research

The Stay Agent is responsible for researching and evaluating accommodation options based on the traveler's requirements.

The agent considers:

* destination
* travel dates
* duration
* number of travelers
* budget
* traveler preferences

The goal is to provide practical accommodation recommendations while keeping the agent focused on the accommodation domain.

### Why a Separate Stay Agent?

The Destination Agent is responsible for understanding the destination, while the Stay Agent focuses specifically on accommodation.

Separating these responsibilities follows the multi-agent design principle of giving each agent a focused task.

```
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
```

This separation improves:

* responsibility isolation
* maintainability
* testing
* scalability
* agent-to-agent communication

### Stay Agent and Tool Calling

The Stay Agent combines tool calling with structured output.

Structured output and tool calling solve different problems.

#### Structured Output

Structured output controls the format of the final model response.

```
Gemini
   |
   v
Pydantic Schema
   |
   v
Structured Result
```

The Stay Agent uses the `StayAnalysis` Pydantic model to produce predictable accommodation recommendations.

#### Tool Calling

Tool calling allows Gemini to request external accommodation information.

```
Stay Agent
     |
     v
  Gemini
     |
     v
 Tool Call
     |
     v
Accommodation Tool
     |
     v
   SerpApi
     |
     v
Google Hotels
     |
     v
 Hotel Results
     |
     v
  Gemini
     |
     v
StayAnalysis
```

The application executes the requested tool and provides the tool result back to Gemini.

### Difference Between Structured Output and Tool Calling

| Concept           | Purpose                                           |
| ----------------- | ------------------------------------------------- |
| Structured Output | Controls the format of model output               |
| Tool Calling      | Allows the model to request an external function  |
| Pydantic          | Defines and validates structured data             |
| External API      | Provides real-world accommodation information     |
| LangChain         | Connects the LLM with tools and structured output |
| LangGraph         | Orchestrates the overall travel-planning workflow |

Both structured output and tool calling are used together in the Stay Agent.

### Accommodation Search Tool

The accommodation search tool is implemented in:

```
src/tools/accommodation.py
```

The tool provides a stable application-level interface:

```
search_accommodations(
    destination,
    travel_dates,
    duration,
    travelers,
    budget,
    preferences
)
```

The tool is responsible for retrieving accommodation candidates from an external hotel data provider.

### Selected Provider: SerpApi Google Hotels

After evaluating accommodation API availability, access requirements, and project complexity, the project uses **SerpApi Google Hotels**.

The existing `SERPAPI_API_KEY` used by the Food Agent can also be reused for the Stay Agent.

This avoids introducing another API provider and keeps the project simpler.

The integration uses the SerpApi search endpoint with the `google_hotels` engine.

The request includes:

* destination query
* check-in date
* check-out date
* number of adults
* currency
* country
* language
* sorting preference

Conceptually:

```
Stay Agent
     |
     v
Accommodation Tool
     |
     v
   SerpApi
     |
     v
Google Hotels
     |
     v
Hotel Candidates
```

### Why SerpApi Google Hotels?

SerpApi Google Hotels was selected because it provides:

* real hotel search results
* hotel names
* accommodation addresses
* nightly pricing information
* ratings
* descriptions
* date-aware hotel searches
* traveler/occupancy information
* a reusable API key already used elsewhere in the project

The API returns structured Google Hotels property data that can be normalized by the application.

### Provider Independence

The Stay Agent remains provider-independent at the agent layer.

The agent interacts with:

```
search_accommodations()
```

rather than directly depending on SerpApi.

The underlying implementation can therefore be replaced later with:

* another hotel API
* a web search provider
* an MCP-based tool
* another suitable accommodation data source

This keeps provider-specific logic inside the tool layer.

### Accommodation Data Normalization

External API responses should not be passed directly into the application's internal schema.

The accommodation tool normalizes the external Google Hotels response into a consistent structure:

```
Accommodation
├── name
├── area
├── price_per_night
├── rating
└── description
```

This creates a stable contract between the external API and the Stay Agent.

Conceptually:

```
Google Hotels Response
         |
         v
Accommodation Tool
         |
         v
   Normalized Data
         |
         v
     Gemini
         |
         v
   StayAnalysis
```

### StayAnalysis Schema

The Stay Agent uses structured output similar to the Destination Agent.

The schema is:

```
StayAnalysis
├── recommended_area
├── accommodation_options
├── budget_assessment
└── stay_recommendation
```

Each accommodation option contains:

```
Accommodation
├── name
├── area
├── price_per_night
├── rating
└── description
```

Pydantic validates the final structure.

### Stay Agent Flow

The implemented architecture is:

```
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
Accommodation Tool
        |
        v
     SerpApi
        |
        v
  Google Hotels
        |
        v
 Hotel Candidates
        |
        v
    Gemini LLM
        |
        v
 StayAnalysis
        |
        v
   TravelState
```

The Stay Agent therefore combines:

* LLM reasoning
* tool calling
* external API integration
* response normalization
* structured output
* shared graph state

### Research Decision

The final Stay Agent design is:

```
Stay Agent
     |
     +── Gemini
     |
     +── Accommodation Search Tool
                 |
                 v
              SerpApi
                 |
                 v
          Google Hotels
     |
     +── Pydantic Structured Output
     |
     v
  TravelState
```

SerpApi is currently used for both:

```
Food Agent
     |
     v
  SerpApi
     |
     v
 Google Maps
```

and:

```
Stay Agent
     |
     v
  SerpApi
     |
     v
Google Hotels
```

This provides a practical and reusable external API integration layer.

MCP will be introduced later as part of the advanced Agentic AI architecture rather than being forced into the initial Stay Agent implementation.

### Research Conclusion

The Stay Agent extends the AI Travel Planner from destination analysis into real external-data-driven accommodation research.

The architectural progression is:

```
Destination Agent
     |
     v
   Gemini
     |
     v
Structured Output
     |
     v
DestinationAnalysis

Stay Agent
     |
     v
   Gemini
     |
     v
Tool Calling
     |
     v
SerpApi Google Hotels
     |
     v
Normalized Hotel Data
     |
     v
Structured Output
     |
     v
StayAnalysis
```

This establishes a reusable pattern for the Activity, Weather, Food, and future Itinerary agents while keeping each component focused and independently testable.

### Research Sources

* SerpApi Google Hotels API documentation
* Gemini Function Calling documentation — Google AI
* Gemini Tools documentation — Google AI
* Gemini Structured Output documentation — Google AI
* LangChain tool calling documentation
* LangGraph documentation

## Weather Agent Research

### 1. Purpose

The Weather Agent is responsible for retrieving and interpreting weather information relevant to a travel plan.

Weather is different from destination, accommodation, and activity research because it is **time-sensitive external information**.

The Weather Agent should therefore not rely on the LLM's internal knowledge to provide current or forecast weather information.

The architecture should be:

```
Weather API
    ↓
Weather Tool
    ↓
Weather Agent / LLM
    ↓
Structured Weather Analysis
    ↓
TravelState
```

The Weather API provides factual weather data, while the LLM interprets that information in the context of the traveler's trip.

---

### 2. Why a Separate Weather Agent?

Weather affects several travel-planning decisions:

* Whether outdoor activities are suitable
* Whether beach activities should be recommended
* Whether alternative indoor activities are needed
* Whether rain may affect the itinerary
* Whether particular travel days require flexibility
* Whether weather conditions are generally suitable for the planned trip

A dedicated Weather Agent keeps this responsibility separate from other agents.

This follows the multi-agent design principle used throughout the project:

```
One agent = one specialized responsibility
```

The Weather Agent focuses specifically on weather analysis and travel-related weather recommendations.

---

### 3. Weather Data Source

Several weather APIs were considered:

* WeatherAPI.com
* Open-Meteo
* OpenWeatherMap

For the initial implementation, **WeatherAPI.com** is selected.

Reasons:

* Simple REST API
* Supports city-name input
* Provides current weather information
* Provides forecast information
* Provides daily and hourly forecast data
* Supports forecasts for multiple days
* Returns structured JSON data
* Easy to integrate with a Python tool

The API can therefore act as the factual data source for the Weather Tool.

---

### 4. Weather Tool

The Weather Agent should use a dedicated LangChain tool to retrieve weather information.

Conceptually:

```
search_weather(
    destination,
    travel_dates,
    duration
)
```

The tool will:

1. Receive the destination and travel requirements.
2. Call the weather API.
3. Extract relevant weather information.
4. Return useful weather data to the Weather Agent.

The tool should avoid returning unnecessary API fields.

Relevant information may include:

* Date
* Temperature
* Feels-like temperature
* Weather condition
* Rain probability
* Precipitation
* Wind

The Weather Tool is responsible for **retrieving factual information**, not making the final travel recommendation.

---

### 5. API Data vs LLM Interpretation

An important architectural principle is:

```
API = factual information
LLM = interpretation
```

The application should not ask the LLM to directly predict weather.

Incorrect approach:

```
User
  ↓
Gemini
  ↓
"What will the weather be in Goa?"
```

This could result in outdated or hallucinated information.

Instead:

```
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
```

For example:

```
Weather API

Day 1 → 29°C, Sunny, 10% rain
Day 2 → 28°C, Cloudy, 35% rain
Day 3 → 26°C, Heavy Rain, 80% rain
```

The LLM can then interpret the information:

```
Day 1 → Good for outdoor activities
Day 2 → Suitable with some flexibility
Day 3 → Prefer indoor activities
```

This separation improves reliability because the LLM does not generate the underlying weather facts.

---

### 6. Weather Analysis

The Weather Agent should transform raw weather information into a structured travel-oriented analysis.

A possible structure is:

```
WeatherAnalysis

    forecast_summary
    temperature_summary
    precipitation_summary
    travel_assessment
    weather_recommendation
```

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

* Suitable days for outdoor activities
* Days requiring flexibility
* Possible indoor alternatives
* General weather-related travel advice

---

### 7. Structured Output

The Weather Agent should use Pydantic structured output, consistent with the other agents.

Conceptually:

```
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
```

Structured output provides a predictable format for the rest of the LangGraph workflow.

This is important because the Itinerary Agent will eventually consume information from multiple agents, including weather information.

---

### 8. Weather Information in Shared State

The existing TravelState already contains a weather field:

```
weather: dict
```

The Weather Agent will populate this field after processing the weather information.

Conceptually:

```
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
```

This allows later agents, especially the Itinerary Agent, to use weather information when constructing the final itinerary.

---

### 9. Forecast Limitations

Weather forecasts are time-dependent and become less certain further into the future.

Therefore, the system should not present long-range forecasts as guaranteed facts.

The Weather Agent should work with whatever forecast information is available from the selected weather API.

The application should also distinguish between:

* Available forecast information
* Travel interpretation based on that information

Forecast uncertainty can be improved later, but it is not necessary to over-engineer the first implementation.

---

### 10. LangGraph Integration

The Weather Agent will be added as another node in the existing LangGraph workflow.

Current workflow:

```
START
  ↓
Destination Agent
  ↓
Stay Agent
  ↓
Activity Agent
  ↓
END
```

After adding the Weather Agent:

```
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
```

The Weather Agent receives the shared TravelState, retrieves weather information, generates structured analysis, stores the result in the state, and passes the updated state to the next node.

---

### 11. Weather Agent Workflow

The complete Weather Agent workflow is:

```
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
```

This follows the same architecture already established for the Stay and Activity Agents:

```
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
```

---

### 12. Initial Implementation Decision

For the first implementation:

* WeatherAPI.com will be used as the weather data source.
* A LangChain `search_weather` tool will retrieve weather data.
* The Weather Agent will interpret the retrieved information.
* Pydantic will define the structured WeatherAnalysis output.
* Weather information will be stored in TravelState.
* The Weather Agent will be integrated into the existing sequential LangGraph workflow.

The implementation will initially remain simple.

Future improvements may include:

* More weather APIs
* Better location resolution
* Weather alerts
* More detailed hourly analysis
* Weather-based itinerary adjustments
* MCP-based weather tools
* More advanced conditional workflows

These features will be considered later as the project evolves.

---

### 13. Research Conclusion

The Weather Agent introduces an important capability to the AI Travel Planner: **using external, time-sensitive information and allowing the LLM to interpret that information instead of generating factual data itself.**

The selected architecture is:

```
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
```

This design keeps responsibilities separated, improves reliability, and prepares the system for future itinerary optimization based on real-world weather conditions.

### Sources

* WeatherAPI.com Documentation
* Open-Meteo Documentation
* OpenWeatherMap API Documentation
* LangChain Tools Documentation
* LangChain Structured Output Documentation
* LangGraph Documentation

## Food / Restaurant Agent Research

### 1. Purpose

The Food / Restaurant Agent is responsible for finding suitable restaurants and food experiences for the travel destination.

The agent considers:

- Destination
- Traveler preferences
- Food interests
- Restaurant category
- Ratings
- Location
- Relative price level

The Food Agent should not generate restaurant information purely from the LLM's internal knowledge.

Instead, it retrieves real place data from an external Maps API and then uses the LLM to analyze and personalize those results.

The overall architecture is:

    TravelState
        ↓
    Food Agent
        ↓
    Gemini Tool Calling
        ↓
    Restaurant Search Tool
        ↓
    SerpApi Google Maps
        ↓
    Restaurant Data
        ↓
    Gemini Structured Output
        ↓
    FoodAnalysis
        ↓
    TravelState["restaurants"]

### 2. Why a Separate Food Agent?

Food recommendations are an important part of travel planning.

However, restaurant discovery has different requirements from:

- Destination research
- Accommodation search
- Activity research
- Weather analysis

A dedicated Food Agent allows the system to:

- Search restaurants using real location data
- Consider restaurant categories
- Consider traveler preferences
- Use ratings and relative price information
- Rank suitable options
- Generate practical food recommendations

Separating this responsibility also keeps the multi-agent architecture modular.

### 3. Selected External API

The project uses **SerpApi Google Maps** for restaurant discovery.

The project already uses SerpApi for accommodation research through Google Hotels. Reusing the same provider keeps the architecture simpler and avoids introducing another API key and provider-specific integration.

The Google Maps search endpoint is:

    https://serpapi.com/search.json

with:

    engine = google_maps

The API supports Google Maps-style local searches and returns structured local results.

### 4. Why SerpApi Google Maps?

SerpApi Google Maps is suitable for the Food Agent because it can search for restaurants in a destination and return useful place information.

Relevant result fields may include:

- Name/title
- Address
- Type/category
- Rating
- Description
- Distance
- Links and other place information when available

The Food Agent can therefore retrieve real restaurant candidates before Gemini performs the final reasoning and recommendation.

The main advantages for this project are:

1. Existing `SERPAPI_API_KEY`
2. Already used successfully by the Stay Agent
3. Restaurant and local-place search support
4. Structured JSON responses
5. Simple REST integration
6. No additional external provider required

### 5. Restaurant Search Tool

The restaurant search tool is implemented in:

    src/tools/food.py

The application-level interface is:

    search_restaurants(
        destination,
        price_level,
        limit
    )

The tool is responsible for:

1. Loading the SerpApi API key.
2. Validating that the API key exists.
3. Building the Google Maps search request.
4. Searching for restaurants in the destination.
5. Limiting the number of returned results.
6. Validating the HTTP response.
7. Parsing the JSON response.
8. Normalizing restaurant information.
9. Returning restaurant candidates to the Food Agent.

### 6. Search Request

The current implementation uses:

    url = "https://serpapi.com/search.json"

with parameters equivalent to:

    engine = google_maps
    q = restaurants in {destination}
    type = search
    limit = requested result count
    api_key = SERPAPI_API_KEY

The destination is therefore used as the primary search context.

### 7. Restaurant Data Normalization

External API responses should not be passed directly into the application's internal schema.

The tool normalizes Google Maps results into a consistent structure:

    Restaurant
    ├── name
    ├── location
    ├── category
    ├── price_level
    ├── rating
    ├── distance
    └── description

The current implementation maps:

    title       → name
    address     → location
    type        → category
    rating      → rating
    distance    → distance
    description → description

The current `price_level` is supplied by the tool interface rather than being treated as an exact monetary amount.

### 8. Price Level

The Food Agent uses a relative price-level input.

This should not be interpreted as an exact meal cost in Indian rupees.

The application therefore treats price level as an affordability signal rather than a guaranteed monetary price.

This distinction is important because local search results do not guarantee standardized exact meal pricing for every restaurant.

### 9. API Data vs LLM Responsibilities

The system separates factual restaurant retrieval from AI reasoning.

#### SerpApi Google Maps

Responsible for:

    Restaurant discovery
    Location information
    Categories
    Ratings
    Distance
    Descriptions when available
    Other place metadata when available

#### Gemini

Responsible for:

    Understanding traveler preferences
    Comparing restaurant candidates
    Categorizing recommendations
    Ranking suitable restaurants
    Explaining recommendations
    Producing personalized food recommendations

The external API provides real-world place data.

The LLM provides reasoning and personalization.

### 10. Food Analysis Schema

The Food Agent uses a Pydantic structured-output model.

The schema contains:

    FoodAnalysis
    ├── recommended_restaurants
    ├── restaurants_by_category
    ├── budget_assessment
    └── food_recommendation

Each restaurant contains:

    Restaurant
    ├── name
    ├── location
    ├── category
    ├── price_level
    ├── rating
    ├── distance
    └── description

This provides predictable output for the shared TravelState.

### 11. Shared State Integration

The Food Agent stores its result in:

    TravelState["restaurants"]

Conceptually:

    TravelState
        |
        +── destination_data
        +── stay_options
        +── activities
        +── weather
        +── restaurants
        +── itinerary

The future Itinerary Agent can consume restaurant information together with the other research outputs.

### 12. Food Agent Tool Calling

The Food Agent follows the established project tool-calling pattern:

    Food Agent
        ↓
    Gemini
        ↓
    Tool Call
        ↓
    search_restaurants
        ↓
    SerpApi Google Maps
        ↓
    Restaurant Results
        ↓
    Gemini
        ↓
    FoodAnalysis
        ↓
    TravelState

This keeps the Food Agent consistent with the Destination, Stay, Activity, and Weather agents.

### 13. Structured Output

Structured output is used after the external restaurant search.

The flow is:

    Restaurant Search Tool
        ↓
    Real Restaurant Data
        ↓
    Gemini
        ↓
    FoodAnalysis
        ↓
    TravelState

Pydantic validates the final structure.

Structured output solves the response-format problem, while the external API provides factual restaurant information.

### 14. Provider Independence

The Food Agent interacts with the application-level tool:

    search_restaurants()

rather than directly depending on SerpApi inside the agent.

The provider-specific implementation remains inside:

    src/tools/food.py

This allows the underlying provider to be replaced later with:

- Another Maps/Places API
- Another search provider
- An MCP-based tool
- Another suitable restaurant data source

without redesigning the Food Agent itself.

### 15. Error Handling Requirements

The tool should handle failures such as:

- Missing `SERPAPI_API_KEY`
- HTTP errors
- API failures
- Network timeouts
- Empty search results
- Unexpected response structures

The current implementation uses HTTP status validation and a request timeout.

More advanced retry and fallback behavior can be introduced later as part of the project's global error-handling and productionization pass.

### 16. Testing Strategy

The Food Agent is tested at multiple levels.

#### Tool Test

The restaurant tool is tested with a real SerpApi request and verifies that results contain the expected normalized fields.

Expected fields include:

    name
    location
    category
    price_level
    rating
    distance
    description

#### Agent Test

The Food Agent is tested to verify that real tool results can be converted into the `FoodAnalysis` structure.

#### Workflow Test

The Food Agent is integrated into the LangGraph workflow and tested as part of the broader graph.

### 17. Integration into LangGraph

The Food Agent is currently integrated after the research agents.

The current sequential implementation is:

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

This is the current implementation state.

Later, the graph will be refactored into the planned hybrid workflow where Stay, Activity, and Weather can execute in parallel and Food can execute after the required research is available.

### 18. Relationship with the Future Itinerary Agent

The Food Agent does not generate the final itinerary.

Its responsibility ends after producing structured restaurant recommendations.

The future Itinerary Agent will combine:

    DestinationAnalysis
    StayAnalysis
    ActivityAnalysis
    WeatherAnalysis
    FoodAnalysis

and generate a day-by-day travel plan.

This keeps the Food Agent focused and prevents it from becoming a general-purpose travel planner.

### 19. Current Implementation Decision

The final Food Agent design is:

    Food Agent
        |
        +── Gemini
        |
        +── Restaurant Search Tool
                    |
                    v
                SerpApi
                    |
                    v
              Google Maps
        |
        +── Pydantic Structured Output
        |
        v
    TravelState

The same SerpApi provider is reused by:

    Stay Agent
        ↓
    SerpApi Google Hotels

and:

    Food Agent
        ↓
    SerpApi Google Maps

and now also:

    Activity Agent
        ↓
    SerpApi Google Maps

This provides a practical and reusable external-data integration layer.

### 20. Research Conclusion

The Food Agent adds real restaurant discovery to the AI Travel Planner while maintaining the project's specialized multi-agent architecture.

The architectural pattern is:

    Agent
      ↓
    Tool
      ↓
    External API
      ↓
    Normalized Data
      ↓
    LLM Interpretation
      ↓
    Structured Output
      ↓
    Shared State

This pattern can be reused for the remaining agents and future itinerary workflow.

### Sources

- SerpApi Google Maps API documentation
- LangChain Tools documentation
- LangChain Structured Output documentation
- LangGraph documentation



## Activity Agent Research

### 1. Purpose

The Activity Agent is responsible for finding relevant activities, attractions, and experiences for a travel destination.

The agent considers:

- Destination
- Traveler preferences
- Activity relevance
- Location
- Available descriptions
- Available ratings and other place information

The initial Activity Agent used mock data. A real external data source was therefore required.

The goal is to retrieve real activity and attraction candidates and then allow Gemini to organize and personalize them.

### 2. Why a Separate Activity Agent?

Activity planning is a distinct travel-planning responsibility.

The Activity Agent focuses on:

- Attractions
- Beaches
- Adventure activities
- Tourist experiences
- Sightseeing locations
- Preference-based activity recommendations

This keeps activity research separate from:

- Destination research
- Accommodation research
- Weather analysis
- Restaurant discovery
- Final itinerary generation

The separation follows the project's multi-agent principle:

    One agent = one specialized responsibility

### 3. API Evaluation

Amadeus was initially considered because it provides travel-related activity and experience capabilities.

However, the Amadeus for Developers self-service portal has been decommissioned, so it was not suitable for creating a new integration for this project.

The project therefore uses an existing provider already required elsewhere in the system.

### 4. Selected External API

The selected provider is:

**SerpApi — Google Maps API**

The same API provider is already used by the Stay and Food agents.

The Activity Agent uses Google Maps-style local search to find activities, attractions, and experiences.

The request is made through:

    https://serpapi.com/search.json

with:

    engine = google_maps

### 5. Why SerpApi Google Maps?

SerpApi Google Maps was selected because it:

1. Already works in the project
2. Uses the existing `SERPAPI_API_KEY`
3. Supports destination-based local searches
4. Can return tourist attractions and activity-related places
5. Provides structured local result data
6. Avoids adding another external API provider
7. Keeps the Activity Agent implementation consistent with the Food Agent

This is especially useful for an intermediate project where unnecessary provider complexity should be avoided.

### 6. Activity Search Tool

The activity search tool is implemented in:

    src/tools/activity.py

The application-level interface is:

    search_activities(
        destination,
        preferences,
        limit
    )

The tool:

1. Loads the SerpApi API key.
2. Validates the API key.
3. Builds an activity-focused Google Maps query.
4. Sends the request to SerpApi.
5. Validates the HTTP response.
6. Parses the JSON response.
7. Normalizes the local results.
8. Returns activity candidates to the Activity Agent.

### 7. Search Query

The current implementation constructs a query similar to:

    things to do, activities, attractions, and experiences in {destination}

When preferences are provided, they are incorporated into the query.

Example:

    things to do, activities, attractions, and experiences in Goa, India for beaches, adventure, food

The request uses parameters equivalent to:

    engine = google_maps
    q = activity search query
    type = search
    limit = requested result count
    hl = en
    gl = in

### 8. Activity Data Normalization

The raw Google Maps response is normalized into the application's Activity structure.

The current structure is:

    Activity
    ├── name
    ├── location
    ├── category
    ├── estimated_cost
    ├── duration
    └── description

The tool maps available search-result fields into this structure.

Conceptually:

    Google Maps Result
        |
        +── title       → name
        +── address     → location
        +── type        → category
        +── description → description

Price and duration require special handling.

### 9. Price and Duration Availability

Google Maps local search results do not guarantee standardized activity pricing or duration for every result.

Therefore, the application does not invent missing values.

When price information is unavailable:

    estimated_cost = 0.0

When duration information is unavailable:

    duration = "Not available"

These values indicate that the source did not provide standardized information.

This is preferable to allowing the LLM to fabricate factual activity costs or durations.

### 10. API Data vs LLM Responsibilities

The external API and Gemini have different responsibilities.

#### SerpApi Google Maps

Responsible for retrieving real-world activity candidates and available place information.

#### Gemini

Responsible for:

- Understanding traveler preferences
- Categorizing activities
- Ranking suitable candidates
- Summarizing retrieved information
- Producing the structured `ActivityAnalysis`
- Explaining recommendations

The architectural principle is:

    External API = factual source
    LLM = reasoning and personalization

### 11. Activity Analysis Schema

The Activity Agent uses:

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

Pydantic validates the structured response.

### 12. Tool Calling

The Activity Agent follows the same tool-calling pattern used by the other research agents:

    Activity Agent
        ↓
    Gemini
        ↓
    Tool Call
        ↓
    search_activities
        ↓
    SerpApi Google Maps
        ↓
    Activity Results
        ↓
    Gemini
        ↓
    ActivityAnalysis
        ↓
    TravelState

This provides a consistent architecture across the project.

### 13. Grounding Considerations

The Activity Agent prompt explicitly instructs the model to use the retrieved tool results and not invent factual fields.

The model may:

- Categorize retrieved activities
- Rank them according to preferences
- Summarize retrieved descriptions
- Assess the available activity information

The model should not invent:

- New activities
- Prices
- Durations
- Ratings
- Other factual information not supported by the retrieved results

A stricter grounding mechanism will be considered during the later global tool-calling/refactoring pass.

### 14. Provider Independence

The Activity Agent interacts with:

    search_activities()

rather than directly depending on SerpApi.

The provider-specific implementation remains inside:

    src/tools/activity.py

This means the underlying activity data provider can later be replaced without redesigning the agent.

Possible future replacements include:

- Another Places/Maps API
- A dedicated experiences API
- An MCP-based activity tool
- Another travel data provider

### 15. Testing Strategy

The Activity tool has been tested with a real SerpApi request.

Example destination:

    Goa, India

Example preferences:

    beaches
    adventure
    food

The real search returned activity/attraction candidates such as:

- Butterfly Beach Goa
- Velsao Beach
- Thunder World Goa
- Goosebumps Virtual Escape
- Boat-trip-related attractions

The Activity Agent was also tested with a real tool call and successfully produced a structured `ActivityAnalysis`.

The complete existing test suite currently passes:

    12 passed

The remaining warning is a dependency deprecation warning from the Google GenAI package under Python 3.14 and is not caused by the Activity API integration.

### 16. LangGraph Integration

The Activity Agent is currently a node in the sequential graph.

Current implementation:

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

Later, the graph will be changed to the planned hybrid workflow.

In the final architecture, Activity will execute in parallel with Stay and Weather after Destination research:

    Destination Agent
          |
          +--------+--------+
          |        |        |
          v        v        v
        Stay   Activity  Weather
          |        |        |
          +--------+--------+
                   |
                   v
               Food Agent

### 17. Relationship with Itinerary Agent

The Activity Agent does not generate the final itinerary.

It provides structured activity information to the shared TravelState.

The future Itinerary Agent will combine:

    DestinationAnalysis
    StayAnalysis
    ActivityAnalysis
    WeatherAnalysis
    FoodAnalysis

to generate a day-by-day plan.

This keeps activity discovery separate from itinerary reasoning.

### 18. Current Implementation Decision

The final Activity Agent design is:

    Activity Agent
        |
        +── Gemini
        |
        +── Activity Search Tool
                    |
                    v
                SerpApi
                    |
                    v
              Google Maps
        |
        +── Pydantic Structured Output
        |
        v
    TravelState

SerpApi is therefore reused across three different travel domains:

    Stay Agent
        ↓
    Google Hotels

    Activity Agent
        ↓
    Google Maps

    Food Agent
        ↓
    Google Maps

This keeps the external integration layer simple while still demonstrating multiple real-world data sources.

### 19. Research Conclusion

The Activity Agent replaces the initial mock activity data with a real external search capability.

The resulting architecture is:

    Travel Request
        ↓
    Activity Agent
        ↓
    SerpApi Google Maps
        ↓
    Real Activity Candidates
        ↓
    Gemini
        ↓
    Structured ActivityAnalysis
        ↓
    TravelState

This establishes the Activity Agent as a real tool-using component rather than a mock component.

### Sources

- SerpApi Google Maps API documentation
- LangChain Tools documentation
- LangChain Structured Output documentation
- LangGraph documentation



## Destination Research Agent — Tavily Search Research
```

### Purpose

The Destination Research Agent is responsible for researching the requested destination and providing useful, current, and preference-aware information to the rest of the travel-planning workflow.

The initial Destination Agent was implemented using the LLM alone. However, relying only on the LLM's internal knowledge is not sufficient for a travel application because destination information can change over time.

Therefore, the Destination Agent will use an external web-search capability.

### Selected Research Provider

The selected provider for destination research is **Tavily**.

Tavily is designed as a web access and search layer for AI applications and agents. It provides search results in a form that can be consumed and analyzed by an LLM.

Official documentation:

* Tavily Search API: https://docs.tavily.com/documentation/api-reference/search
* Tavily documentation: https://docs.tavily.com/

### Why Tavily

Tavily is a suitable choice for the Destination Research Agent because destination research requires broad web information rather than a single specialized dataset.

The agent may need information about:

* Destination overview
* Recommended areas
* Major attractions
* Travel considerations
* Local experiences
* Preference-specific recommendations
* Current or recently published travel information

A web-search-based solution is therefore more appropriate than a narrow destination database API.

### Destination Research Architecture

The planned architecture is:

```
Destination Agent
        |
        v
Tavily Search Tool
        |
        v
   Web Search
        |
        v
  Search Results
        |
        v
      Gemini
        |
        v
DestinationAnalysis
        |
        v
   TravelState
```

The Destination Agent remains responsible for reasoning and analysis, while Tavily is responsible for retrieving relevant web information.

### Separation of Responsibilities

The system separates external information retrieval from LLM reasoning.

```
External Web
     |
     v
Tavily Search
     |
     v
Retrieved Information
     |
     v
   Gemini
     |
     v
Analysis and Recommendations
```

Tavily should not replace the Destination Agent.

The Destination Agent will use the retrieved information as research context and then generate the structured destination analysis.

### Destination Research Tool

A LangChain tool will be created around the Tavily Search API.

Conceptually:

```
@tool
search_destination(destination, preferences)
        |
        v
   Tavily Search
        |
        v
  Search Results
```

The tool will receive the destination and relevant travel preferences and retrieve information that can help the Destination Agent analyze the destination.

### Example Research

For a request such as:

```
Destination: Goa
Duration: 5 days
Travelers: 2
Budget: ₹50,000
Preferences:
- beaches
- adventure
- food
```

The Destination Research Tool may perform searches related to:

```
Goa best areas to visit for beaches and adventure
Goa travel attractions
Goa travel considerations
Goa experiences for adventure travelers
```

The retrieved information will then be supplied to Gemini for analysis.

### LLM Responsibilities

Gemini remains responsible for:

1. Understanding the user's travel requirements
2. Interpreting retrieved destination information
3. Selecting relevant information
4. Connecting information with user preferences
5. Producing practical recommendations
6. Generating structured output using the Pydantic schema

The LLM should not be treated as the primary source of current destination facts when external research is available.

### Structured Output

The existing `DestinationAnalysis` schema will be retained:

```
DestinationAnalysis
├── overview
├── recommended_areas
├── travel_considerations
└── preference_suggestions
```

The research results will provide context for generating these fields.

### Integration with TravelState

The final structured destination analysis will be stored in the shared `TravelState`.

```
TravelState
     |
     +── destination
     +── duration
     +── travelers
     +── budget
     +── preferences
     |
     +── destination_data
              |
              ├── overview
              ├── recommended_areas
              ├── travel_considerations
              └── preference_suggestions
```

This allows subsequent agents such as Stay, Activity, Weather, Food, and Itinerary to use destination information.

### Relationship with Other Agents

The Destination Agent will run before the independent research agents because destination information provides useful context for the rest of the workflow.

The planned workflow is:

```
User Request
      |
      v
Destination Agent
      |
      v
Destination Research
      |
      v
DestinationAnalysis
      |
      +----------------+----------------+
      |                |                |
      v                v                v
   Stay            Activity         Weather
   Agent             Agent            Agent
      |                |                |
      +----------------+----------------+
                       |
                       v
                   Food Agent
                       |
                       v
                Itinerary Agent
```

### API vs LLM Responsibilities

The architecture follows a clear separation:

```
API / Search Tool
    |
    +-- Retrieve external information
    |
    +-- Provide source results
    |
    v
   Gemini
    |
    +-- Understand information
    +-- Reason about relevance
    +-- Adapt to user preferences
    +-- Generate recommendations
    |
    v
Structured Output
```

The search provider retrieves information; the LLM performs the reasoning and analysis.

### Error Handling Considerations

The Destination Research Tool should handle:

* Missing Tavily API key
* Network errors
* HTTP errors
* Empty search results
* Invalid responses
* Search failures

The agent should not silently fabricate research results when the external search fails.

Error handling and retry behavior will be improved later as part of the project's engineering and productionization phase.

### Testing Strategy

The Destination Research implementation will be tested at multiple levels:

1. Tool-level testing
2. Search/API response handling
3. Agent-level testing
4. Structured output validation
5. LangGraph integration
6. Real API end-to-end testing

Mock responses may be used for deterministic unit tests, while a real API test will verify that the complete research flow works with Tavily.

### Initial Implementation Decision

The first implementation will use the Tavily Search API through a custom LangChain tool.

The project will not initially use Tavily's complete research workflow as the Destination Agent itself.

This keeps the architecture under our control:

```
LangGraph
    |
    v
Destination Agent
    |
    v
LangChain Tool
    |
    v
Tavily Search API
```

More advanced research capabilities can be evaluated later if they provide meaningful value to the project.

### Conclusion

The Destination Agent will be upgraded from an LLM-only agent to a research-enabled agent.

The final responsibility split is:

```
Tavily
    -> Retrieve current web information

Gemini
    -> Analyze and reason over the information

Pydantic
    -> Validate structured output

LangGraph
    -> Orchestrate the agent within the travel workflow
```

This provides a stronger foundation for the multi-agent travel-planning system while keeping the architecture modular and extensible.

### Sources

* Tavily Search API:
  https://docs.tavily.com/documentation/api-reference/search
* Tavily Documentation:
  https://docs.tavily.com/
