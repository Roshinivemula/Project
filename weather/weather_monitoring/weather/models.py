# weather/models.py

from django.db import models

class Weather(models.Model):
    city = models.CharField(max_length=50)
    date = models.DateField()
    avg_temp = models.FloatField()
    max_temp = models.FloatField()
    min_temp = models.FloatField()
    dominant_weather = models.CharField(max_length=50)

    def __str__(self):
        return f"Weather data for {self.city} on {self.date}"

class Alert(models.Model):
    city = models.CharField(max_length=50)
    temperature = models.FloatField()
    condition = models.CharField(max_length=100)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Alert for {self.city}: {self.condition} at {self.temperature}°C"
