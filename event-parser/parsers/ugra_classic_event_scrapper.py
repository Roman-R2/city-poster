import locale
from dataclasses import dataclass
from datetime import datetime
from lxml.html import fromstring, tostring

from abstracts import AbstractScrapper
from services import HTTPResponse, RequestHeaders, MonthTitleReplace


@dataclass
class UgraClassicEventItem:
    name: str
    description: str
    source: str
    datetime_list: list
    event_venue: str = ''
    poster: str = ''
    categorys: str = ''  # ManyToManyField
    tags: str = ''  # ManyToManyField


class UgraClassicEventScrapper(AbstractScrapper):
    INDEX_URL = 'https://ugraclassic.ru'

    BASE_URL = "https://ugraclassic.ru/events/index.php"

    PAGINATOR_XPATH = "//div[contains(@class, 'bx_pagination_page')]//li/a/@href"

    AGE_TAG_XPATH = "//div[@class='age']//text()"

    EVENT_ITEMS_XPATH = "//div[contains(@class, 'afisha__item')]"
    PART_EVENT_TITLE_XPATH = "//div[contains(@class, 'afisha-desc')]/h3//text()"
    PART_EVENT_HREF_XPATH = "/a/@href"
    PART_SCHEDULE_XPATH = "//ul[contains(@class, 'afisha-w')]"

    EVENT_ADDITION_DATA_XPATH = "//div[contains(@class, 'afisha-detail__text')]//text()"

    def __init__(self):
        super().__init__()
        locale.setlocale(locale.LC_ALL, 'ru_RU.UTF-8')
        self.parse_result: list = []

    def __clean_xpath_generated_list(self, data: list):
        data = [x.strip() for x in data]
        data = [x.replace('\xa0', ' ') for x in data]
        return list(filter(None, [x.strip() for x in data]))

    def __clean_xpath_generated_list_for_description(self, data: list):
        data = [x.strip('\t ') for x in data]
        data = [x.replace('\n', '<br>') for x in data]
        data = [x.replace('\xa0', ' ') for x in data]
        return list(filter(None, [x.strip() for x in data]))

    def __get_formated_datetime(self, non_format_string: str):
        return datetime.strptime(
            MonthTitleReplace.for_russian_words(non_format_string),
            "%d %B%Y%H:%M"
        )

    def __get_event_datetime_list(self, string_date: str, string_time: str) -> list:
        event_times = []
        # print(f"{string_date=} {string_time=}")

        # Если дата составная то это ничего не значит для данного источника событий (путаница)
        # is_right_time  = False значит учитывать только дату, так как время с большой вероятностью неверное
        is_right_time = True
        if '; ' in string_time or ', ' in string_time:
            string_time = "00:00"
            is_right_time = False
        if ' и ' in string_date:
            string_time = "00:00"
            is_right_time = False
            string_date_list = string_date.split(' и ')
            month = string_date_list[-1].split(' ')[-1]
            for i in range(len(string_date_list)):
                event_times.append((
                    self.__get_formated_datetime(
                        non_format_string=(string_date_list[i] if i + 1 == len(
                            string_date_list) else string_date_list[i] + ' ' + month) + datetime.now().strftime(
                            '%Y') + string_time
                    ), is_right_time)
                )
            pass
        else:
            event_times.append((
                self.__get_formated_datetime(
                    non_format_string=string_date + datetime.now().strftime('%Y') + string_time
                ), is_right_time)
            )
        # print('--> ', event_times)
        return event_times

    def __get_events_from_one_page(self, url: str):
        """ Append all events to self.parse_result for requested url. """
        dom = fromstring(HTTPResponse.get_response(url=url, headers=RequestHeaders().headers).text)

        item_event_title = dom.xpath(self.EVENT_ITEMS_XPATH + self.PART_EVENT_TITLE_XPATH)
        item_event_href = dom.xpath(self.EVENT_ITEMS_XPATH + self.PART_EVENT_HREF_XPATH)
        schedule_item = dom.xpath(self.EVENT_ITEMS_XPATH + self.PART_SCHEDULE_XPATH)
        schedule_mix_list = dom.xpath(
            self.EVENT_ITEMS_XPATH + self.PART_SCHEDULE_XPATH + "//li[contains(@class, 'afisha-w__item')]//text()")
        # Удалим пробелы в строках элементов и пустые элементы
        schedule_mix_list = self.__clean_xpath_generated_list(schedule_mix_list)

        for item in schedule_item:
            temp_date = ''
            temp_time = ''
            temp_title = item_event_title.pop(0)
            temp_href = self.INDEX_URL + item_event_href.pop(0)
            for i in range(len(item)):
                if i == 0:
                    schedule_mix_list.pop(0)
                    temp_date = schedule_mix_list.pop(0)
                elif i == 1:
                    schedule_mix_list.pop(0)
                    temp_time = schedule_mix_list.pop(0)
                else:
                    schedule_mix_list.pop(0)
                    schedule_mix_list.pop(0)

            event_page = self.__get_event_page(temp_href)

            event_description = event_page.xpath(self.EVENT_ADDITION_DATA_XPATH)
            event_tag = event_page.xpath(self.AGE_TAG_XPATH)
            event_description = ''.join(
                self.__clean_xpath_generated_list_for_description(event_description)).replace(
                '                ', ' '
            ).replace('<br><br>', '<br>')

            self.parse_result.append(
                UgraClassicEventItem(
                    name=temp_title,
                    description=event_description,
                    source=temp_href,
                    datetime_list=self.__get_event_datetime_list(temp_date, temp_time),
                    tags=event_tag
                )
            )

    def __get_event_page(self, url: str):
        """ Send request for event url and get event data. """
        with HTTPResponse.get_response(url, headers=RequestHeaders().headers) as get_request:
            return fromstring(get_request.text)

    def start_scraping(self):

        dom = fromstring(HTTPResponse.get_response(url=self.BASE_URL, headers=RequestHeaders().headers).text)

        pagination = dom.xpath(self.PAGINATOR_XPATH)
        event_page_url_set = set()
        for item in pagination:
            event_page_url_set.add(self.INDEX_URL + item)

        for page_url in event_page_url_set:
            self.__get_events_from_one_page(page_url)

        return self.parse_result


if __name__ == "__main__":
    print(f"{__file__} must include as module.")
    UgraClassicEventScrapper().start_scraping()
