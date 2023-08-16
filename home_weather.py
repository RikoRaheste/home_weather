import requests
import pandas as pd
import schedule
from datetime import datetime
import os

# Add your own Weather API api key and selected coordinates (or a city name)
api_key = ''
coordinates = ''
csv_file_path = 'home_weather_data.csv'
weather_data = []

if not os.path.exists(csv_file_path):
    df = pd.DataFrame(columns=["time", "wind_kph", "temp_c", "humidity", "daily_chance_of_rain"])
    df.to_csv(csv_file_path, index=False)

# Request weather data and store/return it as a library
def fetch_weather_data():

    request = requests.get(
        f"http://api.weatherapi.com/v1/forecast.json?key={api_key}&q={coordinates}&days=3&aqi=yes&alerts=no")
    
    weather_data = pd.DataFrame(request.json())
   # '%H:%M:%S' to get the time as hours, minutes, seconds
    weather = {
        "time": datetime.now().strftime("%H:%M"),
        "temp_c": weather_data['current']['temp_c'],
        "wind_kph": weather_data['current']['wind_kph'],
        "humidity": weather_data['current']['humidity']}
    
    return weather

# Read and append weather data to a .csv file
def fetch_store_data():
    try:
        weather = fetch_weather_data()
        weather_data.append(weather)
        print("Weather data fetched and updated:", weather)

        # Append new data to DataFrame and save it to CSV
        df = pd.DataFrame(weather_data)
        df.to_csv(csv_file_path, index=False)
        
        
        
    except Exception as e:
        print("An error occurred:", e)

# Run the task every hour
schedule.every(1).hour.do(fetch_store_data)

# Main loop
while True:
    schedule.run_pending()