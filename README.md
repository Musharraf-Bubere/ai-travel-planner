# ✈️ AI Travel Planner — Multi-Agent Travel Planning System

<p align="center">

  <img src="https://img.shields.io/badge/Python-3.x-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python">

  <img src="https://img.shields.io/badge/LangChain-Framework-1C3C3C?style=for-the-badge" alt="LangChain">

  <img src="https://img.shields.io/badge/LangGraph-Agent%20Orchestration-1C3C3C?style=for-the-badge" alt="LangGraph">

  <img src="https://img.shields.io/badge/Google%20Gemini-LLM-4285F4?style=for-the-badge&logo=google&logoColor=white" alt="Google Gemini">

  <img src="https://img.shields.io/badge/FastAPI-Backend-009688?style=for-the-badge&logo=fastapi&logoColor=white" alt="FastAPI">

  <img src="https://img.shields.io/badge/Streamlit-Frontend-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white" alt="Streamlit">

</p>

<p align="center">

  <img src="https://img.shields.io/badge/MCP-Model%20Context%20Protocol-6B46C1?style=for-the-badge" alt="MCP">

  <img src="https://img.shields.io/badge/PostgreSQL-Database-4169E1?style=for-the-badge&logo=postgresql&logoColor=white" alt="PostgreSQL">

  <img src="https://img.shields.io/badge/Pytest-Testing-0A9EDC?style=for-the-badge&logo=pytest&logoColor=white" alt="Pytest">

  <img src="https://img.shields.io/badge/Docker-Containerization-2496ED?style=for-the-badge&logo=docker&logoColor=white" alt="Docker">

  <img src="https://img.shields.io/badge/GitHub%20Actions-CI%2FCD-2088FF?style=for-the-badge&logo=githubactions&logoColor=white" alt="GitHub Actions">

</p>

<p align="center">
  <b>🤖 Agentic AI • 🔀 Multi-Agent System • 🧠 LangGraph • 🌍 Travel Intelligence</b>
</p>

---

## 🌍 Overview

**AI Travel Planner** is an Agentic AI application that uses a coordinated **multi-agent architecture** to research, analyze, and generate personalized travel plans.

Instead of relying on a single LLM prompt to generate an entire trip, the system divides travel planning into specialized tasks and assigns those tasks to dedicated AI agents.

The agents are coordinated using **LangGraph**, which manages the workflow, shared state, agent execution, and decision-making.

The system combines:

- 🤖 AI Agents
- 👥 Multi-Agent Collaboration
- 🔀 LangGraph Orchestration
- 🧠 Google Gemini
- 🔧 Tool Calling
- 🌐 External APIs
- 🔌 Model Context Protocol
- 📊 Structured Outputs
- ⚡ FastAPI
- 🖥️ Streamlit

The result is a personalized, structured, and practical **day-by-day travel itinerary**.

---

## 🎯 Problem Statement

Planning a trip manually requires researching information from multiple sources.

A traveler may need to separately find:

- 📍 Destination information
- 🏨 Accommodation
- 🌤️ Weather
- 🎯 Activities
- 🍴 Restaurants
- 🗺️ Places and attractions
- 💰 Budget information
- 📅 Daily itinerary

The information is fragmented across different websites and applications.

The traveler must then manually compare the information and combine everything into a practical travel plan.

### 💡 Problem

> Travel planning is time-consuming because relevant information is distributed across multiple sources and must be manually researched, evaluated, and organized.

---

## 💡 Solution

AI Travel Planner automates the planning process using specialized AI agents.

Instead of:

    User
      ↓
    Single LLM
      ↓
    Generic Travel Answer

the system uses:

    User
      ↓
    LangGraph Orchestrator
      ↓
    Multiple Specialized Agents
      ↓
    External Tools / APIs
      ↓
    Shared Travel State
      ↓
    Itinerary Agent
      ↓
    Personalized Travel Plan

This allows different parts of the planning problem to be handled independently and then combined into a final itinerary.

---

# 🏗️ System Architecture

    ┌──────────────────────────────────────────┐
    │                  USER                    │
    │                                          │
    │ Destination • Budget • Dates • Preferences│
    └─────────────────────┬────────────────────┘
                          │
                          ▼
    ┌──────────────────────────────────────────┐
    │               STREAMLIT                  │
    │                FRONTEND                  │
    └─────────────────────┬────────────────────┘
                          │
                          ▼
    ┌──────────────────────────────────────────┐
    │                 FASTAPI                  │
    │                 BACKEND                  │
    └─────────────────────┬────────────────────┘
                          │
                          ▼
    ┌──────────────────────────────────────────┐
    │             LANGGRAPH                    │
    │           ORCHESTRATOR                   │
    └─────────────────────┬────────────────────┘
                          │
                          ▼
    ┌──────────────────────────────────────────┐
    │            SHARED TRAVEL STATE            │
    └─────────────────────┬────────────────────┘
                          │
             ┌────────────┼────────────┐
             │            │            │
             ▼            ▼            ▼
       ┌──────────┐ ┌──────────┐ ┌──────────┐
       │Destination│ │   Stay   │ │ Activity │
       │   Agent  │ │   Agent  │ │   Agent  │
       └────┬─────┘ └────┬─────┘ └────┬─────┘
            │             │             │
            └─────────────┼─────────────┘
                          │
                          ▼
                    ┌──────────┐
                    │ Weather  │
                    │  Agent   │
                    └────┬─────┘
                         │
                         ▼
                    ┌──────────┐
                    │   Food   │
                    │  Agent   │
                    └────┬─────┘
                         │
                         ▼
                  ┌──────────────┐
                  │  Itinerary   │
                  │    Agent     │
                  └──────┬───────┘
                         │
                         ▼
                  ┌──────────────┐
                  │Final Travel  │
                  │    Plan      │
                  └──────────────┘

---

# 🤖 Multi-Agent Architecture

The system divides travel planning into specialized agents.

## 📍 Destination Agent

Responsible for destination-level research.

### Responsibilities

- Destination overview
- Popular areas
- Major attractions
- Travel considerations
- Location context

---

## 🏨 Stay Agent

Responsible for accommodation recommendations.

### Responsibilities

- Hotel recommendations
- Accommodation options
- Approximate pricing
- Location suitability
- Budget considerations

---

## 🎯 Activity Agent

Responsible for finding activities and attractions.

### Responsibilities

- Tourist attractions
- Activities
- Experiences
- Sightseeing
- Preference-based recommendations

---

## 🌤️ Weather Agent

Responsible for weather information.

### Responsibilities

- Weather conditions
- Temperature
- Rain probability
- Forecast information
- Activity suitability

---

## 🍴 Food Agent

Responsible for food and restaurant recommendations.

### Responsibilities

- Local cuisine
- Restaurants
- Food experiences
- Budget-friendly options
- Preference-based recommendations

---

## 📅 Itinerary Agent

Responsible for combining information from the other agents.

### Responsibilities

- Day-by-day planning
- Activity sequencing
- Location-aware scheduling
- Budget considerations
- Travel preferences
- Practical itinerary generation

---

# 🔀 Agent Orchestration

**LangGraph** acts as the orchestrator of the multi-agent system.

The orchestrator manages:

- Agent execution
- Workflow progression
- Shared state
- Agent dependencies
- Conditional routing
- Parallel execution
- Final result generation

Conceptually:

    User Request
         │
         ▼
    ┌───────────────┐
    │   LangGraph   │
    │ Orchestrator  │
    └───────┬───────┘
            │
       ┌────┼────┐
       │    │    │
       ▼    ▼    ▼
     Stay Weather Activity
     Agent Agent   Agent
       │    │      │
       └────┼──────┘
            │
            ▼
      Itinerary Agent
            │
            ▼
       Final Result

---

# 🧠 Shared State

Agents need to exchange information during the workflow.

The system maintains a shared travel state.

Example:

    TravelState

    ├── destination
    ├── travel_dates
    ├── duration
    ├── travelers
    ├── budget
    ├── preferences
    ├── destination_data
    ├── stay_options
    ├── activities
    ├── restaurants
    ├── weather
    └── itinerary

This allows information produced by one agent to become available to other agents.

---

# 🔧 Tool Calling

Agents can use external tools when additional information is required.

    Agent
      │
      ▼
     LLM
      │
      ▼
    Tool Selection
      │
      ▼
    External Tool
      │
      ▼
    API / Service
      │
      ▼
    Tool Result
      │
      ▼
    Agent
      │
      ▼
    Structured Result

Potential tools include:

- 🔎 Web Search
- 🌤️ Weather
- 📍 Places
- 🍴 Restaurants
- 🗺️ Maps
- 🌐 Travel Information

---

# 🔌 Model Context Protocol (MCP)

AI Travel Planner incorporates **Model Context Protocol (MCP)** as an advanced tool-integration capability.

MCP provides a standardized way for AI applications to interact with external tools and resources.

Conceptually:

    AI Agent
        │
        ▼
       MCP
        │
        ├── Search Tools
        ├── Weather Tools
        ├── Places Tools
        └── Travel Tools

MCP allows tool integrations to follow a standardized protocol instead of every integration requiring a completely different communication pattern.

---

# 🧠 LLM Architecture

The initial LLM provider is **Google Gemini**.

Gemini is responsible for:

- Understanding user requirements
- Agent reasoning
- Travel recommendations
- Information summarization
- Itinerary generation
- Structured response generation

The architecture uses an LLM abstraction layer.

    ┌──────────────────┐
    │   LLM Interface  │
    └────────┬─────────┘
             │
       ┌─────┼─────┐
       │     │     │
       ▼     ▼     ▼
    Gemini OpenAI Anthropic

Gemini is the primary provider, while the abstraction allows future provider changes without rewriting the complete agent architecture.

---

# 📊 Structured Output

LLM responses are represented using structured schemas where required.

Example models:

- `DestinationResult`
- `StayResult`
- `ActivityResult`
- `WeatherResult`
- `RestaurantResult`
- `ItineraryResult`

Structured output makes information easier to:

- Validate
- Store
- Pass between agents
- Process programmatically
- Display in the frontend

**Pydantic** is used for validation and structured data models.

---

# 🔀 Conditional Workflows

The system can make workflow decisions based on the current state or agent results.

Example:

    Weather Result
          │
          ▼
    Suitable for Outdoor Activities?
          │
       ┌──┴──┐
       │     │
      YES    NO
       │     │
       ▼     ▼
    Outdoor Indoor
    Activities Activities

Conditional routing allows the workflow to adapt dynamically instead of always following a fixed sequence.

---

# ⚡ Parallel Workflows

Some travel-planning tasks are independent and can be executed in parallel.

For example:

    Travel Request
          │
          ▼
    LangGraph Orchestrator
          │
      ┌───┼────────┐
      │   │        │
      ▼   ▼        ▼
    Stay Weather Activity
    Agent Agent   Agent
      │   │        │
      └───┼────────┘
          │
          ▼
    Itinerary Agent

Parallel execution reduces unnecessary waiting and demonstrates practical workflow orchestration.

---

# 🖥️ Frontend

The frontend is built using **Streamlit**.

The interface allows users to provide:

- 📍 Destination
- 📅 Travel dates
- 🌙 Duration
- 👥 Number of travelers
- 💰 Budget
- ❤️ Travel preferences

The generated results can include:

- Destination information
- Hotel recommendations
- Weather
- Activities
- Restaurants
- Day-by-day itinerary
- Estimated budget

---

# ⚡ Backend

The backend is built using **FastAPI**.

FastAPI is responsible for:

- REST API endpoints
- Request validation
- Calling the LangGraph workflow
- Returning structured responses
- Error handling

Architecture:

    Streamlit
        │
        ▼
    FastAPI
        │
        ▼
    LangGraph
        │
        ▼
    Multi-Agent System

---

# 🗄️ Persistence

The application supports persistence for stateful workflows and travel-planning sessions.

PostgreSQL is used as the database layer where persistent application data is required.

Potential persisted information includes:

- Travel requests
- Workflow state
- Conversation/session information
- Planning results
- Checkpoints

---

# 🧪 Testing

Testing is implemented using **Pytest**.

Testing areas include:

- Input validation
- Utility functions
- Agent behavior
- Structured outputs
- Tool integrations
- LangGraph workflows
- FastAPI endpoints
- Integration behavior

Run tests with:

    pytest

---

# 🐳 Docker

The application can be containerized using Docker.

Build:

    docker build -t ai-travel-planner .

Run:

    docker run --env-file .env -p 8000:8000 ai-travel-planner

Docker provides a reproducible application environment.

---

# 🔄 CI/CD

GitHub Actions is used for automation.

The CI pipeline can perform:

    Git Push
       │
       ▼
    GitHub Actions
       │
       ├── Install Dependencies
       │
       ├── Run Tests
       │
       ├── Validate Application
       │
       ▼
    Build / Deployment

---

# 🛠️ Technology Stack

| Category | Technologies |
|----------|--------------|
| Language | Python |
| LLM | Google Gemini |
| AI Framework | LangChain |
| Agent Orchestration | LangGraph |
| Agentic AI | Multi-Agent, Tool Calling, MCP |
| Backend | FastAPI |
| Validation | Pydantic |
| Frontend | Streamlit |
| Search | Web Search API |
| Weather | Weather API |
| Places | Maps / Places API |
| Database | PostgreSQL |
| ORM | SQLAlchemy |
| Testing | Pytest |
| Containerization | Docker |
| CI/CD | GitHub Actions |
| Version Control | Git, GitHub |

---

# 📁 Project Structure

    ai-travel-planner/
    │
    ├── docs/
    │   ├── 01-project-overview.md
    │   ├── 02-research.md
    │   └── architecture/
    │
    ├── src/
    │   ├── agents/
    │   ├── graph/
    │   ├── tools/
    │   ├── models/
    │   ├── services/
    │   ├── config/
    │   └── ...
    │
    ├── tests/
    │   ├── unit/
    │   ├── integration/
    │   └── ...
    │
    ├── .env.example
    ├── .gitignore
    ├── Dockerfile
    ├── README.md
    ├── requirements.txt
    └── ...

The final structure may evolve during implementation and refactoring.

---

# 🚀 Installation

## 1. Clone the Repository

    git clone https://github.com/Musharraf-Bubere/ai-travel-planner.git

    cd ai-travel-planner

---

## 2. Create a Virtual Environment

### Windows

    python -m venv venv

    venv\Scripts\activate

### Linux / macOS

    python3 -m venv venv

    source venv/bin/activate

---

## 3. Install Dependencies

    pip install -r requirements.txt

---

## 4. Configure Environment Variables

Create a `.env` file based on `.env.example`.

Example:

    GOOGLE_API_KEY=your_google_api_key

    TAVILY_API_KEY=your_tavily_api_key

    WEATHER_API_KEY=your_weather_api_key

    GOOGLE_MAPS_API_KEY=your_google_maps_api_key

    DATABASE_URL=your_database_url

    LLM_PROVIDER=gemini

Never commit API keys or other secrets to GitHub.

---

# ▶️ Running the Application

## Start FastAPI

    uvicorn src.main:app --reload

## Start Streamlit

    streamlit run src/frontend/app.py

The exact commands may change depending on the final project structure.

---

# 🧳 Example Input

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

# 📅 Example Output

    GOA — 5 DAY TRAVEL PLAN

    👥 Travelers: 2
    💰 Budget: ₹30,000

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

Actual recommendations and costs depend on the user's requirements and the information returned by external services.

---

# 🔐 Security

The application follows basic security practices:

- API keys stored in environment variables
- Secrets excluded from Git
- Input validation
- Error handling
- No hard-coded credentials
- Controlled external API access
- Environment-specific configuration

---

# ⚠️ Limitations

AI Travel Planner depends on external services and APIs.

Therefore:

- Travel information may change
- Prices may change
- Weather forecasts may change
- API availability may vary
- External API rate limits may apply
- Recommendations may not always be perfect
- LLM-generated information should be verified before real-world bookings

The application is intended as an intelligent travel-planning assistant and not as a guaranteed booking or travel advisory service.

---

# 🔮 Future Enhancements

Potential future improvements include:

- ✈️ Flight booking integrations
- 🏨 Hotel booking integrations
- 💰 Real-time price comparison
- 🗺️ Interactive maps
- 👤 User accounts
- 🧠 Advanced long-term memory
- 🎙️ Voice-based travel planning
- 🖼️ Multimodal travel planning
- 📸 Image-based destination exploration
- 🌍 More travel providers
- 📊 Advanced agent evaluation
- 🔍 Enhanced observability

---

# 🎓 Learning Outcomes

This project demonstrates practical experience with:

### Generative AI

- Large Language Models
- Prompt Engineering
- Structured Generation

### Agentic AI

- AI Agents
- Multi-Agent Systems
- Agent Orchestration
- Tool Calling
- Shared State
- Conditional Workflows
- Parallel Workflows
- MCP

### LLM Engineering

- Gemini Integration
- LLM Abstraction
- Structured Outputs
- External Tool Integration
- Error Handling

### Backend Engineering

- FastAPI
- REST APIs
- Pydantic
- Request Validation
- Exception Handling
- Persistence

### Software Engineering

- Modular Architecture
- Automated Testing
- Git
- GitHub
- Docker
- CI/CD

---

# 📈 Development Workflow

The project follows a structured learning and development workflow:

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

This approach ensures that each major implementation is supported by conceptual understanding, research, testing, refactoring, and documentation.

---

# 🌟 Project Highlights

| Area | Implementation |
|------|----------------|
| 🤖 Agentic AI | Multi-Agent Travel Planning |
| 🔀 Orchestration | LangGraph |
| 🧠 LLM | Google Gemini |
| 🔧 Tools | External Travel APIs |
| 🔌 Protocol | MCP |
| 📊 State | Shared Stateful Workflow |
| ⚡ Backend | FastAPI |
| 🖥️ Frontend | Streamlit |
| 🗄️ Persistence | PostgreSQL |
| 🧪 Testing | Pytest |
| 🐳 DevOps | Docker |
| 🔄 CI/CD | GitHub Actions |

---

# 👨‍💻 Author

**Musharraf Bubéré**

GitHub: https://github.com/Musharraf-Bubere

---

# 📄 License

This project is intended for educational, portfolio, and demonstration purposes.
