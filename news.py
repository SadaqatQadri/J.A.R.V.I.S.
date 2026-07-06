import requests
from dotenv import load_dotenv
import os

load_dotenv()

news_api_key = os.getenv("NEWS_API_KEY")

def get_news(country="us", topic=None):
    if topic:
        url = "https://newsapi.org/v2/top-headlines?country=" + country + "&category=" + topic + "&apiKey=" + news_api_key
    else: 
        url = "https://newsapi.org/v2/top-headlines?country=" + country + "&apikey=" + news_api_key

    response = requests.get(url)   
    data = response.json()

    articles = data["articles"]

    if not articles:
        print("No news found for that particular search, sir.")
        return

    print ("Here are the top headlines, sir:")
    for i, article in enumerate(articles[:5]):
        print(str(i+1) + ". " + article["title"])

country = input("Which country would you like me to get the news from, sir? (e.g. us, gb, pk): ")
topic = input("Any specific topic? (technology/business/entertainment/sports/leave blank): ")

if topic == "":
    get_news(country)
else:
    get_news(country, topic)