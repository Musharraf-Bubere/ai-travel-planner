# ⚠️ Module 6: Technical Debt, Known Limitations & Architectural Trade-offs

> **Purpose**: This document provides a transparent, technically rigorous audit of all verified limitations, architectural debt, and design trade-offs in the AI Travel Planner codebase. 
> 
> *Interview Value*: Demonstrating deep self-awareness of your system's edge cases and being able to critique your own code with actionable engineering solutions is the hallmark of a Senior AI Engineer.

---

## 📑 Priority Summary Table

| ID | Priority | Category | Status | Summary of Issue |
|---|---|---|---|---|
| **LIM-01** | **P1 — High** | Reliability | **Confirmed** | `DATABASE_URL` evaluated at import time; crashes if missing. |
| **LIM-02** | **P1 — High** | DevOps | **Confirmed** | Docker Compose does not automatically run Alembic migrations. |
| **LIM-03** | **P1 — High** | Architecture | **Confirmed** | Geographic validation and repair logic is hardcoded exclusively for Goa. |
| **LIM-04** | **P1 — High** | Performance | **Confirmed** | MCP client spawns a new Python interpreter subprocess per tool call. |
| **LIM-05** | **P2 — Medium** | Correctness | **Confirmed** | Streamlit PDF download URL hardcoded to `http://api:8000`, breaking local dev. |
| **LIM-06** | **P2 — Medium** | Data Grounding | **Confirmed** | Missing Google Maps attraction prices are defaulted to `0.0` (false free). |
| **LIM-07** | **P2 — Medium** | Testing | **Confirmed** | Automated test suite invokes live external APIs (Gemini, SerpApi, WeatherAPI). |
| **LIM-08** | **P2 — Medium** | Testing | **Confirmed** | Persistence integration tests mutate the live database without rollback fixtures. |
| **LIM-09** | **P2 — Medium** | Security | **Confirmed** | API error handlers leak raw exception strings in HTTP 500 responses. |
| **LIM-10** | **P2 — Medium** | Architecture | **Confirmed** | `POST /plan` blocks synchronously for 30–90 seconds inside HTTP handler. |
| **LIM-11** | **P2 — Medium** | UI / Integration | **Confirmed** | Backend trip history endpoints (`/trips`) are disconnected from the UI. |
| **LIM-12** | **P2 — Medium** | Input Validation | **Confirmed** | `TravelRequest.travel_dates` lacks regex/order validation, causing downstream 500s. |
| **LIM-13** | **P2 — Medium** | Document Engine | **Confirmed** | ReportLab lacks XML escaping on dynamic strings and lacks non-ASCII font support. |
| **LIM-14** | **P2 — Medium** | Localization | **Confirmed** | Accommodation search forces INR currency and Indian locale (`gl="in"`) globally. |
| **LIM-15** | **P2 — Medium** | Resilience | **Confirmed** | External API tool calls lack exponential backoff retries on 429/5xx errors. |
| **LIM-16** | **P2 — Medium** | Security | **Confirmed** | API endpoints are completely unauthenticated. |
| **LIM-17** | **P2 — Medium** | Security | **Confirmed** | FastAPI lacks `CORSMiddleware`, blocking cross-origin browser clients. |
| **LIM-18** | **P3 — Low** | DevOps | **Confirmed** | Docker containers run as default `root` user without dropped capabilities. |
| **LIM-19** | **P3 — Low** | Observability | **Confirmed** | Zero application-level logging (`logging.getLogger`) configured in `src/`. |
| **LIM-20** | **P3 — Low** | Code Cleanliness | **Confirmed** | `src/services/pdf.py` is an unreferenced 644-line duplicate of `pdf_generator.py`. |
| **LIM-21** | **P3 — Low** | State Integrity | **Confirmed** | Trips reaching `validation_failed` are still marked `status="completed"` in DB. |
| **LIM-22** | **P3 — Low** | Orchestration | **Confirmed** | `food_agent` unnecessarily waits for `stay`, `activity`, and `weather` at barrier join. |
| **LIM-23** | **P3 — Low** | Performance | **Confirmed** | Research agents perform redundant Stage 1 tool-calling LLM invocations. |
| **LIM-24** | **P3 — Low** | Domain Logic | **Confirmed** | WeatherAPI free tier only supports 3 days; cannot forecast dates months in advance. |
| **LIM-25** | **P3 — Low** | Testing | **Confirmed** | Zero automated unit tests exist for MCP client or MCP server implementations. |

---

## 🔍 Detailed Analysis of All 25 Limitations

---

### [LIM-01] Import-Time `DATABASE_URL` Crash
- **Status**: **Confirmed**
- **Priority**: P1 — High
- **Verified Evidence**: [`src/database/connection.py`](../src/database/connection.py#L11-L16)
  ```python
  DATABASE_URL = os.getenv("DATABASE_URL")
  if not DATABASE_URL:
      raise ValueError("DATABASE_URL is not set in the environment.")
  engine = create_engine(DATABASE_URL, pool_pre_ping=True)
  ```
- **Practical Impact**: If an engineer clones the repository, configures API keys, but omits `DATABASE_URL`, executing `uvicorn src.api.main:app` or `pytest` immediately crashes with an unhandled `ValueError` at module import time before any application code executes.
- **Current Behavior**: Top-level code execution immediately raises `ValueError`.
- **Recommended Resolution**: Use a lazy connection getter, or provide a default fallback to a local SQLite database (`sqlite:///./local_travel.db`) when `DATABASE_URL` is omitted in development mode.
- **Relevant Module**: `src.database.connection`

---

### [LIM-02] Missing Automatic Database Migrations in Docker
- **Status**: **Confirmed**
- **Priority**: P1 — High
- **Verified Evidence**: [`docker-compose.yml`](../docker-compose.yml#L3-L16) & [`Dockerfile`](../Dockerfile#L16)
- **Practical Impact**: Running `docker compose up --build` starts PostgreSQL and launches Uvicorn. However, no command executes `alembic upgrade head`. The database starts completely empty. When a user calls `POST /plan`, the first SQL insert crashes with `psycopg.errors.UndefinedTable: relation "trips" does not exist`.
- **Current Behavior**: Requires manual intervention: `docker compose exec api alembic upgrade head`.
- **Recommended Resolution**: Create a `docker-entrypoint.sh` script that executes `alembic upgrade head` before running `uvicorn src.api.main:app`.
- **Relevant Module**: `docker-compose.yml`, `Dockerfile`

---

### [LIM-03] Goa-Specific Geographic Validation & Repair
- **Status**: **Confirmed**
- **Priority**: P1 — High
- **Verified Evidence**: [`src/utils/itinerary_checks.py`](../src/utils/itinerary_checks.py#L295-L296) & [`lines 568–569`](../src/utils/itinerary_checks.py#L568-L569)
  ```python
  if destination.lower().strip() != "goa":
      return []
  ...
  if destination.lower().strip() != "goa":
      return itinerary
  ```
- **Practical Impact**: Over 1,000 lines of regex checks, area classifications (`GOA_AREA_KEYWORDS`), and transit conflict repair routines are hardcoded exclusively for Goa. For all other destinations worldwide (Tokyo, Paris, New York, Manali), geographic checks return early and do not validate spatial clustering.
- **Current Behavior**: Silently passes all non-Goa itineraries without checking transit spread.
- **Recommended Resolution**: Extract latitude and longitude coordinates from SerpApi Google Maps results and compute pairwise Haversine distances to flag daily travel exceeding realistic thresholds (>35 km).
- **Relevant Module**: `src.utils.itinerary_checks`

---

### [LIM-04] Subprocess Creation Per MCP Tool Call
- **Status**: **Confirmed**
- **Priority**: P1 — High
- **Verified Evidence**: [`src/mcp_server/client.py`](../src/mcp_server/client.py#L23-L34)
  ```python
  async def call_tool(self, tool_name: str, arguments: dict[str, Any]) -> Any:
      async with Client(self.server_params) as client:
          result = await client.call_tool(tool_name, arguments)
  ```
- **Practical Impact**: Every tool call spawns a brand new `sys.executable` child process. Spawning Python and loading dependencies takes ~1 second per call. Across 5 research agents, 5–6 seconds is wasted purely on process initialization, causing severe CPU spikes.
- **Current Behavior**: Process starts, performs JSON-RPC handshake, calls tool, and exits.
- **Recommended Resolution**: Maintain a long-lived persistent MCP client session across the application lifetime, or use in-process FastMCP server / SSE transport.
- **Relevant Module**: `src.mcp_server.client`

---

### [LIM-05] Streamlit PDF Download URL Incompatible Outside Docker
- **Status**: **Confirmed**
- **Priority**: P2 — Medium
- **Verified Evidence**: [`streamlit_app/app.py`](../streamlit_app/app.py#L1624-L1626)
  ```python
  pdf_url = f"http://api:8000/trips/{trip_id}/pdf"
  ```
- **Practical Impact**: When running Streamlit on a local machine outside Docker (`streamlit run streamlit_app/app.py`), the host name `api` does not exist in local DNS. Clicking "Download Travel Plan PDF" catches `requests.RequestException` and displays `"PDF download is currently unavailable"`.
- **Current Behavior**: Completely ignores `API_URL` setting and hardcodes Docker network hostname `http://api:8000`.
- **Recommended Resolution**: Derive the PDF URL dynamically: `pdf_base = API_URL.rsplit('/', 1)[0]; pdf_url = f"{pdf_base}/trips/{trip_id}/pdf"`.
- **Relevant Module**: `streamlit_app.app`

---

### [LIM-06] Missing Attraction Prices Defaulted to Free (`0.0`)
- **Status**: **Confirmed**
- **Priority**: P2 — Medium
- **Verified Evidence**: [`src/tools/activity.py` line 75](file:///d:/ai-travel-planner/src/tools/activity.py#L75) & [`src/agents/activity_agent.py` line 53](file:///d:/ai-travel-planner/src/agents/activity_agent.py#L53)
  ```python
  # src/tools/activity.py: "estimated_cost": 0.0
  # src/agents/activity_agent.py: "4. If price information is unavailable, use 0.0."
  ```
- **Practical Impact**: SerpApi Google Maps `local_results` does not provide admission prices. The tool hardcodes cost as `0.0`, and the agent prompt instructs the model to use `0.0`. Paid attractions (scuba diving, museums, boat cruises) are presented to travelers as free, artificially deflating total trip expenses.
- **Current Behavior**: Numerical budget calculation treats unpriced activities as costing ₹0.
- **Recommended Resolution**: Use `estimated_cost: float | None = None` and display `"Admission fee not published"` in the UI and PDF.
- **Relevant Module**: `src.tools.activity`, `src.agents.activity_agent`

---

### [LIM-07] Live External API Calls in Automated Tests
- **Status**: **Confirmed**
- **Priority**: P2 — Medium
- **Verified Evidence**: [`tests/test_llm.py`](../tests/test_llm.py#L7), [`tests/test_accommodation_tool.py`](../tests/test_accommodation_tool.py#L5), [`tests/test_weather_agent.py`](../tests/test_weather_agent.py#L13), [`tests/test_food_agent.py`](../tests/test_food_agent.py#L13), [`tests/test_itinerary_agent.py`](../tests/test_itinerary_agent.py#L86)
- **Practical Impact**: Running `pytest` makes real network requests to Google Gemini, SerpApi, and WeatherAPI. Tests fail in offline environments, fail if API keys expire, consume paid API credits, and suffer from external network flakiness.
- **Current Behavior**: Unmocked live integration tests disguised as unit tests.
- **Recommended Resolution**: Mock all external HTTP requests using `unittest.mock.patch` or `pytest-mock` with recorded JSON fixtures.
- **Relevant Module**: `tests/`

---

### [LIM-08] Persistence Tests Mutate Live Database
- **Status**: **Confirmed**
- **Priority**: P2 — Medium
- **Verified Evidence**: [`tests/test_api_persistence.py`](../tests/test_api_persistence.py#L122-L135)
  ```python
  db = SessionLocal()
  trip = db.query(Trip).filter(Trip.destination == "Test Destination").first()
  ```
- **Practical Impact**: Running the test suite connects to the live database specified in `.env`, inserts records with destination `"Test Destination"`, and does not roll back or delete them. This pollutes development databases with test artifacts and fails if PostgreSQL is not running.
- **Current Behavior**: Permanent database mutation during test runs.
- **Recommended Resolution**: Use a dedicated in-memory SQLite database fixture (`sqlite:///:memory:`) for pytest execution.
- **Relevant Module**: `tests.test_api_persistence`

---

### [LIM-09] Raw Exception Detail Leakage in API
- **Status**: **Confirmed**
- **Priority**: P2 — Medium
- **Verified Evidence**: [`src/api/main.py`](../src/api/main.py#L388-L391)
  ```python
  except Exception as exc:
      ...
      raise HTTPException(status_code=500, detail=f"Travel planning failed: {exc}") from exc
  ```
- **Practical Impact**: When an unexpected error occurs (e.g. database connection drop or third-party API error containing query parameters with API keys), the raw stringified exception is returned to the client in HTTP 500 JSON, exposing internal file paths, module structures, and potentially credentials.
- **Current Behavior**: Full internal exception string returned in response.
- **Recommended Resolution**: Log the exception internally and return a sanitized message: `detail="An internal error occurred during plan generation."`.
- **Relevant Module**: `src.api.main`

---

### [LIM-10] Synchronous Long-Running HTTP Request Blocking
- **Status**: **Confirmed**
- **Priority**: P2 — Medium
- **Verified Evidence**: [`src/api/main.py`](../src/api/main.py#L268-L372)
  ```python
  @app.post("/plan", response_model=TravelPlanResponse)
  def create_travel_plan(request: TravelRequest) -> TravelPlanResponse:
      ...
      result = run_travel_planner(request) # Blocks for 30-90s
  ```
- **Practical Impact**: The endpoint executes 13–19 LLM calls and 5 web searches synchronously. The HTTP socket remains open for 30–90 seconds. Reverse proxies (Nginx, AWS ALB, Cloudflare default 60s) drop the connection with a 504 Gateway Timeout, and Uvicorn threadpool workers become saturated under modest concurrency.
- **Current Behavior**: Request blocks until complete or timed out.
- **Recommended Resolution**: Return `202 Accepted` with a `job_id`, run the graph in an asynchronous background worker (Celery/Redis), and stream real-time node progress via WebSockets or Server-Sent Events (SSE).
- **Relevant Module**: `src.api.main`

---

### [LIM-11] Disconnected Backend Trip History Endpoints
- **Status**: **Confirmed**
- **Priority**: P2 — Medium
- **Verified Evidence**: [`src/api/main.py` lines 46–136](file:///d:/ai-travel-planner/src/api/main.py#L46-L136) vs [`streamlit_app/app.py`](../streamlit_app/app.py)
- **Practical Impact**: The backend provides fully functional endpoints `GET /trips` and `GET /trips/{trip_id}`. However, the Streamlit frontend has zero components or sidebar menus that call these endpoints. Users have no way to view previously generated trips through the UI.
- **Current Behavior**: Endpoints exist in FastAPI but are orphaned from the user interface.
- **Recommended Resolution**: Add a "Trip History" sidebar in Streamlit allowing users to select and view past trips.
- **Relevant Module**: `streamlit_app.app`

---

### [LIM-12] Missing Date-Format Validation in `TravelRequest`
- **Status**: **Confirmed**
- **Priority**: P2 — Medium
- **Verified Evidence**: [`src/api/schemas.py`](../src/api/schemas.py#L12-L15) vs [`src/tools/accommodation.py`](../src/tools/accommodation.py#L11-L25)
- **Practical Impact**: `TravelRequest.travel_dates` is typed as an unvalidated `str`. If a user passes `"next weekend"` or `"2026/10/10 to 2026/10/12"`, Pydantic accepts it. Downstream, `accommodation.py` crashes on `split("to")`, causing an unhandled HTTP 500 error instead of a clean HTTP 422 validation response.
- **Current Behavior**: Bad date formats cause internal 500 crashes.
- **Recommended Resolution**: Add a Pydantic `@field_validator` with regex `^\d{4}-\d{2}-\d{2}\s+to\s+\d{4}-\d{2}-\d{2}$`.
- **Relevant Module**: `src.api.schemas`

---

### [LIM-13] ReportLab XML Escaping and Unicode Limitations
- **Status**: **Confirmed**
- **Priority**: P2 — Medium
- **Verified Evidence**: [`src/services/pdf_generator.py`](../src/services/pdf_generator.py#L166-L194)
- **Practical Impact**: Dynamic strings are interpolated directly into ReportLab `Paragraph` flowables without escaping. If a venue has an ampersand (`&`) or angle brackets (`<`, `>`), ReportLab's XML parser throws `ExpatError`, crashing PDF downloads with HTTP 500. Additionally, ReportLab's default font fails on Indian Rupee symbols (`₹`) or emojis.
- **Current Behavior**: Unescaped XML or non-ASCII characters crash PDF generation.
- **Recommended Resolution**: Wrap all dynamic strings with `html.escape()`, and register a TrueType Unicode font (e.g. DejaVu Sans).
- **Relevant Module**: `src.services.pdf_generator`

---

### [LIM-14] Accommodation Localization Hardcoded to INR and India
- **Status**: **Confirmed**
- **Priority**: P2 — Medium
- **Verified Evidence**: [`src/tools/accommodation.py`](../src/tools/accommodation.py#L58-L60)
  ```python
  "currency": "INR",
  "gl": "in",
  "hl": "en",
  ```
- **Practical Impact**: Hotel queries for non-Indian destinations (London, Tokyo, Paris) force rates into INR and bias search results toward Indian traveler portals.
- **Current Behavior**: Locked to Indian Rupee and Indian Google locale.
- **Recommended Resolution**: Make currency and `gl` parameters dynamic based on destination or user input.
- **Relevant Module**: `src.tools.accommodation`

---

### [LIM-15] External API Retry and Rate-Limit Handling Gaps
- **Status**: **Confirmed**
- **Priority**: P2 — Medium
- **Verified Evidence**: [`src/tools/destination.py`](../src/tools/destination.py), [`accommodation.py`](../src/tools/accommodation.py), [`activity.py`](../src/tools/activity.py), [`weather.py`](../src/tools/weather.py), [`food.py`](../src/tools/food.py)
- **Practical Impact**: Tools execute `requests.get(...)` followed immediately by `response.raise_for_status()`. There are no retry decorators (`tenacity`), exponential backoff, or jitter for handling transient network drops or HTTP 429 rate limits.
- **Current Behavior**: A single dropped network packet aborts the entire 60-second workflow.
- **Recommended Resolution**: Apply `@retry(stop=stop_after_attempt(3), wait=wait_exponential())` on all external tool calls.
- **Relevant Module**: `src.tools.*`

---

### [LIM-16] Missing API Authentication and Authorization
- **Status**: **Confirmed**
- **Priority**: P2 — Medium
- **Verified Evidence**: [`src/api/main.py`](../src/api/main.py)
- **Practical Impact**: Endpoints `/plan`, `/trips`, and `/trips/{id}/pdf` are completely open and unauthenticated. Any client on the network can trigger expensive, billable LLM workflows or access all stored travel plans.
- **Current Behavior**: Zero access control.
- **Recommended Resolution**: Implement API key header validation (`Security(APIKeyHeader)`) or OAuth2 JWT bearer tokens.
- **Relevant Module**: `src.api.main`

---

### [LIM-17] Missing CORS Configuration in FastAPI
- **Status**: **Confirmed**
- **Priority**: P2 — Medium
- **Verified Evidence**: [`src/api/main.py`](../src/api/main.py#L23-L30)
- **Practical Impact**: The FastAPI app lacks `CORSMiddleware`. Modern web browsers will reject API calls from any external frontend running on a different domain or port.
- **Current Behavior**: Browser cross-origin requests fail.
- **Recommended Resolution**: Add `app.add_middleware(CORSMiddleware, allow_origins=["*"], ...)` in development.
- **Relevant Module**: `src.api.main`

---

### [LIM-18] Container Running as Default Root User
- **Status**: **Confirmed**
- **Priority**: P3 — Low
- **Verified Evidence**: [`Dockerfile`](../Dockerfile)
- **Practical Impact**: The container executes as `root`. If a container breakout vulnerability were discovered, an attacker would have root privileges.
- **Current Behavior**: Default root user execution.
- **Recommended Resolution**: Add `RUN useradd -m appuser && USER appuser`.
- **Relevant Module**: `Dockerfile`

---

### [LIM-19] Limited Application-Level Logging
- **Status**: **Confirmed**
- **Priority**: P3 — Low
- **Verified Evidence**: Entire `src/` directory
- **Practical Impact**: No standard library `logging` instances are configured. When exceptions occur, nothing is written to log files or standard error streams beyond default Uvicorn access logs.
- **Current Behavior**: Zero structured application logging.
- **Recommended Resolution**: Configure standard `logging.getLogger("ai_travel_planner")` across all modules.
- **Relevant Module**: Entire `src/` directory

---

### [LIM-20] Duplicate Dead Code in PDF Services
- **Status**: **Confirmed**
- **Priority**: P3 — Low
- **Verified Evidence**: [`src/services/pdf.py`](../src/services/pdf.py) vs [`src/services/pdf_generator.py`](../src/services/pdf_generator.py)
- **Practical Impact**: `src/services/pdf.py` contains 644 lines of code that is never imported or executed anywhere in the project (`main.py` imports `src.services.pdf_generator`). It creates confusion and maintenance burden.
- **Current Behavior**: Dead duplicate code residing in the repository.
- **Recommended Resolution**: Delete `src/services/pdf.py`.
- **Relevant Module**: `src.services.pdf`

---

### [LIM-21] Status Marked `completed` Even After Failed Validation
- **Status**: **Confirmed**
- **Priority**: P3 — Low
- **Verified Evidence**: [`src/api/main.py` line 352](file:///d:/ai-travel-planner/src/api/main.py#L352)
  ```python
  update_trip_status(db=db, trip_id=trip.id, status="completed")
  ```
- **Practical Impact**: When a plan fails validation 3 times and exits via `validation_failed`, the plan is incomplete and contains unaddressed issues. However, the API still marks `trip.status = "completed"` in the database.
- **Current Behavior**: Failed plans are marked as completed.
- **Recommended Resolution**: Set `status="completed_with_warnings"` or `"validation_failed"` when `is_valid == False`.
- **Relevant Module**: `src.api.main`

---

### [LIM-22] Unnecessary Synchronization Barrier Before Food Agent
- **Status**: **Confirmed**
- **Priority**: P3 — Low
- **Verified Evidence**: [`src/graph/travel_graph.py`](../src/graph/travel_graph.py#L182-L196) & [`src/agents/food_agent.py`](../src/agents/food_agent.py#L27-L66)
- **Practical Impact**: `food_agent` waits for `stay`, `activity`, and `weather` to finish. However, `food_agent` only uses destination, budget, and preferences. It has zero dependency on stay, activity, or weather data.
- **Current Behavior**: Unnecessary serialization adds 5–10 seconds of latency.
- **Recommended Resolution**: Connect `destination -> food` directly, running all 4 research agents in parallel.
- **Relevant Module**: `src.graph.travel_graph`

---

### [LIM-23] Redundant Stage 1 Tool-Calling Model Invocations
- **Status**: **Confirmed**
- **Priority**: P3 — Low
- **Verified Evidence**: Research agents in [`src/agents/`](../src/agents/)
- **Practical Impact**: Each research agent calls Gemini once to generate tool arguments (`bind_tools`), and a second time to format results into Pydantic (`with_structured_output`). Because tool arguments are already known deterministically from state, Stage 1 is an unnecessary roundtrip.
- **Current Behavior**: Two LLM calls per research agent (10 calls total).
- **Recommended Resolution**: Call tools directly with state arguments and execute only one structured LLM call per research agent.
- **Relevant Module**: `src.agents.*`

---

### [LIM-24] Weather Forecast Duration & Date Constraints
- **Status**: **Confirmed**
- **Priority**: P3 — Low
- **Verified Evidence**: [`src/tools/weather.py`](../src/tools/weather.py#L23-L32)
- **Practical Impact**: WeatherAPI `/forecast.json` free tier only supports 3 days of forecast from the current date. Trips longer than 3 days fail or truncate, and trips planned months in advance query current weather rather than future climate.
- **Current Behavior**: Assumes upcoming days from today match future travel dates.
- **Recommended Resolution**: Check date distance; if >14 days out, query monthly historical climate averages.
- **Relevant Module**: `src.tools.weather`

---

### [LIM-25] Missing Automated MCP Unit Tests
- **Status**: **Confirmed**
- **Priority**: P3 — Low
- **Verified Evidence**: [`tests/`](../tests/)
- **Practical Impact**: There are zero automated tests covering `TravelMCPClient`, `MCPServer`, tool registration, or JSON-RPC serialization. Regressions in MCP tool handling can only be discovered during full manual graph execution.
- **Current Behavior**: MCP layer is completely untested in CI.
- **Recommended Resolution**: Add `tests/test_mcp_client.py` asserting tool listing and execution using mocked transport.
- **Relevant Module**: `tests/`

---

## ⚖️ Architectural Trade-off Summary: Prototype vs. Enterprise

| Architectural Dimension | Current Prototype Decision | Why It Was Chosen | Enterprise Production Target |
|---|---|---|---|
| **API Execution** | Synchronous HTTP POST | Simpler code, zero queue dependencies. | Asynchronous Celery / Redis queue with SSE streaming. |
| **Tool Protocol** | Ephemeral Stdio Subprocess | Easy local setup; no separate server ports. | Persistent MCP Server cluster with SSE/gRPC transport. |
| **Geographic Validation** | Hardcoded Goa Area Maps | Fast demonstration of heuristic safety nets. | Geocoding lat/long coordinates with Haversine clustering. |
| **Testing Strategy** | Live API calls in `pytest` | Fast initial development without building mocks. | 100% deterministic tests using `pytest-mock` & in-memory SQLite. |
| **Security Layer** | Unauthenticated | Easy local development and testing. | API Key / JWT header guards with Redis rate limiting. |
