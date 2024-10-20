# weather/tasks.py

from apscheduler.schedulers.background import BackgroundScheduler
from .services import process_and_store_weather_data

def start_weather_scheduler():
    scheduler = BackgroundScheduler()
    scheduler.add_job(process_and_store_weather_data, 'interval', minutes=5)
    scheduler.start()
