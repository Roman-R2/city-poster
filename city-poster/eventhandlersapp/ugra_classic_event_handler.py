from mainapp.models import CompanyProfile
from mainapp.services import UgraClassicEventScrapper


class UgraClassicEventHandler:
    palace_name = 'КТЦ Югра-Классик'

    def start(self):
        event_venue = CompanyProfile.objects.get(name=self.palace_name)

        # events = UgraClassicEventScrapper().start_scraping()

        # print(events)


if __name__ == "__main__":
    pass
