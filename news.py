import requests
from dotenv import load_dotenv
import os

load_dotenv()

news_api_key = os.getenv("NEWS_API_KEY")   

def get_news():
    url = "https://newsapi.org/v2/top-headlines?country=us&apiKey=" + news_api_key
    response = requests.get(url)
    data = response.json()  

    articles = data["articles"]

    print("Here are the top headlines for today, sir:")
    for i, article in enumerate(articles[:5]):
        print(str(i+1) + ". " + article["title"])

get_news()