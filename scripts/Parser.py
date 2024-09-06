import json

class Parser:
    def parse(self, text:str):
        dict = json.loads(text)
        return dict['content']
