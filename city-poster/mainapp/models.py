from django.conf import settings
from django.db import models


class CompanyProfile(models.Model):
    name = models.CharField(max_length=512, verbose_name='Наименование компани')
    type = models.CharField(max_length=512, verbose_name='Тип компани')
    address = models.CharField(max_length=512, verbose_name='Адрес компани')

    def __str__(self):
        return f"{self.name} ({self.type})"


class EventCategory(models.Model):
    name = models.CharField(max_length=512, verbose_name='Тип события')

    def __str__(self):
        return f"{self.pk}. {self.name}"


class Event(models.Model):
    name = models.CharField(max_length=512, verbose_name='Наименование события')
    poster = models.ImageField(upload_to=settings.MEDIA_POSTER_IMAGE_FOLDER, verbose_name='Картинка-постер события')
    description = models.TextField(verbose_name='Описание события')
    date = models.DateTimeField()
    source = models.CharField(max_length=512, verbose_name='Источник события')

    def __str__(self):
        return f"{self.pk} событие {self.name}"
