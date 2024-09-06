import asyncio
import websockets

async def test_client():
    uri = "ws://localhost:8765"
    async with websockets.connect(uri) as websocket:
        while True:
            message = input("Input message: ")
            await websocket.send(message)
            print(f"Sent: {message}")

            response = await websocket.recv()
            print(f"Received: {response}")

if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(test_client())