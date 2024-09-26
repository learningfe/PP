from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse
from requests import exceptions
from Logger import Logger
import json
from github_oauth_client import github_oauth_client
from github_user_api_client import github_user_api_client

# Read secret from environment variable or something else
GITHUB_CLIENT_ID = ''
GITHUB_CLIENT_SECRET = ''
GITHUB_REDIRECT_URI = 'http://localhost:8100/api/v1/oauth/github'

logger = Logger("./log/api.log")

class ParameterError(Exception):
    def __init__(self, message: str):
        self.error = 'parameter_error'
        self.error_description = message

class GithubError(Exception):
    def __init__(self, error: str, error_description: str, error_uri: str):
        self.error = error
        self.error_description = error_description
        self.error_uri = error_uri

class GithubOAuthError(GithubError):
    pass

class GithubAccessTokenError(GithubError):
    pass

class GithubUserInfoError(GithubError):
    pass

class RequestHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        content_length = int(self.headers.get('Content-Length', '0'))
        url_object = urlparse(self.path)
        path = url_object.path

        if path == '/api/v1/login/github':
            try:
                body = json.loads(self.rfile.read(content_length).decode('utf-8'))
            except Exception as e:
                body = {}
                logger.error(f'read body error: {e}')

            try:
                code = body.get('code')
                if not code:
                    logger.error(f'code is invalid, code={code}')
                    raise ParameterError('code is required')

                logger.log(f'get access token, code={code}')

                # 获取 access_token
                github_oauth_client_instance = github_oauth_client(GITHUB_CLIENT_ID, GITHUB_CLIENT_SECRET, GITHUB_REDIRECT_URI, code)
                access_token = github_oauth_client_instance.get_access_token()
                logger.log(f'get access token success, access_token={access_token}')
                
                # 获取用户信息
                github_user_api_client_instance = github_user_api_client(access_token)       
                user_info_response_json = github_user_api_client_instance.get_user_info_json()

                avatar_url = user_info_response_json.get('avatar_url')
                user_name = user_info_response_json.get('name')
                logger.log(f'get user info success, avatar_url={avatar_url}, user_name={user_name}')

                self.respond_html(200, f'<div style="display: flex; align-items: center;">Welcome, <img src="{avatar_url}" width="20" height="20" /> <span>{user_name}</span></div>')

            except exceptions.ConnectionError as e:
                logger.error(f'connection error: {e}')
                self.respond_json(500, {
                    'error': 'connection_error',
                })

            except exceptions.Timeout as e:
                logger.error(f'timeout error: {e}')
                self.respond_json(500, {
                    'error': 'timeout_error',
                })

            except exceptions.HTTPError as e:
                logger.error(f'http error: {e}')
                self.respond_json(e.response.status_code, {
                    'error': 'http_error',
                    'error_description': e.response.reason,
                })

            except ParameterError as e:
                logger.error(f'parameter error: {e}')
                self.respond_json(400, {
                    'error': e.error,
                    'error_description': e.error_description,
                })

            except GithubAccessTokenError as e:
                logger.error(f'request github access token error: {e}')
                self.respond_json(500, {
                    'error': e.error,
                    'error_description': e.error_description,
                })

            except GithubUserInfoError as e:
                logger.error(f'request github user info error: {e}')
                self.respond_json(500, {
                    'error': e.error,
                    'error_description': e.error_description,
                })

            except Exception as e:
                logger.error(f'unknown error: {e}')
                self.respond_json(500, {
                    'error': 'unknown_error',
                })
        else:
            self.respond_html(404, '<pre>404 not found</pre>')

    def do_GET(self):
        self.respond_html(404, '<pre>404 not found</pre>')

    def respond_html(self, code: int, html: str):
        self.send_response(code)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(bytes(html, 'utf-8'))

    def respond_json(self, code: int, data):
        self.send_response(code)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(bytes(json.dumps(data), 'utf-8'))


if __name__ == '__main__':
    server_address = ('localhost', 8100)
    httpd = HTTPServer(server_address, RequestHandler)
    print('Starting server...')
    httpd.serve_forever()