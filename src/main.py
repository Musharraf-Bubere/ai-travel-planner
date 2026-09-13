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
    print("FINAL TRAVEL PLAN")
    print("=" * 60)

    print(result.get("final_response"))


if __name__ == "__main__":
    main()