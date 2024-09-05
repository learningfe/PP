import json
import os

class AccountManager:
    def __init__(self,user_data_file_path = '.\\user_data.json'):
        self.user_data_file_path = user_data_file_path
        self.user_data = {}
    
    def load_user_data(self):
        if not os.path.exists(self.user_data_file_path):
            open(self.user_data_file_path,'w').close()
        else:
            with open(self.user_data_file_path,'r') as f:
                self.user_data = json.load(f)

    def save_user_data(self):
        with open(self.user_data_file_path,'w') as f:
            json.dump(self.user_data,f)

    def add_user(self,username:str,password:str):
        self.load_user_data()
        for user in self.user_data:
            if user['user_name'] == username:
                return False
        new_user = dict(user_name = username,password = password,nickname = '')
        self.user_data.append(new_user)
        self.save_user_data()
        return True
    
    def remove_user(self,username:str):
        self.load_user_data()
        for user in self.user_data:
            if user['user_name'] == username:
                self.user_data.remove(user)
                self.save_user_data()
                return True
        return False

    def verify_user(self,username:str,password:str):
        self.load_user_data()
        for user in self.user_data:
            return user['user_name'] == username and user['password'] == password
        return False

    def set_nickname(self,username:str,nickname:str):
        self.load_user_data()
        for user in self.user_data:
            if user['user_name'] == username:
                user['nickname'] = nickname
                self.save_user_data()
                return True
        return False