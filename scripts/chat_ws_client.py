import asyncio
import websockets
import json
from concurrent.futures import ThreadPoolExecutor

async def async_input(prompt):
    with ThreadPoolExecutor() as pool:
        return await asyncio.get_event_loop().run_in_executor(pool, input, prompt)

async def send_message(websocket):
    try:
        while True:
            message = await async_input("Input message: ")
            message_data = {
                "type": "message",
                "content": message,
                "nickname": "YourNickname"
            }
            await websocket.send(json.dumps(message_data))
            print(f"Sent: {message_data}")
    except websockets.ConnectionClosedError as e:
        print(f"Connection closed with error: {e}")
    except asyncio.CancelledError:
        print("Send message task was cancelled.")
    except Exception as e:
        print(f"Unexpected error: {e}")

async def receive_message(websocket):
    try:
        while True:
            response = await websocket.recv()
            print(f"Received: {response}")
    except websockets.ConnectionClosedError as e:
        print(f"Connection closed with error: {e}")
    except asyncio.CancelledError:
        print("Receive message task was cancelled.")
    except Exception as e:
        print(f"Unexpected error: {e}")

async def test_client():
    uri = "ws://localhost:8765"
    try:
        async with websockets.connect(uri) as websocket:
            await asyncio.gather(
                send_message(websocket),
                receive_message(websocket)
            )
    except Exception as e:
        print(f"Failed to connect to server: {e}")

if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(test_client())