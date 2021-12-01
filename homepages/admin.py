from django.contrib import admin

from .models import StateData, Prescriber, Drug

admin.site.register(StateData)
admin.site.register(Prescriber)
admin.site.register(Drug)