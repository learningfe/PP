from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
from requests import post, get, exceptions
from Logger import Logger
import json

# Read secret from environment variable or something else
GITHUB_CLIENT_ID = ''
GITHUB_CLIENT_SECRET = ''
GITHUB_REDIRECT_URI = 'http://localhost:8100/api/v1/oauth/github'
GITHUB_ACCESS_TOKEN_URL = 'https://github.com/login/oauth/access_token'
GITHUB_USER_API = 'https://api.github.com/user'


logger = Logger("api.log")

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
            logger.log(f'user login')

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
                access_token_request_data = {
                    'client_id': GITHUB_CLIENT_ID,
                    'client_secret': GITHUB_CLIENT_SECRET,
                    'redirect_uri': GITHUB_REDIRECT_URI,
                    'code': code,
                }
                access_token_response = post(GITHUB_ACCESS_TOKEN_URL, data=access_token_request_data, headers={ 'Accept': 'application/json' })
                access_token_response.raise_for_status()
                access_token_response_json = access_token_response.json()

                # 获取 AccessToken 失败
                get_access_token_error = access_token_response_json.get('error')
                get_access_token_error_description = access_token_response_json.get('error_description')
                if get_access_token_error:
                    raise GithubAccessTokenError(get_access_token_error, get_access_token_error_description)

                access_token = access_token_response_json.get('access_token')

                logger.log(f'access_token: {access_token}')

                user_info_response = get(GITHUB_USER_API, headers={ 'Authorization': f'Bearer {access_token}' })
                user_info_response.raise_for_status()
                user_info_response_json = user_info_response.json()

                # 获取用户信息失败
                get_user_info_error = user_info_response_json.get('error')
                get_user_info_error_description = user_info_response_json.get('error_description')
                if get_user_info_error:
                    raise GithubUserInfoError(get_user_info_error, get_user_info_error_description)

                avatar_url = user_info_response_json.get('avatar_url')
                user_name = user_info_response_json.get('name')

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