from src.graph.travel_graph import build_travel_graph


def main():
    graph = build_travel_graph()

    state = {
        "destination": "Goa",
        "travel_dates": "2026-10-10 to 2026-10-13",
        "duration": 3,
        "travelers": 2,
        "budget": 30000,
        "preferences": [
            "beaches",
            "food",
            "relaxation",
        ],
    }

    result = graph.invoke(state)

    print("\n" + "=" * 60)
    print("INTERMEDIATE STATE")
    print("=" * 60)

    print("\nDESTINATION:")
    print(result.get("destination_data"))

    print("\nACCOMMODATION:")
    print(result.get("stay_options"))

    print("\nACTIVITIES:")
    print(result.get("activities"))

    print("\nWEATHER:")
    print(result.get("weather"))

    print("\nRESTAURANTS:")
    print(result.get("restaurants"))

    print("\nITINERARY:")
    print(result.get("itinerary"))

    print("\nVALIDATION:")
    print(result.get("validation"))

    print("\nVALIDATION ATTEMPTS:")
    print(result.get("validation_attempts"))

    print("\n" + "=" * 60)
    print("FINAL TRAVEL PLAN")
    print("=" * 60)

    print(result.get("final_response"))


if __name__ == "__main__":
    main()