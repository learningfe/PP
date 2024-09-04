class RoomManager:
    def __init__(self):
        self.rooms = {}

    def add_room(self, room):
        self.rooms[room.id] = room

    def remove_room(self, room):
        del self.rooms[room.id]

    def get_room(self, room_id):
        return self.rooms.get(room_id)

    def get_all_rooms(self):
        return self.rooms.values()