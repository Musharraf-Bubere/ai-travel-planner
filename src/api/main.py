from fastapi import FastAPI, HTTPException

from src.api.schemas import TravelPlanResponse, TravelRequest
from src.database.connection import SessionLocal
from src.database.repository import (
    create_travel_plan as save_travel_plan,
    create_trip,
    update_trip_status,
)
from src.graph.travel_graph import build_travel_graph


app = FastAPI(
    title="AI Travel Planner API",
    description=(
        "Multi-Agent Travel Planning System powered by "
        "LangGraph, LangChain, and external travel research tools."
    ),
    version="1.0.0",
)


@app.get("/health")
def health_check() -> dict:
    """
    Health check endpoint.

    Used to verify that the API server is running.
    """
    return {
        "status": "healthy",
        "service": "AI Travel Planner API",
    }


def run_travel_planner(
    request: TravelRequest,
) -> dict:
    """
    Execute the LangGraph travel planning workflow.

    This function is kept separate from the HTTP endpoint so it can
    be mocked during API tests.
    """
    graph = build_travel_graph()

    state = {
        "destination": request.destination,
        "travel_dates": request.travel_dates,
        "duration": request.duration,
        "travelers": request.travelers,
        "budget": request.budget,
        "preferences": request.preferences,
    }

    config = {
        "tags": [
            "travel-planner",
            "multi-agent",
            "langgraph",
            "mcp",
        ],
        "metadata": {
            "destination": request.destination,
            "travel_dates": request.travel_dates,
            "duration": request.duration,
            "travelers": request.travelers,
            "budget": request.budget,
            "preferences": request.preferences,
        },
    }

    return graph.invoke(
        state,
        config=config,
    )


@app.post(
    "/plan",
    response_model=TravelPlanResponse,
)
def create_travel_plan(
    request: TravelRequest,
) -> TravelPlanResponse:
    """
    Generate a complete travel plan and persist it in PostgreSQL.
    """
    db = SessionLocal()

    trip = None

    try:
        # ---------------------------------------------------------
        # 1. Persist the original travel request
        # ---------------------------------------------------------
        trip = create_trip(
            db=db,
            destination=request.destination,
            travel_dates=request.travel_dates,
            duration=request.duration,
            travelers=request.travelers,
            budget=request.budget,
            preferences=request.preferences,
            status="planning",
        )

        # ---------------------------------------------------------
        # 2. Execute the multi-agent LangGraph workflow
        # ---------------------------------------------------------
        result = run_travel_planner(request)

        final_response = result.get(
            "final_response"
        )

        if not final_response:
            update_trip_status(
                db=db,
                trip_id=trip.id,
                status="failed",
            )

            raise ValueError(
                "Travel planning workflow did not produce "
                "a final response."
            )

        # ---------------------------------------------------------
        # 3. Persist the generated travel plan
        # ---------------------------------------------------------
        save_travel_plan(
            db=db,
            trip_id=trip.id,
            itinerary=result.get(
                "itinerary",
                {},
            ),
            accommodation_summary=result.get(
                "stay_options",
                {},
            ),
            food_summary=result.get(
                "restaurants",
                {},
            ),
            travel_tips=final_response.get(
                "travel_tips",
                {},
            ),
            validation=result.get(
                "validation",
                {},
            ),
            validation_attempts=result.get(
                "validation_attempts",
                0,
            ),
        )

        # ---------------------------------------------------------
        # 4. Mark the trip as completed
        # ---------------------------------------------------------
        update_trip_status(
            db=db,
            trip_id=trip.id,
            status="completed",
        )

        # ---------------------------------------------------------
        # 5. Return the API response
        # ---------------------------------------------------------
        return TravelPlanResponse(
            destination=request.destination,
            travel_dates=request.travel_dates,
            validation=result.get(
                "validation",
                {},
            ),
            validation_attempts=result.get(
                "validation_attempts",
                0,
            ),
            final_response=final_response,
        )

    except HTTPException:
        raise

    except Exception as exc:
        if trip is not None:
            try:
                update_trip_status(
                    db=db,
                    trip_id=trip.id,
                    status="failed",
                )
            except Exception:
                # Preserve the original application error.
                pass

        raise HTTPException(
            status_code=500,
            detail=f"Travel planning failed: {exc}",
        ) from exc

    finally:
        db.close()