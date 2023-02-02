import unittest
from datetime import datetime


# from ugra_classic_event_scrapper import UgraClassicEventScrapper


class TestStringMethods(unittest.TestCase):

    # string_date='24 и 25 марта' string_time='19:00, 15:00'
    # [(datetime.datetime(2023, 3, 24, 0, 0), False), (datetime.datetime(2023, 3, 25, 0, 0), False)]
    # --------------------
    # string_date='18 марта' string_time='18:00'
    # [(datetime.datetime(2023, 3, 18, 18, 0), True)]
    # --------------------
    # string_date='9 и 10 марта' string_time='19:00'
    # [(datetime.datetime(2023, 3, 9, 0, 0), False), (datetime.datetime(2023, 3, 10, 0, 0), False)]
    # def test_private_get_event_datetime_list(self):
    #     scrapper_class = UgraClassicEventScrapper()
    #     expected = [(datetime(2023, 3, 24, 0, 0), False), (datetime(2023, 3, 25, 0, 0), False)]
    #     actual = scrapper_class._UgraClassicEventScrapper__get_event_datetime_list(
    #         string_date="24 и 25 марта",
    #         string_time="19:00, 15:00"
    #     )
    #     self.assertEqual(expected, actual)

    def test_some(self):
        self.assertEqual(True, True)


if __name__ == '__main__':
    unittest.main()
