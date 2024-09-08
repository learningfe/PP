import asyncio
import websockets
from config import PORT
from Parser import Parser
from RequestHandler import RequestHandler
from Logger import Logger

class ChatServer:
    def __init__(self):
        self.clients = set()

    async def handle_single_client(self, client, path):
        self.clients.add(client)
        Logger().log(f"New client connected: {client.remote_address}")
        try:
            async for message in client:
                if message:
                    Logger().log(f"Received message from {client.remote_address}: {message}")
                    message_parsed = Parser().parse_message(message)
                    response = await RequestHandler(self.server, self.clients).handle_request(**message_parsed)
                    Logger().log(f"Sent response to {client.remote_address}: {response}")
        except Exception as e:
            Logger().error(f"Error handling client {client.remote_address}: {e}")
        finally:
            self.clients.remove(client)
            await client.close()

    def start_server(self):
        self.server = websockets.serve(self.handle_single_client, '0.0.0.0', PORT)
        asyncio.get_event_loop().run_until_complete(self.server)
        asyncio.get_event_loop().run_forever()

if __name__ == "__main__":
    Logger().log("Starting chat server")
    chat_server = ChatServer()
    chat_server.start_server()