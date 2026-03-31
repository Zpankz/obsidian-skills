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

    # Test Canvas Creation
    nodes = [
        {"id": "n1", "x": 0, "y": 0, "width": 400, "height": 400, "type": "text", "text": "Hello from SDK"},
        {"id": "n2", "x": 500, "y": 0, "width": 400, "height": 400, "type": "file", "file": "obstetrics-pain-hypertension.md"}
    ]
    edges = [
        {"id": "e1", "fromNode": "n1", "fromSide": "right", "toNode": "n2", "toSide": "left"}
    ]

    print("Creating TestCanvas.canvas...")
    try:
        await sdk.create_canvas("TestCanvas.canvas", nodes, edges)
        print("Success! Created TestCanvas.canvas")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    asyncio.run(main())
