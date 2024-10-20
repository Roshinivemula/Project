# weather/services.py

import requests
from datetime import datetime
from .models import Weather, Alert

API_KEY = 'your_openweathermap_api_key'
CITIES = ['Delhi', 'Mumbai', 'Chennai', 'Bangalore', 'Kolkata', 'Hyderabad']

def fetch_weather_data():
    weather_data = []
    for city in CITIES:
        url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}'
        response = requests.get(url)
        data = response.json()

        # Extract relevant data
        main_weather = data['weather'][0]['main']
        temp_kelvin = data['main']['temp']
        feels_like_kelvin = data['main']['feels_like']
        timestamp = data['dt']

        # Convert temperatures from Kelvin to Celsius
        temp_celsius = temp_kelvin - 273.15
        feels_like_celsius = feels_like_kelvin - 273.15

        # Calculate daily aggregates (simplified for example purposes)
        weather_data.append({
            'city': city,
            'timestamp': timestamp,
            'temp': temp_celsius,
            'feels_like': feels_like_celsius,
            'weather': main_weather
        })
    return weather_data

def process_and_store_weather_data():
    data = fetch_weather_data()
    for entry in data:
        # Get or create Weather summary for the current day
        date = datetime.utcfromtimestamp(entry['timestamp']).date()
        weather_summary, created = Weather.objects.get_or_create(
            city=entry['city'],
            date=date,
            defaults={'avg_temp': entry['temp'], 'max_temp': entry['temp'], 'min_temp': entry['temp'], 'dominant_weather': entry['weather']}
        )

        # Update aggregates for the day
        if not created:
            weather_summary.avg_temp = (weather_summary.avg_temp + entry['temp']) / 2
            weather_summary.max_temp = max(weather_summary.max_temp, entry['temp'])
            weather_summary.min_temp = min(weather_summary.min_temp, entry['temp'])
            weather_summary.dominant_weather = entry['weather']
            weather_summary.save()

        # Check for alert thresholds (e.g., if temperature > 35°C)
        if entry['temp'] > 35:
            Alert.objects.create(city=entry['city'], temperature=entry['temp'], condition="High Temperature")

