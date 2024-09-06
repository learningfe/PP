import time
import json

class RequestHandler:
    def __init__(self, server ,clients):
        self.server = server
        self.clients = clients
        self.handlers = {}
        self.register_command("message", self.handle_message)

    def register_command(self, type:str, handler):
        self.handlers[type] = handler

    async def handle_request(self, **kwargs):
        type = kwargs.get("type")
        return await self.handlers[type](**kwargs)
        
    async def handle_message(self, **kwargs):
        content = kwargs.get("content")
        nickname = kwargs.get("nickname")
        timestamp = int(time.time() * 1000)
        response = {
            "type": "message",
            "content": content,
            "nickname": nickname,
            "timestamp": timestamp
        }
        for client in self.clients:
            await client.send(json.dumps(response))
        return response        