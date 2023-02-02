from django.core.management import BaseCommand
from mainapp.models import CompanyProfile


class Command(BaseCommand):
    EVENTS_COMPANYS = [
        {
            'name': 'КТЦ Югра-Классик',
            'type': 'Концертно-театральный центр',
            'address': 'г. Ханты-Мансийск, ул. Мира, 22.',
            'company_url': 'ugraclassic.ru'
        },
    ]

    def handle(self, *args, **options):
        for item in self.EVENTS_COMPANYS:
            if not CompanyProfile.objects.filter(**item).exists():
                CompanyProfile.objects.create(**item)
                print(f"Создана площадка {item['name']}")
            else:
                print(f"Площадка {item['name']} уже имеется в БД")
