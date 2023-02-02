import sys
import unittest
from datetime import datetime

from parsers.ugra_classic_event_scrapper import \
    UgraClassicEventScrapperToolsMixin


class TestStringMethods(unittest.TestCase):

    def test_private_get_event_datetime_list(self):
        test_params = (
            (
                {"string_date": "24 и 25 марта", "string_time": "19:00, 15:00"},
                [(datetime(2023, 3, 24, 0, 0), False), (datetime(2023, 3, 25, 0, 0), False)]
            ),
            (
                {"string_date": "18 марта", "string_time": "18:00"},
                [(datetime(2023, 3, 18, 18, 0), True)]
            ),
            (
                {"string_date": "9 и 10 марта", "string_time": "19:00"},
                [(datetime(2023, 3, 9, 0, 0), False), (datetime(2023, 3, 10, 0, 0), False)]
            ),
        )
        for test_data, expected in test_params:
            actual = UgraClassicEventScrapperToolsMixin()._get_event_datetime_list(
                **test_data
            )
            self.assertEqual(expected, actual)


if __name__ == '__main__':
    # print(vars().keys())
    unittest.main()
