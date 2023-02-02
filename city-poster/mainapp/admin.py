from django.contrib import admin

from mainapp.models import (CompanyProfile, Event, EventCategory,
                            EventDatetime, EventTags)

admin.site.register(CompanyProfile)
admin.site.register(EventCategory)
admin.site.register(Event)
admin.site.register(EventDatetime)
admin.site.register(EventTags)
