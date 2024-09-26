from requests import post
from GithubError import GithubAccessTokenError

class github_oauth_client:
    def __init__(self, client_id: str, client_secret: str, redirect_uri: str,code: str):
        self.access_token_request_data = {
            'client_id': client_id,
            'client_secret': client_secret,
            'redirect_uri': redirect_uri,
            'code': code,
        }
        self.access_token_url = "https://github.com/login/oauth/access_token"

    def get_access_token(self):
        access_token_response = post(self.access_token_url, data=self.access_token_request_data, headers={ 'Accept': 'application/json' })
        access_token_response.raise_for_status()
        access_token_response_json = access_token_response.json()

        get_access_token_error = access_token_response_json.get('error')
        get_access_token_error_description = access_token_response_json.get('error_description')
        if get_access_token_error:
            raise GithubAccessTokenError(get_access_token_error, get_access_token_error_description,self.access_token_url)

        access_token = access_token_response_json.get('access_token')
        return access_token