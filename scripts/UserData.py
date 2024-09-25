import time 

class UserData:
    def __init__(self, username, password, status):
        self.status = status
        self.username = username
        self.password = password
        self.last_active = 'Never'

    def set_online(self):
        if self.status == 'offline':
            self.status = 'online'
            self.update_last_active()
            return True
        return False

    def set_offline(self):
        if self.status == 'online':
            self.status = 'offline'
            self.update_last_active()
            return True
        return False

    def update_last_active(self,):
        self.last_active = int(time.time() * 1000)

    def __dict__(self):
        return {
            'user_id': self.user_id,
            'status': self.status,
            'last_active': self.last_active
        }