import asyncio
import websockets
import json
import time
#from RequestHandler import RequestHandler

class ChatServer:
    def init_server(self):
        #self.Parser = Parser()
        #self.RequestHandler = RequestHandler()
        pass

    def parse_message(self, message_json):
        message = json.loads(message_json)

        type = message.get("type")
        content = message.get("content")
        timestamp = int(time.time() * 1000)
        nickname = message.get("nickname") # for temporary, will be removed after login supported

        return {
            "type": type,
            "content": content,
            "timestamp": timestamp,
            "nickname": nickname
        }


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
                print(f"Received message: {message}")
                message_parsed = self.parse_message(message)
                await websocket.send(json.dumps(message_parsed))

    def start_server(self):
        self.init_server()
        start_server = websockets.serve(self.handle_single_client, '0.0.0.0', 8765)
        asyncio.get_event_loop().run_until_complete(start_server)
        asyncio.get_event_loop().run_forever()

if __name__ == "__main__":
    chat_server = ChatServer()
    chat_server.start_server()