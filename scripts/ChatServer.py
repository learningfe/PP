import asyncio
import websockets
from config import PORT
from Parser import Parser
from RequestHandler import RequestHandler

class ChatServer:
    def __init__(self):
        self.clients = set()

    async def handle_single_client(self, client, path):
        self.clients.add(client)
        print(f"New client connected")
        async for message in client:
            if message:
                print(f"Received message: {message}")
                message_parsed = Parser().parse_message(message)
                await RequestHandler(self.server, self.clients).handle_request(**message_parsed)

    def start_server(self):
        self.server = websockets.serve(self.handle_single_client, '0.0.0.0', PORT)
        asyncio.get_event_loop().run_until_complete(self.server)
        asyncio.get_event_loop().run_forever()

if __name__ == "__main__":
    chat_server = ChatServer()
    chat_server.start_server()