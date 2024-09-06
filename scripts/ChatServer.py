import asyncio
import websockets
#from RequestHandler import RequestHandler

class ChatServer:
    def init_server(self):
        #self.Parser = Parser()
        #self.RequestHandler = RequestHandler()
        pass

    async def handle_single_client(self, websocket, path):
        async for message in websocket:
            '''
            if message:
                try:
                    parsed_data = self.Parser.parse(message)
                except UnknownCommandError:
                    continue
                except ParameterError:
                    continue
                request_id = parsed_data[0]
                response = await self.RequestHandler.handle_request(websocket, request_id, **parsed_data[1])
                await websocket.send(response)
            else:
                break
            '''
            if message:
                await websocket.send(message)

    def start_server(self):
        self.init_server()
        start_server = websockets.serve(self.handle_single_client, '0.0.0.0', 8765)
        asyncio.get_event_loop().run_until_complete(start_server)
        asyncio.get_event_loop().run_forever()

if __name__ == "__main__":
    chat_server = ChatServer()
    chat_server.start_server()