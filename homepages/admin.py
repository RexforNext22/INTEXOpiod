from django.contrib import admin

from .models import State 
from .models import Prescriber, Drug, Triple

admin.site.register(State)
admin.site.register(Prescriber)
admin.site.register(Drug)
admin.site.register(Triple)