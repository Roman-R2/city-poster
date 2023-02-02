from enum import Enum

import requests


class Status:
    """HTTP statuses"""

    NOT_FOUND_404 = 404
    OK_200 = 200


class FileMode(Enum):
    """ DTO for file mod  """
    READ = "r"
    WRITE = "w"
    APPEND_WRITE = "a"


class HTTPResponse:
    def __init__(self, url: str, response_headers=None, response_params=None):
        self.url = url
        self.headers = response_headers
        self.params = response_params

    def __get_response(self):
        response = requests.get(self.url, headers=self.headers, params=self.params)
        if response.status_code != Status.OK_200:
            print(f"{self.url=}\n{self.headers=}\n{self.params}")
            raise ConnectionError(
                f"HTTP status not 200. Server return "
                f"{response.status_code} status code for "
                f"url {self.url}"
            )
        return response

    @staticmethod
    def get_response(url: str, headers=None, params=None):
        return HTTPResponse(url, headers, params).__get_response()


class RequestHeaders:
    _canvas_headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36"
    }

    @property
    def headers(self):
        return self._canvas_headers


class MonthTitleReplace:
    def __init__(self, month_string: str):
        self.month_string = month_string

    def __for_russian_words(self):
        self.month_string = self.month_string.replace('февраля', 'февраль')
        self.month_string = self.month_string.replace('марта', 'март')
        return self.month_string

    @staticmethod
    def for_russian_words(month_string: str):
        return MonthTitleReplace(month_string).__for_russian_words()
