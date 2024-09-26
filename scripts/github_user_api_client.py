from requests import get
from GithubError import GithubUserInfoError

class github_user_api_client:
    def __init__(self, token):
        self.token = token
        self.base_url = 'https://api.github.com/user'

    def get_user_info_json(self):
        user_info_response = get(self.base_url, headers={ 'Authorization': f'Bearer {self.token}' })
        user_info_response.raise_for_status()
        user_info_response_json = user_info_response.json()
        
        get_user_info_error = user_info_response_json.get('error')
        get_user_info_error_description = user_info_response_json.get('error_description')
        if get_user_info_error:
            raise GithubUserInfoError(get_user_info_error, get_user_info_error_description, self.base_url)
        return user_info_response_json