# ✈️ AI Travel Planner — Multi-Agent Travel Planning System

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.11+-blue?logo=python&logoColor=white" alt="Python">
  <img src="https://img.shields.io/badge/LangGraph-Agentic%20AI-orange" alt="LangGraph">
  <img src="https://img.shields.io/badge/LangChain-LLM%20Framework-green" alt="LangChain">
  <img src="https://img.shields.io/badge/MCP-Model%20Context%20Protocol-purple" alt="MCP">
  <img src="https://img.shields.io/badge/FastAPI-Backend-009688?logo=fastapi&logoColor=white" alt="FastAPI">
  <img src="https://img.shields.io/badge/Streamlit-Frontend-FF4B4B?logo=streamlit&logoColor=white" alt="Streamlit">
  <img src="https://img.shields.io/badge/PostgreSQL-Database-336791?logo=postgresql&logoColor=white" alt="PostgreSQL">
  <img src="https://img.shields.io/badge/Docker-Containerized-2496ED?logo=docker&logoColor=white" alt="Docker">
  <img src="https://img.shields.io/badge/SerpApi-Real--World%20Search-black" alt="SerpApi">
  <img src="https://img.shields.io/badge/Tavily-Web%20Search-blueviolet" alt="Tavily">
  <img src="https://img.shields.io/badge/ReportLab-PDF-red" alt="ReportLab">
  <img src="https://img.shields.io/badge/SQLAlchemy-ORM-red" alt="SQLAlchemy">
  <img src="https://img.shields.io/badge/Alembic-Migrations-6BA81E" alt="Alembic">
</p>

<p align="center">
  <b>🤖 An intermediate-level Agentic AI travel planning system that researches destinations, accommodations, activities, restaurants, and weather to generate personalized travel plans.</b>
</p>

---

## 🌍 Project Overview

**AI Travel Planner** is a multi-agent travel planning application that automates the process of researching and creating personalized travel itineraries.

The application combines:

- 🤖 Agentic AI
- 🧠 LangGraph
- 🔗 LangChain
- 🔌 Model Context Protocol (MCP)
- 🔎 Tavily
- 🗺️ SerpApi
- 🚀 FastAPI
- 🎨 Streamlit
- 🗄️ PostgreSQL
- 🧱 SQLAlchemy
- 🔄 Alembic
- 📄 ReportLab
- 🐳 Docker & Docker Compose
- 📊 LangSmith

The user provides a destination, dates, duration, travelers, budget, and preferences. The system researches relevant travel information, combines the results, generates a structured travel plan, stores the trip in PostgreSQL, and provides a downloadable PDF.

---

# 🎯 Project Objectives

- 🤖 Build a practical Agentic AI application
- 🧠 Implement LangGraph-based workflow orchestration
- 🔌 Implement MCP server and client communication
- 🌐 Integrate real-world APIs
- 🗺️ Research travel destinations
- 🏨 Search accommodations
- 🎯 Search activities and attractions
- 🍽️ Search restaurants
- 🌦️ Retrieve weather information
- 💰 Consider travel budget
- 📅 Consider dates and duration
- 🗄️ Persist trips using PostgreSQL
- 🔄 Manage schema migrations with Alembic
- 🚀 Build a FastAPI backend
- 🎨 Build an interactive Streamlit interface
- 📄 Generate downloadable PDF travel plans
- 🐳 Containerize the complete application
- 🧪 Test individual tools and MCP calls

---

# 🏗️ System Architecture

```text
                         👤 USER
                           │
                           ▼
                  🎨 STREAMLIT UI
                           │
                           │ HTTP
                           ▼
                     🚀 FASTAPI
                           │
                           ▼
                    🧠 LANGGRAPH
                           │
             ┌─────────────┼─────────────┐
             │             │             │
             ▼             ▼             ▼
       🗺️ Destination   🏨 Hotels     🎯 Activities
          Research        Search          Search
             │             │             │
             └─────────────┼─────────────┘
                           │
                 ┌─────────┴─────────┐
                 │                   │
                 ▼                   ▼
            🍽️ Restaurants       🌦️ Weather
                 │                   │
                 └─────────┬─────────┘
                           │
                           ▼
                      🔌 MCP SERVER
                           │
                           ▼
                       🛠️ TOOLS
                           │
             ┌─────────────┼─────────────┐
             ▼             ▼             ▼
          Tavily         SerpApi      Weather API
             │             │             │
             └─────────────┼─────────────┘
                           │
                           ▼
                     🧠 LLM REASONING
                           │
                           ▼
                    📋 TRAVEL PLAN
                           │
                  ┌────────┴────────┐
                  ▼                 ▼
            🗄️ PostgreSQL       📄 PDF
                  │                 │
                  └────────┬────────┘
                           ▼
                         👤 USER
```

---

# 🔄 End-to-End Workflow

```text
1️⃣ User enters travel requirements
              ↓
2️⃣ Streamlit sends request to FastAPI
              ↓
3️⃣ FastAPI validates the request
              ↓
4️⃣ Trip record is created
              ↓
5️⃣ LangGraph workflow starts
              ↓
6️⃣ Travel research tools are executed
              ↓
7️⃣ MCP server exposes and executes tools
              ↓
8️⃣ External APIs return travel information
              ↓
9️⃣ Results are aggregated
              ↓
🔟 LLM generates personalized travel plan
              ↓
1️⃣1️⃣ Travel plan is persisted
              ↓
1️⃣2️⃣ API returns the completed plan
              ↓
1️⃣3️⃣ Streamlit displays the itinerary
              ↓
1️⃣4️⃣ ReportLab generates the PDF
              ↓
1️⃣5️⃣ User downloads the travel plan
```

---

# 🤖 Agentic AI Architecture

Instead of using a single large function, the system separates travel research responsibilities into specialized capabilities.

```text
                    🧠 TRAVEL PLANNER
                           │
          ┌────────────────┼────────────────┐
          │                │                │
          ▼                ▼                ▼
     🗺️ Destination    🏨 Accommodation  🎯 Activities
        Research            Search          Search
          │                │                │
          └────────────────┼────────────────┘
                           │
                 ┌─────────┴─────────┐
                 ▼                   ▼
            🍽️ Restaurants       🌦️ Weather
                 │                   │
                 └─────────┬─────────┘
                           ▼
                    🧠 PLAN SYNTHESIS
                           │
                           ▼
                     📋 ITINERARY
```

This modular design makes the system easier to test, maintain, debug, and extend.

---

# 🔌 Model Context Protocol (MCP)

MCP provides the tool communication layer between the application and the travel tools.

```text
                 🧠 APPLICATION
                       │
                       ▼
                  🔌 MCP CLIENT
                       │
                       ▼
                  🔌 MCP SERVER
                       │
       ┌───────────────┼────────────────┐
       │               │                │
       ▼               ▼                ▼
destination_research accommodation   activity_search
                       │
              ┌────────┴────────┐
              ▼                 ▼
       restaurant_search   weather_search
              │                 │
              └────────┬────────┘
                       ▼
                 External APIs
```

## 🛠️ MCP Tools

| Tool | Purpose |
|---|---|
| 🗺️ `destination_research` | Research destination information |
| 🏨 `accommodation_search` | Search accommodation options |
| 🎯 `activity_search` | Search attractions and activities |
| 🌦️ `weather_search` | Retrieve weather information |
| 🍽️ `restaurant_search` | Search restaurants |

---

# 🗺️ Destination Research

Destination research uses web search to gather information relevant to the requested destination and user preferences.

### Example Input

```text
Destination: Goa
Preferences:
- Beaches
- Food
- Relaxation
```

### Technology

- 🔎 Tavily
- 🧠 LLM
- 🔌 MCP

---

# 🏨 Accommodation Search

Accommodation search uses **SerpApi Google Hotels**.

### Inputs

```text
📍 Destination
📅 Travel dates
⏱️ Duration
👥 Travelers
💰 Budget
❤️ Preferences
```

### Example Output

```text
🏨 OYO Aym Yoga Resort
💰 ₹519/night
⭐ 4.1

🏨 SanRit Hotel
💰 ₹533/night
⭐ 3.3

🏨 Om Ganesh Naik Guest House
💰 ₹614/night
⭐ 4.1
```

Structured accommodation data includes:

- Name
- Area
- Price per night
- Rating
- Description

---

# 🎯 Activity Search

Activity search uses **SerpApi Google Maps**.

Example results may include:

```text
📍 Velsao Beach
📍 Butterfly Beach Goa
📍 Bhagwan Mahavir Wildlife Sanctuary
📍 Big Foot Goa
📍 Bondla Wildlife Sanctuary
📍 Honeymoon Beach
📍 Abyss
📍 Japanese Garden
```

Structured fields:

- 🎯 Name
- 📍 Location
- 🏷️ Category
- 💰 Estimated cost
- ⏱️ Duration
- 📝 Description

---

# 🍽️ Restaurant Search

Restaurant search uses **SerpApi Google Maps**.

Example:

```text
🍽️ The Black Sheep Bistro
⭐ 4.6

🍽️ The Fishermans Wharf
⭐ 4.5

🍽️ The Coastal Tawa
⭐ 4.7

🍽️ Pickled Mango
⭐ 4.9

🍽️ The Lazy Goose
⭐ 4.4
```

Structured fields:

- Name
- Location
- Category
- Price level
- Rating
- Distance
- Description

---

# 🌦️ Weather Search

Weather information is retrieved for the requested destination and duration.

Example:

```text
📅 2026-09-16
🌡️ 27.0°C
🌧️ Patchy rain nearby
🌧️ Rain probability: 80%
💧 Precipitation: 6.11 mm
💨 Max wind: 16.9 km/h
```

Structured weather fields:

- Date
- Temperature
- Maximum temperature
- Minimum temperature
- Condition
- Rain probability
- Precipitation
- Maximum wind

Weather information can help the planning workflow make more suitable itinerary recommendations.

---

# 🧠 LangGraph Workflow

LangGraph provides graph-based orchestration for the travel-planning process.

Conceptually:

```text
                  START
                    │
                    ▼
             📥 USER REQUEST
                    │
                    ▼
             🧠 PLANNING STATE
                    │
       ┌────────────┼────────────┐
       ▼            ▼            ▼
   🗺️ Research   🏨 Hotels   🎯 Activities
       │            │            │
       └────────────┼────────────┘
                    │
              ┌─────┴─────┐
              ▼           ▼
          🍽️ Food      🌦️ Weather
              │           │
              └─────┬─────┘
                    ▼
             🧠 SYNTHESIS
                    │
                    ▼
              📋 TRAVEL PLAN
                    │
                    ▼
                   END
```

The graph-based approach makes complex workflows easier to represent and extend.

---

# 🚀 FastAPI Backend

FastAPI provides the backend API.

Core responsibilities include:

- 📥 Receiving travel requests
- ✅ Request validation
- 🧠 Starting the planning workflow
- 🗄️ Persisting trip data
- 📋 Returning generated travel plans
- 📄 Returning PDF documents
- 📚 Providing API documentation

### Important Endpoints

```text
GET  /
POST /plan
GET  /trips
GET  /trips/{trip_id}/pdf
```

FastAPI documentation is available through:

```text
http://localhost:8000/docs
```

---

# 🎨 Streamlit Interface

Streamlit provides the user-facing application.

The interface allows users to specify:

- 📍 Destination
- 📅 Travel dates
- ⏱️ Duration
- 👥 Travelers
- 💰 Budget
- ❤️ Preferences

After generation, the UI displays the travel plan and provides a PDF download button.

---

# 📄 PDF Generation

The project uses **ReportLab 5.0.1**.

```text
📋 Travel Plan
      │
      ▼
🚀 FastAPI PDF Endpoint
      │
      ▼
📄 ReportLab
      │
      ▼
📦 PDF Bytes
      │
      ▼
🎨 Streamlit
      │
      ▼
⬇️ Download Travel Plan PDF
```

PDF endpoint:

```text
GET /trips/{trip_id}/pdf
```

The API returns:

```text
Content-Type: application/pdf
```

---

# 🗄️ PostgreSQL Database

PostgreSQL is used for persistent trip storage.

```text
                🚀 FastAPI
                    │
                    ▼
               SQLAlchemy
                    │
                    ▼
               PostgreSQL
                    │
          ┌─────────┴─────────┐
          ▼                   ▼
       🧳 Trips          📋 Travel Plans
```

The application stores generated trip information including destination, dates, duration, travelers, budget, preferences, and status.

---

# 🔄 Alembic Migrations

Alembic manages database schema changes.

```text
SQLAlchemy Models
       │
       ▼
Alembic Migration
       │
       ▼
Migration Revision
       │
       ▼
PostgreSQL
```

Run:

```powershell
docker compose exec api alembic upgrade head
```

Check:

```powershell
docker compose exec api alembic current
```

---

# 🐳 Docker Architecture

The project is fully containerized using Docker Compose.

```text
                 🐳 DOCKER COMPOSE
                        │
       ┌────────────────┼────────────────┐
       │                │                │
       ▼                ▼                ▼
   🚀 API          🎨 STREAMLIT      🗄️ POSTGRES
   :8000              :8501             :5432
       │                │
       └─────────┬──────┘
                 ▼
             APPLICATION
```

## Services

| Service | Purpose | Port |
|---|---|---:|
| `api` | FastAPI backend | 8000 |
| `streamlit` | Streamlit UI | 8501 |
| `db` | PostgreSQL database | 5432 |

---

# 📁 Project Structure

```text
ai-travel-planner/
│
├── 📁 src/
│   ├── 📁 agents/
│   │   └── ...
│   │
│   ├── 📁 api/
│   │   └── main.py
│   │
│   ├── 📁 database/
│   │   ├── models.py
│   │   ├── session.py
│   │   └── ...
│   │
│   ├── 📁 graph/
│   │   └── ...
│   │
│   ├── 📁 mcp_server/
│   │   ├── travel_server.py
│   │   ├── client.py
│   │   └── mcp_client.py
│   │
│   └── 📁 tools/
│       ├── destination.py
│       ├── accommodation.py
│       ├── activity.py
│       ├── weather.py
│       └── food.py
│
├── 📁 alembic/
│   ├── versions/
│   └── ...
│
├── 📁 streamlit_app/
│   └── app.py
│
├── 📄 Dockerfile
├── 📄 docker-compose.yml
├── 📄 .dockerignore
├── 📄 requirements.txt
├── 📄 alembic.ini
├── 📄 .env
├── 📄 .gitignore
└── 📄 README.md
```

---

# 🛠️ Technology Stack

| Category | Technology |
|---|---|
| 🐍 Programming Language | Python 3.11+ |
| 🧠 Agent Orchestration | LangGraph |
| 🔗 LLM Framework | LangChain |
| 🤖 LLM | Google Gemini |
| 🔌 Agent Protocol | MCP |
| 🔎 Web Research | Tavily |
| 🗺️ Real-World Search | SerpApi |
| 🚀 Backend | FastAPI |
| 🎨 UI | Streamlit |
| 🗄️ Database | PostgreSQL 16 |
| 🧱 ORM | SQLAlchemy |
| 🔄 Migrations | Alembic |
| 📄 PDF | ReportLab 5.0.1 |
| 🐳 Containerization | Docker / Docker Compose |
| 📊 Observability | LangSmith |
| 🔀 Version Control | Git / GitHub |

---

# 📦 Requirements

The project uses the following primary dependencies:

```text
langgraph
langchain
langchain-google-genai
python-dotenv
pydantic
requests
tavily-python
fastapi
uvicorn
mcp[cli]
langsmith
sqlalchemy
psycopg[binary]
alembic
streamlit==1.63.0
reportlab==5.0.1
```

---

# 🔐 Environment Variables

Create a `.env` file in the project root.

Example:

```text
GOOGLE_API_KEY=your_google_api_key
TAVILY_API_KEY=your_tavily_api_key
SERPAPI_API_KEY=your_serpapi_api_key
LANGCHAIN_API_KEY=your_langsmith_api_key
LANGCHAIN_TRACING_V2=true
LANGCHAIN_PROJECT=ai-travel-planner
```

⚠️ Never commit API keys to GitHub.

---

# ⚙️ Local Installation

## 1️⃣ Clone the Repository

```powershell
git clone https://github.com/Musharraf-Bubere/ai-travel-planner.git
cd ai-travel-planner
```

## 2️⃣ Create Virtual Environment

```powershell
python -m venv venv
```

## 3️⃣ Activate Virtual Environment

```powershell
.env\Scripts\Activate.ps1
```

## 4️⃣ Install Dependencies

```powershell
pip install -r requirements.txt
```

## 5️⃣ Configure `.env`

Add the required API credentials.

---

# 🐳 Docker Installation

## 1️⃣ Build Images

```powershell
docker compose build
```

## 2️⃣ Start Services

```powershell
docker compose up -d
```

## 3️⃣ Verify Containers

```powershell
docker compose ps
```

Expected services:

```text
ai-travel-planner-api
ai-travel-planner-streamlit
ai-travel-planner-db
```

---

# 🗄️ Initialize Database

Run:

```powershell
docker compose exec api alembic upgrade head
```

Verify:

```powershell
docker compose exec api alembic current
```

---

# 🌐 Access the Application

### 🎨 Streamlit

```text
http://localhost:8501
```

### 🚀 FastAPI

```text
http://localhost:8000
```

### 📚 Swagger API Documentation

```text
http://localhost:8000/docs
```

---

# 🧪 Testing

Individual tools can be tested directly from the API container.

## 🍽️ Restaurant Search

```powershell
docker compose exec api python -c "from src.tools.food import search_restaurants; print(search_restaurants.invoke({'destination':'Goa','price_level':2,'limit':5}))"
```

## 🏨 Accommodation Search

```powershell
docker compose exec api python -c "from src.tools.accommodation import search_accommodations; print(search_accommodations.invoke({'destination':'Goa','travel_dates':'2026-10-10 to 2026-10-13','duration':3,'travelers':2,'budget':30000,'preferences':['beaches','food','relaxation']}))"
```

## 🎯 Activity Search

```powershell
docker compose exec api python -c "from src.tools.activity import search_activities; print(search_activities.invoke({'destination':'Goa','preferences':['beaches','food','relaxation'],'limit':8}))"
```

## 🌦️ Weather Search

```powershell
docker compose exec api python -c "from src.tools.weather import search_weather; print(search_weather.invoke({'destination':'Goa','duration':3}))"
```

---

# 🔌 Testing MCP

The reusable MCP client can execute MCP tools.

Example:

```powershell
docker compose exec api python -c "from src.mcp_server.client import call_mcp_tool; print(call_mcp_tool('restaurant_search', {'destination':'Goa','price_level':2,'limit':5}))"
```

MCP execution flow:

```text
Python Caller
     │
     ▼
TravelMCPClient
     │
     ▼
MCP Client
     │
     ▼
MCP Server
     │
     ▼
restaurant_search
     │
     ▼
search_restaurants
     │
     ▼
SerpApi
     │
     ▼
Structured Result
```

---

# 🩺 Debugging Commands

## Check Services

```powershell
docker compose ps
```

## API Logs

```powershell
docker compose logs api --tail=50
```

## Streamlit Logs

```powershell
docker compose logs streamlit --tail=50
```

## Database Logs

```powershell
docker compose logs db --tail=50
```

## Follow API Logs

```powershell
docker compose logs -f api
```

## Enter API Container

```powershell
docker compose exec api sh
```

---

# 🧳 Trip Persistence

Trips are stored in PostgreSQL.

Example:

```text
{
  "id": 9,
  "destination": "Goa",
  "travel_dates": "2026-09-19 to 2026-09-22",
  "duration": 3,
  "travelers": 2,
  "budget": 30000.0,
  "preferences": [
    "beaches",
    "food",
    "relaxation"
  ],
  "status": "completed"
}
```

Trips can be retrieved through:

```text
GET /trips
```

---

# 📄 PDF API

A generated travel plan can be returned as a PDF:

```text
GET /trips/{trip_id}/pdf
```

Example:

```text
GET http://localhost:8000/trips/9/pdf
```

Expected response:

```text
HTTP 200
Content-Type: application/pdf
```

The Streamlit interface uses the endpoint to provide:

```text
📄 Download Travel Plan PDF
```

---

# 🔐 Security

Basic security practices include:

- 🔑 API keys stored in environment variables
- 🚫 Secrets excluded from Git
- 🐳 Docker service isolation
- 🗄️ Database configuration through environment variables
- 🧹 External API failures handled at tool level

For production deployment, consider:

- 🔐 Authentication
- 🛡️ Authorization
- 🚦 Rate limiting
- 🔒 HTTPS
- 🧹 Strong input validation
- 🔑 Dedicated secret management
- 📊 Structured logging
- 🔄 Retry and fallback mechanisms

---

# 📊 LangSmith Observability

LangSmith can be used to observe LLM and agent execution.

```text
User Request
     │
     ▼
LangGraph
     │
     ├── LLM Call
     ├── MCP Call
     ├── Tool Call
     └── Workflow Execution
             │
             ▼
        📊 LangSmith
             │
             ▼
      Tracing / Debugging
```

This helps with:

- 🔍 Debugging
- ⏱️ Execution analysis
- 🧠 LLM tracing
- 🛠️ Tool-call inspection
- 📈 Workflow observability

---

# 🐳 Useful Docker Commands

### Start

```powershell
docker compose up -d
```

### Stop

```powershell
docker compose down
```

### Build

```powershell
docker compose build
```

### Rebuild API

```powershell
docker compose build api
```

### Rebuild Streamlit

```powershell
docker compose build streamlit
```

### Restart Streamlit

```powershell
docker compose up -d streamlit
```

### Logs

```powershell
docker compose logs
```

### API Shell

```powershell
docker compose exec api sh
```

---

# 🔄 Development Workflow

The project follows this development cycle:

```text
🧠 Understand
      ↓
🔎 Research
      ↓
📝 Document Research
      ↓
📚 Learn Required Concept
      ↓
💻 Implement
      ↓
🧪 Test
      ↓
♻️ Refactor
      ↓
📝 Document
      ↓
🔀 Git
      ↓
☁️ GitHub
```

---

# 🧠 Engineering Concepts Demonstrated

## 🤖 Artificial Intelligence

- Agentic AI
- LLM applications
- Tool calling
- Multi-step reasoning
- Workflow orchestration

## 🧠 LangGraph

- Graph workflows
- State
- Nodes
- Edges
- Agent orchestration

## 🔌 MCP

- MCP server
- MCP client
- Tool registration
- Tool execution
- Stdio transport

## 🌐 API Engineering

- REST APIs
- External API integration
- API authentication
- JSON processing
- Error handling

## 🗄️ Database Engineering

- PostgreSQL
- SQLAlchemy
- ORM
- Database models
- Alembic
- Schema migrations

## 🚀 Backend Engineering

- FastAPI
- Request validation
- API endpoints
- Service integration
- PDF responses

## 🎨 Application UI

- Streamlit
- Forms
- Session state
- API integration
- File downloads

## 🐳 DevOps

- Docker
- Dockerfile
- Docker Compose
- Container networking
- Environment configuration

---

# 📈 Example Use Case

### 👤 User Request

```text
📍 Destination: Goa
📅 Dates: 2026-09-19 to 2026-09-22
⏱️ Duration: 3 days
👥 Travelers: 2
💰 Budget: ₹30,000
❤️ Preferences:
   - Beaches
   - Food
   - Relaxation
```

### 🤖 System Processing

```text
             👤 USER
                │
                ▼
        📥 Request Validation
                │
                ▼
          🧠 LangGraph
                │
       ┌────────┼────────┐
       ▼        ▼        ▼
     🗺️       🏨       🎯
   Research   Hotels  Activities
       │        │        │
       └────────┼────────┘
                │
          ┌─────┴─────┐
          ▼           ▼
        🍽️          🌦️
     Restaurants   Weather
          │           │
          └─────┬─────┘
                ▼
         🧠 LLM Synthesis
                │
                ▼
          📋 TRAVEL PLAN
                │
       ┌────────┴────────┐
       ▼                 ▼
  🗄️ PostgreSQL       📄 PDF
       │                 │
       └────────┬────────┘
                ▼
             👤 USER
```

---

# 🏆 Project Highlights

```text
⭐ Agentic AI
⭐ LangGraph
⭐ MCP
⭐ Specialized travel tools
⭐ Tavily web research
⭐ SerpApi Google Hotels
⭐ SerpApi Google Maps
⭐ Weather integration
⭐ PostgreSQL
⭐ SQLAlchemy
⭐ Alembic
⭐ FastAPI
⭐ Streamlit
⭐ ReportLab PDF
⭐ Docker Compose
⭐ LangSmith
⭐ Git
⭐ GitHub
```

---

# 🚧 Future Improvements

Potential future enhancements:

- 🤖 Additional specialized agents
- 🗺️ Route optimization
- 🚗 Transportation planning
- ✈️ Flight search
- 🏨 Advanced hotel ranking
- 🍽️ Personalized restaurant ranking
- 🌦️ Weather-aware itinerary adaptation
- 💰 More advanced budget optimization
- 👤 User accounts
- 🔐 Authentication
- 📊 User dashboard
- 🧪 Automated test suite
- 🔄 Retry mechanisms
- ⚡ Caching
- 🚀 CI/CD
- ☁️ Cloud deployment
- 📈 Advanced observability

---

# 📌 Project Status

## 🟢 Working Prototype

Implemented:

- [x] 🤖 Agentic travel-planning foundation
- [x] 🧠 LangGraph workflow
- [x] 🔌 MCP server
- [x] 🔌 MCP client
- [x] 🗺️ Destination research
- [x] 🏨 Accommodation search
- [x] 🎯 Activity search
- [x] 🍽️ Restaurant search
- [x] 🌦️ Weather search
- [x] 🚀 FastAPI backend
- [x] 🎨 Streamlit UI
- [x] 🗄️ PostgreSQL database
- [x] 🧱 SQLAlchemy
- [x] 🔄 Alembic migrations
- [x] 📄 ReportLab PDF generation
- [x] ⬇️ PDF download
- [x] 🐳 Docker Compose
- [x] 🧪 Individual tool testing
- [x] 🔌 MCP tool testing
- [x] 📦 Dependency management
- [x] 🔀 Git version control
- [x] ☁️ GitHub repository

---

# 👨‍💻 Author

## Musharraf Bubere

🎓 Master's in Data Science, Analytics & AI

### Areas of Interest

- 🤖 Artificial Intelligence
- 🧠 Machine Learning
- 🔗 Generative AI
- 🧩 Agentic AI
- 📊 Data Science
- 🐍 Python
- 🗄️ SQL

---

# 🔗 GitHub Repository

https://github.com/Musharraf-Bubere/ai-travel-planner

---

# ⭐ Support the Project

If you find this project useful:

⭐ Star the repository  
🍴 Fork the repository  
💬 Share feedback  
🚀 Build your own Agentic AI application

---

# 📜 License

This project is intended for educational and portfolio purposes.

Review the licenses and terms of use of all external APIs and third-party services before commercial deployment.

---

<p align="center">
  <b>✈️ Plan smarter. Travel better. Powered by Agentic AI. 🤖</b>
</p>
