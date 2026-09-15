import asyncio
import json
import sys
from typing import Any

from mcp import Client, StdioServerParameters


class TravelMCPClient:
    """Reusable client for the AI Travel Planner MCP server."""

    def __init__(self) -> None:
        self.server_params = StdioServerParameters(
            command=sys.executable,
            args=[
                "-m",
                "src.mcp_server.travel_server",
            ],
        )

    async def call_tool(
        self,
        tool_name: str,
        arguments: dict[str, Any],
    ) -> Any:
        """Connect to the MCP server and execute one tool."""
        async with Client(self.server_params) as client:
            result = await client.call_tool(
                tool_name,
                arguments,
            )

            if result.structured_content:
                return result.structured_content

            for content in result.content:
                if hasattr(content, "text"):
                    try:
                        return json.loads(content.text)
                    except json.JSONDecodeError:
                        return content.text

            return None


def call_mcp_tool(
    tool_name: str,
    arguments: dict[str, Any],
) -> Any:
    """Synchronous wrapper for calling an MCP tool."""
    return asyncio.run(
        TravelMCPClient().call_tool(
            tool_name,
            arguments,
        )
    )