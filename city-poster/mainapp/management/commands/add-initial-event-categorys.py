from django.core.management import BaseCommand

from mainapp.models import EventCategory


class Command(BaseCommand):
    EVENTS_CATEGORYS = [
        'Кино',
        'Концерт',
        'Театр',
        'Детям',
        'Шоу',
    ]

    def handle(self, *args, **options):
        for item in self.EVENTS_CATEGORYS:
            if not EventCategory.objects.filter(name=item).exists():
                EventCategory.objects.create(name=item)
                print(f"Создана категория {item}")
            else:
                print(f"Категория {item} уже имеется в БД")
