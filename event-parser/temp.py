import locale
from datetime import datetime

locale.setlocale(locale.LC_ALL, 'ru_RU.UTF-8')

print(locale.locale_alias)

print(f"{locale.LC_ALL=}")

string = "3 Февраля 2023"

result = datetime.strptime(string, "%d %B %Y")

print(result)
