import datetime
import time

import schedule
from django.conf import settings

from event_handlers.ugra_classic_event_handler import UgraClassicEventHandler

if __name__ == '__main__':
    # locale.setlocale(locale.LC_ALL, 'ru_RU.UTF-8')
    # schedule.every().minute.do(job)
    # schedule.every(1).days.do(job)

    schedule.every().day.at(settings.UGRA_CLASSIC_HARVEST_TIME).do(UgraClassicEventHandler.start())

    print(f'Запустили задачу {schedule.jobs}')

    while True:
        schedule.run_pending()
        print(datetime.datetime.now(), schedule.jobs)
        time.sleep(1)
