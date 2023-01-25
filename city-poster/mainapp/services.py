from abc import ABC, abstractmethod
from enum import Enum

import requests
from lxml.html import fromstring, Element
from tqdm import tqdm


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


class AbstractScrapper(ABC):
    _news_list = []

    def __init__(self):
        print(f"Начал работать {self.__class__}")

    @abstractmethod
    def start_scraping(self):
        """Start scraping process."""
        pass


class UgraClassicEventScrapper(AbstractScrapper):
    BASE_URL = "https://ugraclassic.ru/events/index.php"

    EVENT_ITEMS_XPATH = "//div[contains(@class, 'afisha__item')]"
    PART_EVENT_TITLE_XPATH = "//div[contains(@class, 'afisha-desc')]/h3//text()"
    # PART_EVENT_DATE_XPATH = "//ul[contains(@class, 'afisha-w')]//text()"
    PART_SCHEDULE_XPATH = "//ul[contains(@class, 'afisha-w')]"

    def start_scraping(self):
        request_headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36"
        }

        dom = fromstring(HTTPResponse.get_response(url=self.BASE_URL, headers=request_headers).text)
        item_event_title = dom.xpath(self.EVENT_ITEMS_XPATH + self.PART_EVENT_TITLE_XPATH)
        schedule_item = dom.xpath(self.EVENT_ITEMS_XPATH + self.PART_SCHEDULE_XPATH)
        schedule_mix = dom.xpath(self.EVENT_ITEMS_XPATH + self.PART_SCHEDULE_XPATH + "//li[contains(@class, 'afisha-w__item')]//text()")
        # Удалим пробелы в строках элементов и пустые элементы
        schedule_mix = list(filter(None, [x.strip() for x in schedule_mix]))
        print(len(item_event_title), item_event_title)
        print(len(schedule_item), schedule_item)
        print(len(schedule_mix), schedule_mix)

        for item in schedule_item:
            print(len(item), item)



if __name__ == "__main__":
    UgraClassicEventScrapper().start_scraping()
