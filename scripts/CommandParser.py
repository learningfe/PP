class CommandParser:
    def __init__(self):
        self.commands = {}

    def register_command(self, command_name, handler):
        self.commands[command_name] = handler

    def parse_command(self, input_str):
        parts = input_str.split(' ', 1)
        command_name = parts[0]
        args = parts[1] if len(parts) > 1 else ''
        
        if command_name in self.commands:
            handler = self.commands[command_name]
            handler(args)
        else:
            print(f"Unknown command: {command_name}")