# weather/apps.py

from django.apps import AppConfig

class WeatherConfig(AppConfig):
    name = 'weather'

    def ready(self):
        from .tasks import start_weather_scheduler
        start_weather_scheduler()
