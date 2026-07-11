import requests
from dotenv import load_dotenv
import os
import sqlite3

load_dotenv()
api_key = os.getenv("WEATHER_API_KEY")
conn = sqlite3.connect("jarvis_memory.db")
cursor = conn.cursor()

def get_weather(city):
    url = "https://api.openweathermap.org/data/2.5/weather?q=" + city + "&appid=" + api_key + "&units=metric"

    response = requests.get(url)
    data = response.json()

    if data.get("cod") != 200:
        return "Sorry sir, I couldn't find the weather for " + str(data.get("message", "Unknown error"))
    else:
        temp = data["main"]["temp"]
        condition = data["weather"][0]["description"]
        humidity = data["main"]["humidity"]

        return "Sir, the weather in " + city + " is " + condition + ". Temperature: " + str(temp) + "°C. Humidity: " + str(humidity) + "%"

def get_preferred_city():
    cursor.execute("SELECT content FROM memory WHERE topic = 'preferred city'")
    result = cursor.fetchone()

    if result:
        return result[0]
    else:
        return None

if __name__ == "__main__":
    city = get_preferred_city()
    if city:
        print("Welcome back, sir. Fetching weather for your preferred city: " + city)
    else:
        city = input("Which city should I search for, sir? ")
        cursor.execute("INSERT INTO memory (topic, content) VALUES (?, ?)", ("preferred city", city))
        conn.commit()
        print("Got it sir, I'll remember that.")

    print(get_weather(city))