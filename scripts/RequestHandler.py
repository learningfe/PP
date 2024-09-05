from config import REQUEST_LIST
from config import RESPONSE_LIST
from AccountManager import AccountManager
from ServerSocket import ServerSocket
from SocketWrapper import SocketWrapper

class RequestHandler:
    def __init__(self,server:ServerSocket):
        self.request_handlers = {}
        self.register_handler(REQUEST_LIST['REQUEST_LOGIN'],self.handle_login_request)
        self.register_handler(REQUEST_LIST['REQUEST_SEND_MESSAGE'],self.handle_send_message_request)

    def register_handler(self, request_id:str,handler):
        self.request_handlers[request_id] = handler

    def handle_request(self,client:SocketWrapper,request_id:str,**args):
        handler = self.request_handlers[request_id]
        if handler:
            return handler(client,**args)
    
    def handle_login_request(self,client:SocketWrapper,**args):
        username = args['username']
        password_input = args['password']
        if not AccountManager().verify_user(username,password_input):
            #response to client
            client.send(RESPONSE_LIST['RESPONSE_LOGIN_FAILED'])
            return False
        else:
            #response to client
            client.send(RESPONSE_LIST['RESPONSE_LOGIN_SUCCESS'])
            return True
    
    def handle_send_message_request(self,client:SocketWrapper,**args):
        #广播
        client.send(RESPONSE_LIST['RESPONSE_SEND_MESSAGE_SUCCESS'])
        return f"Message sent: {args['message']}"