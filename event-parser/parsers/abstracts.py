from abc import abstractmethod, ABC


class AbstractScrapper(ABC):
    _news_list = []

    def __init__(self):
        print(f"Начал работать {self.__class__}")

    @abstractmethod
    def start_scraping(self):
        """Start scraping process."""
        pass
