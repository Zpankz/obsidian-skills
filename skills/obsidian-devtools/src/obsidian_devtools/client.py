"""
CDP Client for Obsidian
Handles WebSocket connection and CDP protocol messages.
"""
import asyncio
import json
import logging
import httpx
import websockets
from typing import Any, Dict, Optional

logger = logging.getLogger(__name__)

class CDPClient:
    def __init__(self, port: int = 9222):
        self.port = port
        self.base_url = f"http://localhost:{port}"
        self.ws_url: Optional[str] = None
        self.ws: Optional[websockets.WebSocketClientProtocol] = None
        self._msg_id = 0
        self._pending_requests: Dict[int, asyncio.Future] = {}
        self._listen_task: Optional[asyncio.Task] = None

    async def connect(self):
        """Finds the target and establishes WebSocket connection."""
        if self.ws:
            try:
                # Check if connection is active by accessing state or similar
                # For newer websockets, closed is a property.
                if not getattr(self.ws, 'closed', True):
                    return
            except Exception:
                pass


        # 1. Discovery
        try:
            async with httpx.AsyncClient() as client:
                resp = await client.get(f"{self.base_url}/json/list")
                resp.raise_for_status()
                targets = resp.json()
        except Exception as e:
            raise RuntimeError(f"Failed to query Obsidian debug info: {e}")

        if not targets:
            raise RuntimeError("No debug targets found. Is Obsidian fully loaded?")

        # 2. Heuristic Target Selection
        # We want type='page' and usually the one with 'app://obsidian.md' or similar in URL
        target = next(
            (t for t in targets if t.get('type') == 'page' and 'app://' in t.get('url', '')),
            None
        )

        # Fallback: if no app:// page, take the first page
        if not target:
            target = next((t for t in targets if t.get('type') == 'page'), None)

        # Ultimate fallback: just take the first target
        if not target:
            target = targets[0]

        self.ws_url = target.get('webSocketDebuggerUrl')
        if not self.ws_url:
            raise RuntimeError(f"Target has no WebSocket URL: {target}")

        logger.info(f"Connecting to target: {target.get('title', 'Unknown')} ({self.ws_url})")

        # 3. Connection
        self.ws = await websockets.connect(self.ws_url, max_size=None) # max_size=None for large payloads
        self._listen_task = asyncio.create_task(self._listener())

    async def _listener(self):
        """Background task to receive messages."""
        try:
            async for raw_msg in self.ws:
                data = json.loads(raw_msg)
                msg_id = data.get("id")

                # If it's a response to a request
                if msg_id in self._pending_requests:
                    future = self._pending_requests.pop(msg_id)
                    if "error" in data:
                        future.set_exception(RuntimeError(data["error"]["message"]))
                    else:
                        future.set_result(data.get("result"))
                else:
                    # It's an event (like Console.messageAdded)
                    # For now we ignore events unless we implement event listeners
                    pass

        except Exception as e:
            logger.error(f"WebSocket listener error: {e}")
        finally:
            # Cancel all pending requests
            for future in self._pending_requests.values():
                future.cancel()
            self._pending_requests.clear()

    async def send(self, method: str, params: Optional[Dict[str, Any]] = None) -> Any:
        """Sends a CDP command and waits for the result."""
        is_closed = True
        if self.ws:
            try:
                is_closed = getattr(self.ws, 'closed', True)
            except Exception:
                pass

        if is_closed:
            await self.connect()


        self._msg_id += 1
        current_id = self._msg_id
        payload = {
            "id": current_id,
            "method": method,
            "params": params or {}
        }

        future = asyncio.Future()
        self._pending_requests[current_id] = future

        await self.ws.send(json.dumps(payload))
        return await future

    async def evaluate(self, expression: str, await_promise: bool = True) -> Any:
        """Executes JavaScript in the target context."""
        response = await self.send("Runtime.evaluate", {
            "expression": expression,
            "awaitPromise": await_promise,
            "returnByValue": True,
            "includeCommandLineAPI": True
        })

        if "exceptionDetails" in response:
            raise RuntimeError(f"JS Error: {response['exceptionDetails']}")

        return response.get("result", {}).get("value")

    async def close(self):
        if self._listen_task:
            self._listen_task.cancel()
        if self.ws:
            await self.ws.close()
