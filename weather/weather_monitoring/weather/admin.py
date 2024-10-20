# weather/admin.py

from django.contrib import admin
from .models import Weather, Alert

admin.site.register(Weather)
admin.site.register(Alert)
