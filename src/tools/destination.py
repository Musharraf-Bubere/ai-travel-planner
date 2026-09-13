import os

from dotenv import load_dotenv
from langchain_core.tools import tool
from tavily import TavilyClient


load_dotenv()


@tool
def search_destination(
    destination: str,
    preferences: list[str],
) -> list[dict]:
    """Search the web for travel information about a destination."""

    api_key = os.getenv("TAVILY_API_KEY")

    if not api_key:
        raise ValueError(
            "TAVILY_API_KEY is not set in the environment."
        )

    client = TavilyClient(api_key=api_key)

    query = (
        f"{destination} travel guide, best areas, attractions, "
        f"travel considerations, and recommendations for "
        f"{', '.join(preferences)}"
    )

    response = client.search(
        query=query,
        search_depth="advanced",
        max_results=5,
    )

    results = []

    for result in response.get("results", []):
        results.append(
            {
                "title": result.get("title", ""),
                "url": result.get("url", ""),
                "content": result.get("content", ""),
            }
        )

    return results