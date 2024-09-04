import RoomUser

class Room:
    def __init__(self,room_id:int,room_name:str):
        self.id = room_id
        self.name = room_name
        self.users = []
        self.chat_history = []

    def add_user(self,user:RoomUser):
        self.users.append(user)

    def remove_user(self,user:RoomUser):
        self.users.remove(user)
        