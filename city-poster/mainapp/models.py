from django.conf import settings
from django.db import models

NULLABLE = {'null': True, 'blank': True}


class CompanyProfile(models.Model):
    name = models.CharField(max_length=512, verbose_name='Наименование компани')
    type = models.CharField(max_length=512, verbose_name='Тип компани')
    address = models.CharField(max_length=512, verbose_name='Адрес компани')
    company_url = models.URLField(max_length=256, verbose_name='Сайт компани', unique=True)

    class Meta:
        verbose_name = 'Площадка события'
        verbose_name_plural = 'Площадки события'

    def __str__(self):
        return f"{self.name} ({self.type})"


class EventCategory(models.Model):
    name = models.CharField(max_length=512, verbose_name='Тип события')

    class Meta:
        verbose_name = 'Категория события'
        verbose_name_plural = 'Категории события'

    def __str__(self):
        return f"{self.pk}. {self.name}"


class EventTags(models.Model):
    name = models.CharField(max_length=128, verbose_name='Тег события')

    class Meta:
        verbose_name = 'Тег события'
        verbose_name_plural = 'Теги события'

    def __str__(self):
        return f"{self.pk} событие {self.name}"


class Event(models.Model):
    name = models.CharField(max_length=512, verbose_name='Наименование события')
    poster = models.ImageField(upload_to=settings.MEDIA_POSTER_IMAGE_FOLDER, verbose_name='Картинка-постер события',
                               **NULLABLE)
    description = models.TextField(verbose_name='Описание события')
    source = models.CharField(max_length=512, verbose_name='Источник события')
    event_venue = models.ForeignKey(
        CompanyProfile,
        on_delete=models.SET_NULL,
        verbose_name='Площадка события',
        related_name='events',
        **NULLABLE
    )
    categorys = models.ManyToManyField(EventCategory, related_name='events')
    tags = models.ManyToManyField(EventTags, related_name='events')

    class Meta:
        verbose_name = 'Событие'
        verbose_name_plural = 'События'

    def __str__(self):
        return f"{self.pk} событие {self.name}"


class EventDatetime(models.Model):
    date = models.DateTimeField(verbose_name='Дата и время события')
    event = models.ForeignKey(
        Event,
        on_delete=models.CASCADE,
        related_name='event_datetime',
        verbose_name='Событие'
    )

    class Meta:
        verbose_name = 'Дата и время события'
        verbose_name_plural = 'Дата и время события'

    def __str__(self):
        return f"{self.date} ({self.event.name})"
