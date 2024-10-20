import io
import matplotlib
matplotlib.use('Agg')  # Use the Agg backend (non-GUI)

import matplotlib.pyplot as plt
from django.http import HttpResponse
from .models import Weather
from datetime import datetime

def weather_plot(request, city):
    # Query the weather data for the given city (example: Delhi)
    weather_data = Weather.objects.filter(city=city).order_by('date')
    
    # Prepare the data for plotting
    dates = [entry.date for entry in weather_data]
    temps = [entry.avg_temp for entry in weather_data]
    
    # Create a plot
    fig, ax = plt.subplots()
    ax.plot(dates, temps, label='Average Temperature')
    
    ax.set(xlabel='Date', ylabel='Temperature (°C)', title=f'Weather Plot for {city}')
    ax.grid(True)
    plt.xticks(rotation=45)
    
    # Save the plot into a BytesIO object instead of displaying it
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)  # Rewind the buffer to the beginning
    
    # Return the plot as an image response
    return HttpResponse(buf, content_type='image/png')
