from fastapi import FastAPI, HTTPException
from fastapi.responses import Response

from src.api.schemas import (
    TravelPlanResponse,
    TravelRequest,
    TripDetailResponse,
    TripResponse,
)
from src.database.connection import SessionLocal
from src.database.repository import (
    create_travel_plan as save_travel_plan,
    create_trip,
    get_all_trips,
    get_trip,
    get_travel_plans_for_trip,
    update_trip_status,
)
from src.graph.travel_graph import build_travel_graph
from src.services.pdf_generator import generate_travel_plan_pdf


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


@app.get(
    "/trips",
    response_model=list[TripResponse],
)
def get_trips() -> list[TripResponse]:
    """
    Retrieve all previously generated travel trips.
    """
    db = SessionLocal()

    try:
        trips = get_all_trips(db)

        return [
            TripResponse(
                id=trip.id,
                destination=trip.destination,
                travel_dates=trip.travel_dates,
                duration=trip.duration,
                travelers=trip.travelers,
                budget=trip.budget,
                preferences=trip.preferences,
                status=trip.status,
            )
            for trip in trips
        ]

    finally:
        db.close()


@app.get(
    "/trips/{trip_id}",
    response_model=TripDetailResponse,
)
def get_trip_details(
    trip_id: int,
) -> TripDetailResponse:
    """
    Retrieve a specific trip and its generated travel plans.
    """
    db = SessionLocal()

    try:
        trip = get_trip(
            db=db,
            trip_id=trip_id,
        )

        if trip is None:
            raise HTTPException(
                status_code=404,
                detail=f"Trip with id {trip_id} not found.",
            )

        travel_plans = get_travel_plans_for_trip(
            db=db,
            trip_id=trip.id,
        )

        return TripDetailResponse(
            id=trip.id,
            destination=trip.destination,
            travel_dates=trip.travel_dates,
            duration=trip.duration,
            travelers=trip.travelers,
            budget=trip.budget,
            preferences=trip.preferences,
            status=trip.status,
            travel_plans=[
                {
                    "id": plan.id,
                    "itinerary": plan.itinerary,
                    "accommodation_summary": (
                        plan.accommodation_summary
                    ),
                    "food_summary": plan.food_summary,
                    "travel_tips": plan.travel_tips,
                    "validation": plan.validation,
                    "validation_attempts": (
                        plan.validation_attempts
                    ),
                    "created_at": plan.created_at,
                }
                for plan in travel_plans
            ],
        )

    finally:
        db.close()

@app.get(
    "/trips/{trip_id}/pdf",
)
def download_trip_pdf(
    trip_id: int,
) -> Response:
    """
    Generate and download a PDF for a previously generated travel plan.
    """

    db = SessionLocal()

    try:
        # ---------------------------------------------------------
        # 1. Retrieve the trip
        # ---------------------------------------------------------
        trip = get_trip(
            db=db,
            trip_id=trip_id,
        )

        if trip is None:
            raise HTTPException(
                status_code=404,
                detail=f"Trip with id {trip_id} not found.",
            )

        # ---------------------------------------------------------
        # 2. Retrieve the generated travel plans
        # ---------------------------------------------------------
        travel_plans = get_travel_plans_for_trip(
            db=db,
            trip_id=trip.id,
        )

        if not travel_plans:
            raise HTTPException(
                status_code=404,
                detail=f"No travel plan found for trip {trip_id}.",
            )

        # ---------------------------------------------------------
        # 3. Use the latest generated travel plan
        # ---------------------------------------------------------
        latest_plan = travel_plans[0]

        # ---------------------------------------------------------
        # 4. Generate PDF
        # ---------------------------------------------------------
        pdf_bytes = generate_travel_plan_pdf(
            destination=trip.destination,
            travel_dates=trip.travel_dates,
            trip_details={
                "itinerary": latest_plan.itinerary,
                "accommodation_summary": (
                    latest_plan.accommodation_summary
                ),
                "food_summary": latest_plan.food_summary,
                "travel_tips": latest_plan.travel_tips,
                "validation": latest_plan.validation,
            },
        )

        # ---------------------------------------------------------
        # 5. Return downloadable PDF
        # ---------------------------------------------------------
        filename = (
            f"travel_plan_{trip.destination.lower().replace(' ', '_')}"
            f"_{trip.id}.pdf"
        )

        return Response(
            content=pdf_bytes,
            media_type="application/pdf",
            headers={
                "Content-Disposition": (
                    f'attachment; filename="{filename}"'
                )
            },
        )

    finally:
        db.close()

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
            trip_id=trip.id,
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