class GithubError(Exception):
    def __init__(self, error: str, error_description: str, error_uri: str):
        self.error = error
        self.error_description = error_description
        self.error_uri = error_uri

class GithubAccessTokenError(GithubError):
    pass

class GithubUserInfoError(GithubError):
    pass