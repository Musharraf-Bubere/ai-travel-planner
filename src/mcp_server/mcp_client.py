import asyncio
import json
import sys

from mcp import Client, StdioServerParameters


server_params = StdioServerParameters(
    command=sys.executable,
    args=["-m", "src.mcp_server.travel_server"],
)


async def main() -> None:
    async with Client(server_params) as client:

        print("=" * 60)
        print("MCP CONNECTION")
        print("=" * 60)

        print(f"Protocol version: {client.protocol_version}")

        if client.server_info:
            print(f"Server name: {client.server_info.name}")
            print(f"Server version: {client.server_info.version}")

        print("\n" + "=" * 60)
        print("AVAILABLE MCP TOOLS")
        print("=" * 60)

        tools_response = await client.list_tools()

        for tool in tools_response.tools:
            print(f"- {tool.name}")
            print(f"  {tool.description}")
            print()

        print("=" * 60)
        print("TESTING DESTINATION RESEARCH")
        print("=" * 60)

        result = await client.call_tool(
            "destination_research",
            {
                "destination": "Goa",
                "preferences": [
                    "beaches",
                    "food",
                    "relaxation",
                ],
            },
        )

        print("\nMCP TOOL RESULT:")

        if result.structured_content:
            print(
                json.dumps(
                    result.structured_content,
                    indent=2,
                    ensure_ascii=False,
                )
            )

        elif result.content:
            for content in result.content:
                if hasattr(content, "text"):
                    try:
                        parsed = json.loads(content.text)

                        print(
                            json.dumps(
                                parsed,
                                indent=2,
                                ensure_ascii=False,
                            )
                        )

                    except json.JSONDecodeError:
                        print(content.text)

                else:
                    print(content)


if __name__ == "__main__":
    asyncio.run(main())