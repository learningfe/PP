from config import DELIMITER
from config import REQUEST_LIST


class UnknownCommandError(Exception):
    pass

class ParameterError(Exception):
    pass

class Parser:
    def parse(self, text:str,delimiter = DELIMITER):
        parsed_data = text.split(delimiter)
        request_id = parsed_data[0]
        if  request_id in REQUEST_LIST.values():
            if request_id == REQUEST_LIST['REQUEST_LOGIN']:
                try:
                    return request_id,{'username':parsed_data[1],'password':parsed_data[2]}
                except IndexError:
                    raise ParameterError("Missing parameters")
            elif request_id == REQUEST_LIST['REQUEST_SEND_MESSAGE']:
                try:
                    return request_id,{'message':parsed_data[1]}
                except IndexError:
                    raise ParameterError("Missing parameters")
        else:
            raise UnknownCommandError(f"Unknown command: {request_id}")
