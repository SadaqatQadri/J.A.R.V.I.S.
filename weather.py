import requests
from dotenv import load_dotenv
import os

load_dotenv()
api_key = os.getenv("WEATHER_API_KEY")
def get_weather(city):
  
    url = "https://api.openweathermap.org/data/2.5/weather?q=" + city + "&appid=" + api_key + "&units=metric"

    response = requests.get(url)
    data = response.json()

    if data.get ("cod") != 200:
        print("Sorry sir, I couldnt find the weather for " + str(data.get("message", "Unknown error")))
    else:    
        temp = data["main"]["temp"]
        condition = data["weather"][0]["description"]
        humidity = data ["main"]["humidity"]
    
        print("Sir, the weather in " + city + " is " + condition)
        print("Temperature: " + str(temp) + "°C")
        print("Humidity: " + str(humidity) + "%")

city = input("Which city should I search for, sir?")
get_weather(city)
another = input("Would you like to check the weather for another city? (yes/no): ").strip().lower()
if another == "yes":
    city2 = input("Which city, sir?")
    get_weather(city2)