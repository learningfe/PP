import json

class Parser:
    def parse_message(self, message_json):
        message = json.loads(message_json)

        type = message.get("type")
        content = message.get("content")
        nickname = message.get("nickname")
        return {
            "type": type,
            "content": content,
            "nickname": nickname
        }
