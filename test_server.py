from fastmcp import Client

async def main():
    # Connect via stdio to a local script
    async with Client("server.py") as client:
        tools = await client.list_tools()
        print(f"Available tools: {', '.join([tool.name for tool in tools])}")
        
        # Test web search
        result = await client.call_tool("web_search", {"query": "What is the capital of France?"})
        print(f"Web search result: {result[0].text[:300]}...")
        
        # Test calculator
        calc_result = await client.call_tool("calculate", {"expression": "15 * 8 + 25"})
        print(f"Calculator result: {calc_result}")
        
        # Test dice roller
        dice_result = await client.call_tool("roll_dice", {"notation": "3d6"})
        print(f"Dice result: {dice_result}")

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())