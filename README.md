# AI Travel Planner — Multi-Agent Travel Planning System

AI Travel Planner is an Agentic AI application that uses a coordinated multi-agent architecture to research, analyze, and generate personalized travel plans.

The system accepts a user's destination, travel dates, budget, number of travelers, and preferences, then coordinates specialized AI agents to gather relevant travel information and produce a structured day-by-day itinerary.

Built with Python, LangChain, LangGraph, Google Gemini, FastAPI, Streamlit, external travel APIs, and MCP, the project demonstrates how Agentic AI can be applied to a practical real-world planning problem.

---

## Features

- Multi-Agent AI travel planning
- Google Gemini-powered reasoning and generation
- LangGraph-based agent orchestration
- LangChain-based LLM and tool integration
- Destination research
- Accommodation recommendations
- Activities and attractions
- Restaurant and food recommendations
- Weather information
- Location-aware recommendations
- Budget-aware travel planning
- Personalized day-by-day itinerary
- External tool and API integration
- Model Context Protocol (MCP) integration
- Structured agent outputs
- Conditional workflows
- Parallel workflows
- Stateful workflow and persistence support
- FastAPI backend
- Streamlit frontend
- Automated testing
- Docker support
- GitHub Actions CI/CD
- Deployment-ready architecture

---

## Problem Statement

Planning a trip manually requires researching information from multiple sources and combining it into a practical itinerary.

A traveler may need to separately research:

- Destination information
- Hotels and accommodation
- Weather
- Places to visit
- Activities
- Restaurants
- Transportation considerations
- Budget
- Daily schedule

The information is fragmented across different platforms, making the planning process time-consuming.

AI Travel Planner addresses this problem by using multiple specialized AI agents that collaborate through an orchestrated workflow.

---

## Solution

Instead of relying on a single LLM prompt to generate an entire trip, the system divides travel planning into specialized responsibilities.

    User
      |
      v
    Streamlit Frontend
      |
      v
    FastAPI Backend
      |
      v
    LangGraph Orchestrator
      |
      v
    Shared Travel State
      |
      +-------------------+-------------------+
      |                   |                   |
      v                   v                   v
    Destination Agent   Stay Agent      Activity Agent
      |                   |                   |
      +-------------------+-------------------+
                          |
                          v
                    Weather Agent
                          |
                          v
                       Food Agent
                          |
                          v
                   Itinerary Agent
                          |
                          v
                  Final Travel Plan

Each agent focuses on a specific task while LangGraph coordinates the overall workflow and shared state.

---

## System Architecture

    +---------------------------------------------------+
    |                   Streamlit UI                    |
    +-------------------------+-------------------------+
                              |
                              v
    +---------------------------------------------------+
    |                     FastAPI                       |
    +-------------------------+-------------------------+
                              |
                              v
    +---------------------------------------------------+
    |              LangGraph Orchestrator               |
    +-------------------------+-------------------------+
                              |
                              v
    +---------------------------------------------------+
    |                 Shared Travel State               |
    +-------------------------+-------------------------+
                              |
              +---------------+---------------+
              |               |               |
              v               v               v
       Destination Agent   Stay Agent    Activity Agent
              |               |               |
              +---------------+---------------+
                              |
                              v
                       Weather Agent
                              |
                              v
                          Food Agent
                              |
                              v
                       Itinerary Agent
                              |
                              v
                       Final Response

---

## Agent Responsibilities

### Destination Agent

Researches the selected destination and provides relevant travel information.

Responsibilities include:

- Destination overview
- Popular areas
- Major attractions
- Travel considerations
- Location context

### Stay Agent

Handles accommodation recommendations.

Responsibilities include:

- Hotel and stay recommendations
- Approximate accommodation costs
- Location suitability
- Budget considerations

### Activity Agent

Researches activities and attractions.

Responsibilities include:

- Tourist attractions
- Activities
- Experiences
- Sightseeing options
- Preference-based recommendations

### Weather Agent

Provides weather-related information for the travel period.

Responsibilities include:

- Weather conditions
- Temperature
- Rain probability
- Weather considerations
- Activity suitability

### Food Agent

Handles restaurant and food recommendations.

Responsibilities include:

- Local cuisine
- Restaurants
- Food experiences
- Budget-friendly options
- Preference-based recommendations

### Itinerary Agent

Combines the information collected by the other agents and generates the final travel plan.

Responsibilities include:

- Day-by-day planning
- Activity sequencing
- Location-aware scheduling
- Budget considerations
- Travel preferences
- Practical itinerary generation

---

## Agentic AI Workflow

The system follows an agentic workflow rather than a simple prompt-response architecture.

    User Request
         |
         v
    Understand Requirements
         |
         v
    Create Travel State
         |
         v
    Agent Orchestration
         |
         +--> Destination Research
         |
         +--> Stay Research
         |
         +--> Activity Research
         |
         +--> Weather Research
         |
         +--> Food Research
         |
         v
    Combine Information
         |
         v
    Generate Itinerary
         |
         v
    Validate Structured Result
         |
         v
    Return Final Travel Plan

---

## Shared State

The system maintains a shared travel-planning state that allows agents to exchange information.

Example state:

    TravelState

    - destination
    - travel_dates
    - duration
    - travelers
    - budget
    - preferences
    - destination_data
    - stay_options
    - activities
    - restaurants
    - weather
    - itinerary

The shared state allows the output of one agent to become available to other agents.

---

## Orchestration with LangGraph

LangGraph is used as the orchestration layer.

It manages:

- Nodes
- Edges
- Shared state
- Agent execution
- Conditional routing
- Parallel execution
- Workflow progression
- Stateful execution

Conceptually:

    LangGraph
    Orchestrator
          |
    +-----+-----+-----+
    |           |     |
    v           v     v
    Destination  Stay  Activities
    Agent        Agent Agent
    |           |     |
    +-----------+-----+
                |
                v
          Itinerary Agent

---

## Conditional Workflows

The system can make workflow decisions based on the current state or agent results.

Example:

    Weather Result
          |
          v
    Suitable for Outdoor Activities?
          |
       +--+--+
       |     |
      Yes    No
       |     |
       v     v
    Outdoor Indoor
    Activities Activities

Conditional routing allows the system to adapt its workflow instead of following one fixed path.

---

## Parallel Workflows

Independent travel-planning tasks can be executed in parallel.

For example:

    Travel Request
          |
          v
    Orchestrator
          |
    +-----+-----+-----+
    |           |     |
    v           v     v
    Stay      Weather Activities
    Agent      Agent     Agent
    |           |         |
    +-----------+---------+
                |
                v
          Itinerary Agent

Parallel execution can reduce unnecessary waiting and demonstrates practical workflow orchestration.

---

## Tool Calling

Agents can interact with external tools to retrieve real-world information.

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
    API / Service
      |
      v
    Tool Result
      |
      v
    Agent

Potential tools include:

- Web search
- Weather lookup
- Places search
- Restaurant search
- Location services
- Travel information services

---

## Model Context Protocol

The project incorporates Model Context Protocol (MCP) as part of its advanced Agentic AI architecture.

MCP provides a standardized way for AI applications to interact with external tools and resources.

Conceptually:

    AI Agent
       |
       v
      MCP
       |
       +----> Search Tools
       |
       +----> Weather Tools
       |
       +----> Places Tools
       |
       +----> Travel Tools

---

## LLM Architecture

Google Gemini is the initial LLM provider.

The application uses an LLM abstraction layer so that agent logic is not tightly coupled to a single provider.

    LLM Interface
          |
    +-----+-----+-----+
    |           |     |
    v           v     v
    Gemini     OpenAI Anthropic

Gemini is the primary implementation, while the abstraction keeps the architecture extensible.

---

## Structured Output

Agent results are represented using structured schemas instead of relying entirely on free-form text.

Examples:

- DestinationResult
- StayResult
- ActivityResult
- WeatherResult
- RestaurantResult
- ItineraryResult

Structured outputs make information easier to:

- Validate
- Store
- Pass between agents
- Process programmatically
- Display in the frontend

Pydantic is used for data validation and structured models.

---

## Technology Stack

### Programming Language

- Python

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

### Backend

- FastAPI
- Pydantic
- Uvicorn

### Frontend

- Streamlit

### External Services

- Web Search API
- Weather API
- Places / Maps API
- Travel-related APIs

### Database / Persistence

- PostgreSQL
- SQLAlchemy
- Async database support

### Testing

- Pytest

### DevOps

- Docker
- GitHub Actions

### Version Control

- Git
- GitHub

---

## Project Architecture by Layer

    Frontend
    Streamlit
        |
        v
    Backend
    FastAPI
        |
        v
    Agentic AI Layer
    LangGraph + LangChain
        |
        v
    Multi-Agent System
        |
        v
    LLM Layer
    Google Gemini
        |
        v
    Tool Layer
    Search + Weather + Places + MCP
        |
        v
    Persistence Layer
    PostgreSQL

---

## Example Input

    Destination: Goa

    Travel Duration: 5 Days

    Travelers: 2

    Budget: ₹30,000

    Preferences:
    - Beaches
    - Local Food
    - Sightseeing
    - Relaxing Activities

---

## Example Output

    GOA — 5 DAY TRAVEL PLAN

    Travelers: 2
    Budget: ₹30,000

    DAY 1
    - Arrival
    - Hotel check-in
    - Beach visit
    - Local dinner

    DAY 2
    - Fort Aguada
    - North Goa sightseeing
    - Beach activity
    - Restaurant recommendation

    DAY 3
    - Water activity
    - Local market
    - Sunset location
    - Dinner recommendation

    DAY 4
    - South Goa sightseeing
    - Cultural attraction
    - Local food experience

    DAY 5
    - Relaxed morning
    - Final sightseeing
    - Departure

    ESTIMATED BUDGET

    Accommodation: ₹12,000
    Food: ₹6,000
    Transportation: ₹5,000
    Activities: ₹3,000
    Other: ₹2,000

    Estimated Total: ₹28,000

The actual output depends on the user's requirements and the information returned by the connected tools and APIs.

---

## Project Structure

    ai-travel-planner/
    |
    +-- docs/
    |   +-- 01-project-overview.md
    |   +-- 02-research.md
    |   +-- architecture/
    |
    +-- src/
    |
    +-- tests/
    |
    +-- .env.example
    +-- .gitignore
    +-- Dockerfile
    +-- README.md
    +-- requirements.txt

The exact structure may evolve as the application is implemented and refactored.

---

## Installation

### 1. Clone the Repository

    git clone https://github.com/Musharraf-Bubere/ai-travel-planner.git
    cd ai-travel-planner

### 2. Create a Virtual Environment

Windows:

    python -m venv venv
    venv\Scripts\activate

Linux / macOS:

    python3 -m venv venv
    source venv/bin/activate

### 3. Install Dependencies

    pip install -r requirements.txt

### 4. Configure Environment Variables

Create a `.env` file based on `.env.example`.

Required API keys and configuration may include:

    GOOGLE_API_KEY=your_google_api_key
    TAVILY_API_KEY=your_tavily_api_key
    WEATHER_API_KEY=your_weather_api_key
    GOOGLE_MAPS_API_KEY=your_google_maps_api_key
    DATABASE_URL=your_database_url

    LLM_PROVIDER=gemini

Never commit API keys or other secrets to GitHub.

---

## Running the Application

### Start the FastAPI Backend

    uvicorn src.main:app --reload

### Start the Streamlit Frontend

    streamlit run src/frontend/app.py

The exact commands may vary depending on the final project structure.

---

## Testing

Run the test suite using:

    pytest

Testing covers important application components such as:

- Validation
- Utility functions
- Tool integrations
- Agent outputs
- LangGraph workflows
- API endpoints
- Integration behavior

---

## Docker

The application can be containerized using Docker.

Build the image:

    docker build -t ai-travel-planner .

Run the container:

    docker run --env-file .env -p 8000:8000 ai-travel-planner

---

## CI/CD

GitHub Actions is used to automate development checks.

The CI pipeline can perform:

    Git Push
       |
       v
    GitHub Actions
       |
       +--> Install Dependencies
       |
       +--> Run Tests
       |
       +--> Validate Application
       |
       v
    Build / Deployment

---

## Security

The application follows basic security practices:

- API keys stored in environment variables
- Secrets excluded from Git
- Input validation
- API error handling
- Controlled external API access
- No hard-coded credentials
- Environment-specific configuration

---

## Engineering Practices

The project follows software engineering principles including:

- Modular architecture
- Separation of concerns
- Type hints
- Pydantic validation
- Environment-based configuration
- Error handling
- Logging
- Automated testing
- Git version control
- CI/CD
- Containerization
- Documentation

---

## Development Workflow

The project follows this development workflow:

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

This workflow ensures that implementation is supported by conceptual understanding, research, testing, and documentation.

---

## Key Concepts Demonstrated

### Generative AI

- Large Language Models
- Prompt Engineering
- Structured Generation

### Agentic AI

- AI Agents
- Tool Calling
- Agent Planning
- Multi-Agent Systems
- Agent Orchestration
- Shared State
- Conditional Workflows
- Parallel Workflows
- MCP

### LLM Engineering

- Model Integration
- LLM Abstraction
- Structured Outputs
- Error Handling
- External Tool Integration

### Backend Engineering

- REST APIs
- FastAPI
- Request Validation
- Exception Handling
- Persistence

### Software Engineering

- Modular Architecture
- Testing
- Git
- GitHub
- Docker
- CI/CD

---

## Limitations

AI Travel Planner depends on external services and APIs.

Therefore:

- Travel information may change
- API availability may vary
- Recommendations may not always be perfect
- Prices may change over time
- Weather forecasts may change
- External API rate limits may apply
- LLM-generated information should be verified before making real-world bookings

The application is intended as an intelligent planning assistant and not as a guaranteed booking or travel advisory service.

---

## Future Improvements

Potential future improvements include:

- Flight booking integrations
- Hotel booking integrations
- Real-time price comparison
- Maps visualization
- User accounts
- Advanced memory
- More travel providers
- Voice-based travel planning
- Multimodal travel planning
- Image-based destination exploration
- Personalized long-term travel preferences
- Advanced agent evaluation
- Enhanced observability

These features are outside the core project scope unless they provide meaningful value.

---

## Learning Outcomes

By completing this project, the following practical skills are demonstrated:

- Building LLM-powered applications
- Designing AI agents
- Designing multi-agent systems
- Building LangGraph workflows
- Managing shared agent state
- Implementing tool calling
- Integrating external APIs
- Working with structured LLM outputs
- Designing conditional workflows
- Designing parallel workflows
- Using MCP
- Building FastAPI backends
- Building Streamlit interfaces
- Implementing persistence
- Writing automated tests
- Containerizing applications
- Building CI/CD workflows
- Deploying AI applications

---

## Project Goal

The goal of AI Travel Planner is to demonstrate how Agentic AI can solve a practical real-world problem through:

    LLM
      +
    AI Agents
      +
    Multi-Agent Collaboration
      +
    LangGraph Orchestration
      +
    Tools
      +
    External APIs
      +
    Structured Data
      +
    Software Engineering

The result is a complete Multi-Agent Travel Planning System capable of transforming user travel requirements into a personalized and structured itinerary.

---

## Author

**Musharraf Bubéré**

GitHub: https://github.com/Musharraf-Bubere

---

## License

This project is intended for educational and portfolio purposes.