# ✈️ AI Travel Planner — Multi-Agent Travel Planning System

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.14-blue?style=for-the-badge&logo=python" alt="Python">
  <img src="https://img.shields.io/badge/LangChain-Agentic%20AI-green?style=for-the-badge" alt="LangChain">
  <img src="https://img.shields.io/badge/LangGraph-Orchestration-orange?style=for-the-badge" alt="LangGraph">
  <img src="https://img.shields.io/badge/FastAPI-Backend-009688?style=for-the-badge&logo=fastapi" alt="FastAPI">
  <img src="https://img.shields.io/badge/Streamlit-UI-FF4B4B?style=for-the-badge&logo=streamlit" alt="Streamlit">
  <img src="https://img.shields.io/badge/Pydantic-Structured%20Output-E92063?style=for-the-badge" alt="Pydantic">
</p>

<p align="center">
  <b>A practical Multi-Agent AI system that researches destinations, accommodations, activities, weather, and restaurants, then generates, validates, and iteratively refines a personalized travel itinerary.</b>
</p>

---

## 📌 Table of Contents

- [🌍 Overview](#-overview)
- [🎯 Project Goals](#-project-goals)
- [✨ Key Features](#-key-features)
- [🤖 Multi-Agent Architecture](#-multi-agent-architecture)
- [🔄 Workflow Architecture](#-workflow-architecture)
- [🧩 Workflow Patterns](#-workflow-patterns)
- [🧠 Why Multi-Agent Architecture](#-why-multi-agent-architecture)
- [🔗 Shared State](#-shared-state)
- [🛠️ Technology Stack](#️-technology-stack)
- [🌐 External Tools and APIs](#-external-tools-and-apis)
- [📁 Project Structure](#-project-structure)
- [📦 Structured Outputs](#-structured-outputs)
- [🔧 Tool Calling](#-tool-calling)
- [🛡️ Validation and Refinement](#️-validation-and-refinement)
- [⚙️ Installation](#️-installation)
- [🔐 Environment Variables](#-environment-variables)
- [▶️ Running the Application](#️-running-the-application)
- [📡 API](#-api)
- [🖥️ Streamlit Interface](#️-streamlit-interface)
- [🧪 Testing](#-testing)
- [📊 Example Request](#-example-request)
- [🔍 Example Workflow](#-example-workflow)
- [💡 Engineering Decisions](#-engineering-decisions)
- [🚧 Future Improvements](#-future-improvements)
- [📚 Learning Outcomes](#-learning-outcomes)
- [👨‍💻 Author](#-author)

---

# 🌍 Overview

**AI Travel Planner** is an intermediate-level **Agentic AI project** designed to demonstrate how multiple specialized AI agents can work together to solve a real-world problem.

Instead of asking a single LLM to generate an entire trip plan from its internal knowledge, the system divides the planning process into specialized agents.

Each agent focuses on a particular responsibility such as:

- 📍 Destination research
- 🏨 Accommodation research
- 🏖️ Activity and attraction discovery
- 🌤️ Weather analysis
- 🍽️ Restaurant research
- 🗓️ Itinerary generation
- 🔍 Itinerary validation
- 🔄 Itinerary refinement
- 📝 Final response generation

The agents are coordinated using **LangGraph**, while external tools provide real-world travel information.

The final system combines:

**LLMs + Multi-Agent Architecture + Tool Calling + LangGraph + Structured Output + Validation + Iterative Refinement + FastAPI + Streamlit**

---

# 🎯 Project Goals

The main objective of this project is to build a practical and resume-worthy **Multi-Agent AI system** while demonstrating important Agentic AI engineering concepts.

### 🎯 Primary Goals

- 🤖 Build a real **Agentic AI application**
- 🧩 Implement a **Multi-Agent architecture**
- 🕸️ Use **LangGraph as the workflow orchestrator**
- 🔄 Demonstrate Sequential, Parallel, Conditional, and Iterative workflows
- 🔧 Integrate external tools and APIs
- 🌐 Perform real-world travel research
- 📦 Use Pydantic for structured LLM outputs
- 🛡️ Validate AI-generated itineraries
- 🔄 Automatically refine invalid itineraries
- 🧠 Maintain shared state between agents
- 🚀 Expose the planning system through FastAPI
- 🖥️ Provide a Streamlit interface
- 🧪 Build automated tests
- 🏗️ Follow modular software engineering practices

---

# ✨ Key Features

### 🤖 Multi-Agent Planning

The application uses specialized agents instead of a single monolithic prompt.

### 🔄 Hybrid LangGraph Workflow

The system combines four important workflow patterns:

- ➡️ Sequential Workflow
- ⚡ Parallel Workflow
- 🔀 Conditional Workflow
- 🔁 Iterative Workflow

### 🌐 Real-World Research

The system retrieves external travel information using:

- 🔎 Tavily
- 🏨 SerpApi Google Hotels
- 📍 SerpApi Google Maps
- 🌤️ WeatherAPI

### 📦 Structured AI Output

Pydantic models are used to define predictable schemas for agent outputs.

### 🛡️ Hybrid Validation

The itinerary is validated using:

- 🧠 LLM-based semantic validation
- ⚙️ Deterministic programmatic checks

### 🔁 Automatic Refinement

Invalid itineraries can be sent back through a refinement process and validated again.

### 🗺️ Geographic Coherence

The itinerary attempts to avoid unrealistic movement between geographically distant areas during the same day.

### 💰 Budget Awareness

The system considers the user's total budget when selecting accommodations, activities, and restaurants.

### ❤️ Preference-Aware Planning

Traveler preferences such as:

- Beaches
- Food
- Relaxation
- Adventure
- Culture

can influence the final itinerary.

### 🚀 FastAPI Backend

The complete planning workflow can be accessed through a REST API.

### 🖥️ Streamlit Interface

A user-friendly interface allows users to enter trip information and view the generated travel plan.

### 🧪 Automated Testing

The project includes tests for:

- Graph structure
- Workflow routing
- Geographic validation
- Duplicate detection
- Research grounding
- API validation

---

# 🤖 Multi-Agent Architecture

The system contains multiple specialized agents.

## 📍 1. Destination Agent

The Destination Agent researches the requested destination.

### Responsibilities

- 📖 Destination overview
- 📍 Recommended areas
- ⚠️ Travel considerations
- ❤️ Preference-based suggestions
- 🔎 External destination research

### Tool

**Tavily Search**

### Flow

    User Request
         ↓
    Destination Agent
         ↓
    Tavily Search
         ↓
    Destination Research
         ↓
    Structured Destination Analysis

---

## 🏨 2. Stay Agent

The Stay Agent researches accommodation options.

### Responsibilities

- 🏨 Find accommodation options
- 💰 Retrieve price information
- ⭐ Retrieve ratings
- 📍 Identify accommodation areas
- 💵 Assess accommodation against the budget

### Tool

**SerpApi Google Hotels**

### Flow

    Destination + Dates + Travelers
                  ↓
             Stay Agent
                  ↓
        Google Hotels Search
                  ↓
       Accommodation Results
                  ↓
        Structured Stay Analysis

---

## 🏖️ 3. Activity Agent

The Activity Agent searches for attractions and activities.

### Responsibilities

- 🏝️ Discover attractions
- 🎯 Find activities
- 📍 Retrieve locations
- 🏷️ Categorize activities
- ❤️ Match traveler preferences

### Tool

**SerpApi Google Maps**

### Flow

    Destination + Preferences
               ↓
         Activity Agent
               ↓
       Google Maps Search
               ↓
        Local Attractions
               ↓
      Structured Activity Data

---

## 🌤️ 4. Weather Agent

The Weather Agent retrieves and analyzes weather information.

### Responsibilities

- 🌡️ Weather information
- 🌧️ Weather conditions
- 📅 Travel-period considerations
- 🧳 Weather-aware planning

### Tool

**WeatherAPI.com**

### Flow

    Destination + Travel Dates
               ↓
         Weather Agent
               ↓
          WeatherAPI
               ↓
       Weather Information
               ↓
      Structured Weather Data

---

## 🍽️ 5. Food Agent

The Food Agent researches restaurants.

### Responsibilities

- 🍴 Find restaurants
- ⭐ Retrieve ratings
- 📍 Retrieve restaurant locations
- 🏷️ Identify restaurant categories
- 💰 Consider relative price levels
- ❤️ Provide dining recommendations

### Tool

**SerpApi Google Maps**

### Flow

    Destination
         ↓
      Food Agent
         ↓
    Google Maps Search
         ↓
    Restaurant Results
         ↓
  Structured Food Analysis

---

## 🗓️ 6. Itinerary Agent

The Itinerary Agent combines all researched information and generates the travel itinerary.

### Inputs

- 📍 Destination research
- 🏨 Accommodation research
- 🏖️ Activities
- 🌤️ Weather
- 🍽️ Restaurants
- 📅 Travel dates
- ⏱️ Duration
- 👥 Number of travelers
- 💰 Budget
- ❤️ Preferences

### Responsibilities

- 🗓️ Generate the requested number of days
- 📍 Use researched locations
- 🍽️ Use researched restaurants
- 🏨 Use researched accommodation
- 🗺️ Maintain geographic coherence
- 🌤️ Consider weather
- 💰 Consider budget
- ❤️ Align with preferences
- 🚫 Avoid unsupported facts
- 🚫 Avoid hallucinated places

---

## 🔍 7. Itinerary Validator

The Itinerary Validator checks whether the generated itinerary satisfies the system's requirements.

### Validation Areas

- 📅 Exact duration
- 📍 Geographic coherence
- 🔗 Research grounding
- 🔁 Duplicate places
- 🍽️ Duplicate restaurants
- 🏨 Accommodation grounding
- ❤️ Preference alignment
- 🌤️ Weather considerations
- 💰 Budget semantics
- 📋 Required fields

The validator combines:

**LLM semantic validation**

and

**Deterministic programmatic validation**

This hybrid approach makes the validation layer more reliable than depending entirely on an LLM.

---

## 🔄 8. Refine Itinerary Agent

If validation fails, the itinerary can be sent to the refinement agent.

### Responsibilities

- 🔧 Fix validation issues
- 🗺️ Correct geographic conflicts
- 🔁 Remove unnecessary duplicate places
- 📅 Correct missing days or time slots
- 🔗 Preserve research grounding
- ❤️ Preserve user preferences
- 🚫 Avoid inventing unsupported information

The refinement process is limited by a maximum number of validation attempts to prevent infinite loops.

---

## 📝 9. Final Response Agent

Once the itinerary passes validation, the Final Response Agent prepares the final response.

### Output Includes

- 📍 Destination
- 📝 Trip summary
- 🗓️ Day-by-day itinerary
- 🏨 Accommodation summary
- 🍽️ Food summary
- 💡 Travel tips

---

# 🔄 Workflow Architecture

The complete workflow is a hybrid LangGraph architecture.

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
    │  + Research Tool  │
    └─────────┬─────────┘
              │
              ▼
       Destination Data
              │
       ┌──────┼──────┐
       │      │      │
       ▼      ▼      ▼
     Stay   Activity Weather
     Agent    Agent    Agent
       │      │      │
       └──────┼──────┘
              │
        Parallel Join
              │
              ▼
         Food Agent
              │
              ▼
       Itinerary Agent
              │
              ▼
      Itinerary Validator
              │
         ┌────┴────┐
         │         │
       Valid     Invalid
         │         │
         │         ▼
         │    Refine Itinerary
         │         │
         │         └──────► Validator
         │
         ▼
    Final Response Agent
         │
         ▼
    Final Travel Plan
         │
         ▼
      Streamlit
         │
         ▼
        USER

---

# 🧩 Workflow Patterns

## ➡️ Sequential Workflow

Sequential execution is used when one component depends on another.

    Destination
         ↓
       Food
         ↓
     Itinerary
         ↓
     Validator
         ↓
    Final Response

The next step begins after the previous step produces the required information.

---

## ⚡ Parallel Workflow

Independent research tasks are executed in parallel.

    Destination
         │
    ┌────┼────┐
    ▼    ▼    ▼
   Stay Activity Weather
    │    │    │
    └────┼────┘
         ▼
       Food

The Stay, Activity, and Weather agents are independent after destination information becomes available.

This demonstrates parallel orchestration using LangGraph.

---

## 🔀 Conditional Workflow

The validator determines which path the workflow should follow.

    Itinerary
        ↓
    Validator
       /   \
      /     \
   Valid   Invalid
     │        │
     ▼        ▼
  Final     Refine
 Response     │
              ▼
          Validator

The graph dynamically chooses the next node based on validation results.

---

## 🔁 Iterative Workflow

Invalid itineraries can be repeatedly refined.

    Itinerary
        ↓
    Validator
        ↓
      Invalid
        ↓
      Refine
        ↓
    Validator
        ↓
      Invalid
        ↓
      Refine
        ↓
    Validator
        ↓
       Valid
        ↓
   Final Response

A maximum attempt limit prevents an infinite refinement loop.

---

# 🧠 Why Multi-Agent Architecture?

A single LLM prompt could potentially generate an entire travel plan, but that approach creates several problems.

### ❌ Monolithic Approach

    User
      ↓
    One Large LLM Prompt
      ↓
    Entire Travel Plan

Problems can include:

- Difficult debugging
- Difficult testing
- Large prompts
- Weak separation of responsibilities
- Harder tool integration
- Difficult future extension

### ✅ Multi-Agent Approach

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
    Itinerary Agent
           ↓
    Validator
           ↓
    Refiner
           ↓
    Final Response

### Advantages

- 🧩 Separation of concerns
- 🧪 Easier testing
- 🔧 Easier tool integration
- 🐛 Easier debugging
- 📈 Easier scalability
- 🔄 Better workflow control
- 🧠 Clear agent responsibilities

---

# 🔗 Shared State

LangGraph allows the agents to communicate through a shared state.

The project uses a `TravelState` structure containing user inputs and agent outputs.

### User Input

    destination
    travel_dates
    duration
    travelers
    budget
    preferences

### Agent Data

    destination_data
    stay_options
    activities
    weather
    restaurants

### Workflow Data

    itinerary
    validation
    validation_attempts
    final_response

### State Concept

    User Input
        ↓
    Shared TravelState
        ↓
    Agent 1
        ↓
    Updated State
        ↓
    Agent 2
        ↓
    Updated State
        ↓
    ...
        ↓
    Final State

This shared state makes it possible for downstream agents to use information generated by earlier agents.

---

# 🛠️ Technology Stack

| Category | Technology |
|---|---|
| 🐍 Programming Language | Python |
| 🤖 LLM | Google Gemini |
| 🧠 Agent Framework | LangChain |
| 🕸️ Workflow Orchestration | LangGraph |
| 📦 Structured Output | Pydantic |
| 🔎 Destination Research | Tavily |
| 🏨 Accommodation Search | SerpApi Google Hotels |
| 📍 Activity Search | SerpApi Google Maps |
| 🍽️ Restaurant Search | SerpApi Google Maps |
| 🌤️ Weather | WeatherAPI.com |
| 🚀 Backend | FastAPI |
| 🖥️ UI | Streamlit |
| 🧪 Testing | pytest |
| 🌐 HTTP Client | Requests |
| 🔐 Configuration | python-dotenv |
| 🌿 Version Control | Git |
| ☁️ Repository | GitHub |

---

# 🌐 External Tools and APIs

## 🔎 Tavily

Used for destination research.

The Destination Agent sends a research query and receives relevant web results.

### Used For

- Destination overview
- Recommended areas
- Attractions
- Travel considerations
- Preference-based research

---

## 🏨 SerpApi Google Hotels

Used by the Stay Agent.

### Used For

- Accommodation discovery
- Hotel prices
- Hotel ratings
- Hotel areas
- Travel-date-aware hotel searches

---

## 📍 SerpApi Google Maps

Used by both the Activity Agent and Food Agent.

### Activity Agent

Used for:

- Attractions
- Beaches
- Activities
- Experiences
- Local places

### Food Agent

Used for:

- Restaurants
- Ratings
- Locations
- Categories
- Relative price levels

---

## 🌤️ WeatherAPI

Used by the Weather Agent to retrieve weather information relevant to the trip.

---

# 📁 Project Structure

    ai-travel-planner/
    │
    ├── 📁 src/
    │   │
    │   ├── 📁 agents/
    │   │   ├── destination.py
    │   │   ├── stay.py
    │   │   ├── activity.py
    │   │   ├── weather.py
    │   │   ├── food.py
    │   │   ├── itinerary.py
    │   │   ├── itinerary_validator.py
    │   │   ├── refine_itinerary.py
    │   │   └── final_response.py
    │   │
    │   ├── 📁 api/
    │   │   ├── __init__.py
    │   │   ├── main.py
    │   │   └── schemas.py
    │   │
    │   ├── 📁 graph/
    │   │   └── travel_graph.py
    │   │
    │   ├── 📁 schemas/
    │   │   ├── destination.py
    │   │   ├── stay.py
    │   │   ├── activity.py
    │   │   ├── weather.py
    │   │   ├── food.py
    │   │   ├── itinerary.py
    │   │   ├── validation.py
    │   │   └── final_response.py
    │   │
    │   ├── 📁 services/
    │   │   └── llm.py
    │   │
    │   ├── 📁 tools/
    │   │   ├── destination.py
    │   │   ├── stay.py
    │   │   ├── activity.py
    │   │   ├── weather.py
    │   │   └── food.py
    │   │
    │   ├── 📁 utils/
    │   │   └── itinerary_checks.py
    │   │
    │   ├── state.py
    │   └── main.py
    │
    ├── 📁 tests/
    │   ├── test_graph.py
    │   ├── test_itinerary_checks.py
    │   └── test_api.py
    │
    ├── 📁 streamlit_app/
    │   └── app.py
    │
    ├── 📄 .env
    ├── 📄 .gitignore
    ├── 📄 requirements.txt
    └── 📄 README.md

---

# 📦 Structured Outputs

The project uses Pydantic models to define structured outputs for agents.

## 📍 Destination Schema

    DestinationAnalysis
    ├── overview
    ├── recommended_areas
    ├── travel_considerations
    └── preference_suggestions

---

## 🏨 Accommodation Schema

    Accommodation
    ├── name
    ├── area
    ├── price_per_night
    ├── rating
    └── description

    StayAnalysis
    ├── recommended_area
    ├── accommodation_options
    ├── budget_assessment
    └── stay_recommendation

---

## 🏖️ Activity Schema

    Activity
    ├── name
    ├── location
    ├── category
    ├── estimated_cost
    ├── duration
    └── description

---

## 🍽️ Restaurant Schema

    Restaurant
    ├── name
    ├── location
    ├── category
    ├── price_level
    ├── rating
    ├── distance
    └── description

---

## 🔍 Validation Schema

    ItineraryValidation
    ├── is_valid
    ├── issues
    └── feedback

Structured outputs make the agent pipeline more predictable and easier to validate programmatically.

---

# 🔧 Tool Calling

The project uses an agent + tool-calling pattern.

### General Flow

    User Request
         ↓
       Agent
         ↓
      Tool Call
         ↓
    External API
         ↓
     Tool Result
         ↓
       Agent
         ↓
    Structured Output

This approach allows agents to obtain external information before producing their final response.

---

# 🛡️ Validation and Refinement

One of the important engineering aspects of this project is that the system does not blindly trust the first itinerary generated by the LLM.

The generated itinerary passes through a validation layer.

## 🧠 LLM Validation

The LLM evaluates semantic requirements such as:

- Preference alignment
- Budget reasoning
- Weather considerations
- Overall itinerary quality
- Grounding
- Logical planning

---

## ⚙️ Deterministic Validation

Programmatic checks are used for requirements that can be checked reliably using code.

Examples include:

- 📅 Exact number of days
- 🔁 Duplicate places
- 🍽️ Duplicate restaurants
- 🗺️ Geographic conflicts
- 🔗 Research grounding

---

## 🔄 Refinement Loop

If the itinerary fails:

    Generated Itinerary
           ↓
       Validation
           ↓
        Invalid
           ↓
        Refinement
           ↓
       Validation
           ↓
    ┌──────┴──────┐
    │             │
  Valid         Invalid
    │             │
    ▼             ▼
  Final        Refinement
 Response

The process stops when:

1. ✅ The itinerary becomes valid, or
2. 🛑 The maximum validation attempts are reached.

---

# 🗺️ Geographic Validation

Geographic coherence is treated as an important planning constraint.

For example, a short Goa trip should not unnecessarily move between distant regions during the same day.

The deterministic validation layer identifies geographic areas and checks for problematic combinations.

### Example

    Day 1
    ├── Arambol
    ├── Anjuna
    └── Baga

This is geographically more coherent than:

    Day 1
    ├── Arambol
    ├── Palolem
    └── Colva

The purpose is not to calculate exact driving times, but to prevent obviously incoherent geographic planning based on known location groupings.

---

# 🔁 Duplicate Detection

The validation system also detects repeated places.

Example:

    Day 1 → Sinquerim Beach
    Day 2 → Sinquerim Beach
    Day 3 → Sinquerim Beach

This can be flagged as an unnecessary repetition.

The refinement layer can then attempt to remove or replace the repeated occurrence using available researched information.

---

# 💰 Budget Semantics

The system treats budget information carefully.

For example:

- An accommodation price represents accommodation cost information.
- Restaurant `price_level` represents a relative pricing category, not an exact meal price.
- Activity `estimated_cost = 0.0` can mean price information is unavailable and should not automatically be interpreted as "free".

This distinction helps prevent the LLM from making unsupported financial claims.

---

# ⚙️ Installation

## 1️⃣ Clone the Repository

    git clone https://github.com/Musharraf-Bubere/ai-travel-planner.git

Move into the project:

    cd ai-travel-planner

---

## 2️⃣ Create a Virtual Environment

### Windows

    python -m venv venv

Activate the environment:

    venv\Scripts\activate

---

## 3️⃣ Install Dependencies

    pip install -r requirements.txt

---

# 🔐 Environment Variables

Create a `.env` file in the project root.

Required environment variables:

    GOOGLE_API_KEY=your_google_api_key
    WEATHER_API_KEY=your_weather_api_key
    SERPAPI_API_KEY=your_serpapi_api_key
    TAVILY_API_KEY=your_tavily_api_key

### 🔒 Security

Never commit your `.env` file to GitHub.

The project includes `.env` in `.gitignore`.

---

# ▶️ Running the Application

## 🚀 Start FastAPI

From the project root:

    uvicorn src.api.main:app --reload

The API will run at:

    http://127.0.0.1:8000

---

# ❤️ Health Check

Open:

    http://127.0.0.1:8000/health

Expected response:

    {
        "status": "healthy",
        "service": "AI Travel Planner API"
    }

---

# 📡 API

## POST `/plan`

The `/plan` endpoint runs the complete travel planning workflow.

### Request

    {
        "destination": "Goa",
        "travel_dates": "2026-10-10 to 2026-10-13",
        "duration": 3,
        "travelers": 2,
        "budget": 30000,
        "preferences": [
            "beaches",
            "food",
            "relaxation"
        ]
    }

### Request Fields

| Field | Type | Description |
|---|---|---|
| 📍 destination | string | Travel destination |
| 📅 travel_dates | string | Travel dates |
| ⏱️ duration | integer | Number of travel days |
| 👥 travelers | integer | Number of travelers |
| 💰 budget | float | Total trip budget |
| ❤️ preferences | list[string] | Traveler preferences |

---

# 🖥️ Streamlit Interface

The Streamlit application provides the user-facing interface.

### Features

- 📍 Destination input
- 📅 Travel dates
- ⏱️ Trip duration
- 👥 Number of travelers
- 💰 Budget
- ❤️ Travel preferences
- 🚀 Generate travel plan
- 🔄 Workflow progress
- 🗓️ Day-by-day itinerary
- 🏨 Accommodation information
- 🍽️ Restaurant information
- 🌤️ Weather information
- 🔍 Validation information
- 🔄 Refinement status

### Run Streamlit

    streamlit run streamlit_app/app.py

The application will open in the browser.

---

# 🧪 Testing

The project uses `pytest` for automated testing.

## Run All Tests

    python -m pytest -v

---

## Test Graph Structure

    python -m pytest tests/test_graph.py -v

The graph tests verify:

- 🕸️ Graph compilation
- ⚡ Parallel workflow structure
- 🔀 Conditional routing
- 🔁 Iterative routing
- 🛑 Maximum-attempt handling
- 📝 Final-response routing

---

## Test Itinerary Validation

    python -m pytest tests/test_itinerary_checks.py -v

These tests cover:

- 🗺️ Geographic classification
- 📍 Location extraction
- 🚨 Mixed geographic areas
- ✅ Same-area itineraries
- 🌍 Unknown destinations
- 🚗 Cross-region movement
- 🔁 Duplicate places
- 🍽️ Duplicate restaurants
- 🔗 Activity grounding

---

## Test FastAPI

    python -m pytest tests/test_api.py -v

API tests cover:

- ❤️ Health endpoint
- 📡 Valid planning requests
- ❌ Invalid requests
- 🧾 Missing fields
- 📝 Empty preferences
- ⚠️ Planning failures

---

# 📊 Example Request

Example travel request:

    Destination: Goa
    Travel Dates: 2026-10-10 to 2026-10-13
    Duration: 3 days
    Travelers: 2
    Budget: ₹30,000
    Preferences:
      - Beaches
      - Food
      - Relaxation

---

# 🔍 Example Workflow

A request enters the system:

    User
      │
      ▼
    FastAPI
      │
      ▼
    LangGraph
      │
      ▼
    Destination Research
      │
      ▼
    ┌──────────────┬──────────────┬──────────────┐
    │              │              │
    ▼              ▼              ▼
    Stay        Activities      Weather
    │              │              │
    └──────────────┴──────────────┘
                   │
                   ▼
                Food
                   │
                   ▼
              Itinerary
                   │
                   ▼
              Validator
                   │
              ┌────┴────┐
              │         │
            Valid     Invalid
              │         │
              │         ▼
              │      Refine
              │         │
              │         └──────► Validator
              │
              ▼
         Final Response
              │
              ▼
           Streamlit

---

# 🧠 Engineering Decisions

## 🧩 Separation of Responsibilities

Each agent has a clearly defined responsibility.

This makes the system easier to maintain and extend.

---

## 📦 Structured Output

Pydantic schemas are used instead of relying on unstructured text.

Benefits include:

- Better consistency
- Easier validation
- Easier downstream processing
- Clear contracts between components

---

## ⚡ Parallel Research

Stay, Activity, and Weather research can execute independently.

This makes the workflow more efficient than executing every research task sequentially.

---

## 🛡️ Hybrid Validation

The project intentionally combines LLM validation with deterministic validation.

LLMs are useful for semantic reasoning, while deterministic checks are better for exact rules.

---

## 🔄 Iterative Refinement

The system does not assume that the first LLM-generated itinerary is always correct.

Instead:

    Generate
       ↓
    Validate
       ↓
    Refine if needed
       ↓
    Validate Again

This demonstrates an important Agentic AI pattern.

---

## 🗺️ Geographic Coherence

Geographic consistency is treated as a planning constraint instead of simply asking the LLM to "make a good itinerary."

This reduces unrealistic travel schedules.

---

# 📈 Current Project Capabilities

The project currently demonstrates:

| Capability | Status |
|---|---|
| 🤖 Agentic AI | ✅ |
| 🧩 Multi-Agent Architecture | ✅ |
| 🕸️ LangGraph Orchestration | ✅ |
| ➡️ Sequential Workflow | ✅ |
| ⚡ Parallel Workflow | ✅ |
| 🔀 Conditional Workflow | ✅ |
| 🔁 Iterative Workflow | ✅ |
| 🔧 Tool Calling | ✅ |
| 🌐 External Travel APIs | ✅ |
| 📦 Pydantic Structured Output | ✅ |
| 🔍 Itinerary Validation | ✅ |
| 🔄 Itinerary Refinement | ✅ |
| 🛡️ Deterministic Validation | ✅ |
| 🚀 FastAPI Backend | ✅ |
| 🖥️ Streamlit Interface | ✅ |
| 🧪 Automated Testing | ✅ |
| 🌿 Git | ✅ |
| ☁️ GitHub | ✅ |
| 🔌 MCP Integration | 🚧 |
| 💾 Persistence | 🚧 |
| 🐳 Docker | 🚧 |
| ⚙️ CI/CD | 🚧 |
| ☁️ Deployment | 🚧 |

---

# 🚧 Future Improvements

The architecture is intentionally designed so additional capabilities can be added later.

## 🔌 MCP Integration

Convert selected external tools into MCP-based tools.

Potential integrations include:

- 🔎 Destination research
- 🏨 Hotel search
- 📍 Maps search
- 🍽️ Restaurant search
- 🌤️ Weather

---

## 💾 Persistence

Add persistent state storage so travel planning sessions can be stored and resumed.

Potential technologies:

- PostgreSQL
- SQLite
- LangGraph persistence/checkpointing

---

## 🐳 Docker

Containerize the backend and application.

Potential architecture:

    Docker
      │
      ├── FastAPI
      ├── Streamlit
      └── Supporting Services

---

## ⚙️ GitHub Actions

Add CI/CD workflows for:

- 🧪 Automated tests
- 🔍 Code quality checks
- 🏗️ Build validation
- 🚀 Deployment pipelines

---

## ☁️ Deployment

Deploy the application to a cloud platform.

Possible architecture:

    User
      ↓
    Cloud Frontend
      ↓
    FastAPI
      ↓
    LangGraph
      ↓
    External APIs

---

## 📊 Observability

Future versions can integrate tracing and monitoring for:

- Agent execution
- Tool calls
- Latency
- Token usage
- Errors
- Workflow paths
- Validation attempts

---

## 🧠 Advanced Agent Improvements

Potential future improvements include:

- Dynamic agent routing
- Better cost optimization
- More advanced geographic reasoning
- User feedback loops
- Travel preference learning
- Multi-destination planning
- Flight research
- Transportation planning
- Currency conversion
- Trip modification agents

---

# 📚 Learning Outcomes

This project provides practical experience with:

### 🤖 Agentic AI

- Agents
- Tool calling
- Multi-agent systems
- Agent responsibilities
- Agent coordination

### 🕸️ LangGraph

- Graphs
- Nodes
- Edges
- Shared state
- Sequential workflows
- Parallel workflows
- Conditional routing
- Iterative workflows

### 🧠 LangChain

- Chat models
- Tools
- Tool binding
- Structured output
- Messages

### 📦 Pydantic

- Data validation
- Structured schemas
- Typed application contracts

### 🌐 API Integration

- REST APIs
- External services
- HTTP requests
- API authentication
- JSON response handling

### 🚀 FastAPI

- REST endpoints
- Request validation
- Response models
- Error handling

### 🖥️ Streamlit

- Interactive UI
- Form handling
- Application state
- API integration
- Result visualization

### 🧪 Testing

- Unit testing
- API testing
- Workflow testing
- Deterministic validation testing

### 🏗️ Software Engineering

- Modular architecture
- Separation of concerns
- Environment configuration
- Error handling
- Git version control
- GitHub workflow

---

# 🎓 Project Level

**Intermediate Agentic AI Project**

This project is intentionally designed to be:

- More advanced than a basic chatbot
- More practical than a simple single-agent application
- Smaller and more focused than a large enterprise AI platform
- Strong enough to demonstrate real Agentic AI engineering concepts

---

# 💼 Resume-Relevant Skills Demonstrated

This project demonstrates practical experience with:

- Python
- LangChain
- LangGraph
- Agentic AI
- Multi-Agent Systems
- Tool Calling
- Structured Output
- Pydantic
- LLM Application Development
- REST APIs
- FastAPI
- Streamlit
- External API Integration
- Automated Testing
- Git
- GitHub
- Workflow Orchestration
- AI Validation
- Iterative AI Refinement

---

# 🏆 What Makes This Project Different?

The project is not simply:

    User → LLM → Travel Plan

Instead, it follows:

    User
      ↓
    Research
      ↓
    Specialized Agents
      ↓
    Parallel Information Gathering
      ↓
    Itinerary Generation
      ↓
    Semantic Validation
      ↓
    Deterministic Validation
      ↓
    Iterative Refinement
      ↓
    Final Response

This architecture demonstrates how LLMs can be combined with traditional software engineering to build more reliable AI systems.

---

# 📌 Important Design Principle

The system follows a core principle:

> **Use LLMs for reasoning and use deterministic code where rules can be reliably enforced.**

For example:

    LLM
    ├── Reason about preferences
    ├── Plan activities
    ├── Interpret weather
    └── Generate itinerary

    Deterministic Code
    ├── Check duplicate places
    ├── Check exact duration
    ├── Check geographic conflicts
    ├── Validate required fields
    └── Control iteration limits

This hybrid architecture improves reliability while still benefiting from LLM reasoning.

---

# 🔐 Security Notes

- 🔒 API keys are stored in environment variables.
- 🚫 `.env` should never be committed.
- 🔑 External API credentials should be rotated if exposed.
- 🧾 Sensitive information should not be logged.
- 🌐 Production deployments should use secure HTTPS endpoints.
- 🛡️ Production API authentication and rate limiting should be added before public deployment.

---

# 📜 License

This project is intended for educational, portfolio, and demonstration purposes.

---

# 👨‍💻 Author

## Musharraf Bubére

**Data Science & AI | Machine Learning | Generative AI | Agentic AI**

### 🔗 GitHub

Repository:

    https://github.com/Musharraf-Bubere/ai-travel-planner

---

# ⭐ Support

If you find this project useful or interesting:

- ⭐ Star the repository
- 🍴 Fork the project
- 🐛 Report issues
- 💡 Suggest improvements
- 🤝 Contribute ideas

---

# 🚀 Final Architecture Summary

    ┌─────────────────────────────────────────────────────┐
    │                    👤 USER                          │
    └─────────────────────────┬───────────────────────────┘
                              │
                              ▼
    ┌─────────────────────────────────────────────────────┐
    │                 🚀 FASTAPI                          │
    └─────────────────────────┬───────────────────────────┘
                              │
                              ▼
    ┌─────────────────────────────────────────────────────┐
    │              🕸️ LANGGRAPH                           │
    │                 ORCHESTRATOR                       │
    └─────────────────────────┬───────────────────────────┘
                              │
                              ▼
    ┌─────────────────────────────────────────────────────┐
    │             📍 DESTINATION AGENT                   │
    │                    + 🔎 TAVILY                      │
    └─────────────────────────┬───────────────────────────┘
                              │
              ┌───────────────┼────────────────┐
              │               │                │
              ▼               ▼                ▼
    ┌────────────────┐ ┌────────────────┐ ┌────────────────┐
    │ 🏨 STAY AGENT  │ │ 🏖️ ACTIVITY    │ │ 🌤️ WEATHER     │
    │                │ │    AGENT       │ │    AGENT       │
    │ SerpApi Hotels │ │ SerpApi Maps   │ │  WeatherAPI    │
    └───────┬────────┘ └───────┬────────┘ └───────┬────────┘
            │                  │                  │
            └──────────────────┼──────────────────┘
                               │
                               ▼
                    ┌────────────────────┐
                    │ 🍽️ FOOD AGENT      │
                    │  SerpApi Maps      │
                    └──────────┬─────────┘
                               │
                               ▼
                    ┌────────────────────┐
                    │ 🗓️ ITINERARY AGENT │
                    └──────────┬─────────┘
                               │
                               ▼
                    ┌────────────────────┐
                    │ 🔍 VALIDATOR       │
                    └──────────┬─────────┘
                               │
                       ┌───────┴────────┐
                       │                │
                       ▼                ▼
                    ✅ VALID          ❌ INVALID
                       │                │
                       │                ▼
                       │        🔄 REFINEMENT
                       │                │
                       │                └──────► 🔍 VALIDATOR
                       │
                       ▼
                ┌────────────────────┐
                │ 📝 FINAL RESPONSE  │
                └──────────┬─────────┘
                           │
                           ▼
                ┌────────────────────┐
                │ 🖥️ STREAMLIT UI    │
                └──────────┬─────────┘
                           │
                           ▼
                         👤 USER

---

## ⭐ AI Travel Planner

**Research → Multi-Agent Reasoning → Parallel Processing → Itinerary Generation → Validation → Iterative Refinement → Final Travel Plan**

Built with ❤️ using **Python, LangChain, LangGraph, Gemini, Pydantic, FastAPI, Streamlit, Tavily, SerpApi, and WeatherAPI**.
