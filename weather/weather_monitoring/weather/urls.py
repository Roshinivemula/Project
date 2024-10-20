# weather/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('weather_plot/<str:city>/', views.weather_plot, name='weather_plot'),
]
