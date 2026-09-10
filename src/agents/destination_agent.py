from src.state import TravelState


def destination_agent(state: TravelState) -> TravelState:
    state["destination_data"] = {
        "message": f"Researching {state['destination']}"
    }

    return state