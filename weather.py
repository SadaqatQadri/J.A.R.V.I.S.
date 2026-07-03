import requests

api_key = "c0a55dcc88027253b4f76ad28f234425"
city = input("Which city, sir? ")

url = "https://api.openweathermap.org/data/2.5/weather?q=" + city + "&appid=" + api_key + "&units=metric"

response = requests.get(url)
data = response.json()

temp = data["main"]["temp"]
condition = data["weather"][0]["description"]
humidity = data ["main"]["humidity"]

print("Sir, the weather in " + city + " is " + condition)
print("Temperature: " + str(temp) + "°C")
print("Humidity: " + str(humidity) + "%")