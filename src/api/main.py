from fastapi import FastAPI, HTTPException

from src.api.schemas import TravelPlanResponse, TravelRequest
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

    return graph.invoke(state)


@app.post(
    "/plan",
    response_model=TravelPlanResponse,
)
def create_travel_plan(
    request: TravelRequest,
) -> TravelPlanResponse:
    """
    Generate a complete travel plan using the multi-agent
    LangGraph workflow.
    """
    try:
        result = run_travel_planner(
            request
        )

        final_response = result.get(
            "final_response"
        )

        if not final_response:
            raise ValueError(
                "Travel planning workflow did not produce "
                "a final response."
            )

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
        raise HTTPException(
            status_code=500,
            detail=f"Travel planning failed: {exc}",
        ) from exc