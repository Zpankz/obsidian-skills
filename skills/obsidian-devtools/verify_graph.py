import asyncio
from obsidian_devtools.client import CDPClient
from obsidian_devtools.sdk import ObsidianClient

async def main():
    client = CDPClient(port=9222)
    try:
        await client.connect()
    except Exception as e:
        print(f"Failed to connect: {e}")
        return

    sdk = ObsidianClient(client)

    # Note: Graph zoom usually requires the Graph View to be active (open in a tab)
    print("Attempting to zoom graph...")
    # First, try to open graph view
    await sdk.eval("app.commands.executeCommandById('graph:open')")
    await asyncio.sleep(1) # Wait for view to load

    success = await sdk.graph_zoom_to(2.5) # Zoom in 250%
    if success:
        print("Success! Zoomed graph view.")
    else:
        print("Failed to find or control graph view.")

if __name__ == "__main__":
    asyncio.run(main())
