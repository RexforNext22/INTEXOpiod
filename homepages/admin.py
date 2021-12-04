from django.contrib import admin

from .models import State 
from .models import Prescriber, Drug, Triple, Credential, CredPres

# Register the models for the admin
admin.site.register(State)
admin.site.register(Prescriber)
admin.site.register(Drug)
admin.site.register(Triple)
admin.site.register(Credential)
admin.site.register(CredPres)