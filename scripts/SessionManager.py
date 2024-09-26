import uuid;
import json
import os
import time

class SessionManager:
    def __init__(self,json_path:str = './data/session.json'):
        self.json_path = json_path
        self.session_store = {}
        if not os.path.exists(self.json_path):
            with open(self.json_path, 'w') as json_file:
                json.dump({}, json_file)
        self.load_sessions()

    def create_session_id(self,user_name:str, avatar_url:str,access_token:str):
        session_id = str(uuid.uuid4())
        self.session_store[session_id] = {
            'expire_time': int(time.time()) + 3600,
            'user_name': user_name,
            'avatar_url': avatar_url,
            'access_token': access_token
        }
        self.save_sessions()
        return session_id
    
    def is_valid_session_id(self,session_id:str):
        return session_id in self.session_store 
    
    def is_expired_session_id(self,session_id:str):
        if session_id in self.session_store:
            return self.session_store[session_id]['expire_time'] < int(time.time())
        return True
    
    def get_session(self,session_id:str):
        return self.session_store.get(session_id)
    
    def save_sessions(self):
        with open(self.json_path, 'w') as json_file:
            json.dump(self.session_store, json_file)

    def load_sessions(self):
        if os.path.exists(self.json_path):
            with open(self.json_path, 'r') as json_file:
                self.session_store = json.load(json_file)

    def remove_session(self,session_id:str):
        if session_id in self.session_store:
            self.session_store.pop(session_id)
            self.save_sessions()
            return True
        return False
    
    def update_session(self,session_id:str):
        if session_id in self.session_store:
            user_name = self.session_store[session_id]['user_name']
            avatar_url = self.session_store[session_id]['avatar_url']
            access_token = self.session_store[session_id]['access_token']
            self.remove_session(session_id)
            return self.create_session_id(user_name, avatar_url, access_token)