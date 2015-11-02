from django.contrib import admin

from .models import About, AllRequest, SignalData

admin.site.register(About)
admin.site.register(SignalData)
admin.site.register(AllRequest)
