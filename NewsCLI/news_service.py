from db import conn
from newsapi import NewsApiClient
import requests
import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("NEWS_API_KEY")
if not API_KEY:
    print("ERROR: NEWS_API_KEY not found in .env file")
    exit(1)

newsapi = NewsApiClient(API_KEY)

db = conn.news
all_news_collection = db.get_news
top_news_collection = db.top_news
breaking_news_collection = db.breaking_news

def get_news():
    c1 = input("Enter the title of the news article: ")
    c2 = input("Sort article by (popularity/relevancy): ")
    url = "https://newsapi.org/v2/everything?"
    
    params = {
        "q": c1,
        "sortBy":c2,
        "apiKey": API_KEY,
        "pageSize":10,
    }

    response = requests.get(url, params=params)

    if response.status_code == 200:
        data = response.json()
        for i, article in enumerate(data.get("articles", []), 1):
            all_news_collection.insert_one(article)
            print(f"{i}. {article['title']} ({article['source']['name']})")
            print(article['url'])
            print()
    else:
        print("Failed to fetch news:", response.status_code, response.text)


def top_headlines():
        
        c1 = input("Enter the title of the news article: ")
        c3 = input("Enter the language of the news article: ")
        c4 = input("Enter the country of the news article: ")
        url = ('https://newsapi.org/v2/top-headlines')

        params = {
        "q": c1,
        "language": c3,
        "country": c4,
        "apiKey": API_KEY
    }
        response = requests.get(url, params=params)
        
        if response.status_code == 200:
            data = response.json()
        
            for i, article in enumerate(data.get("articles", []), 1):
             top_news_collection.insert_one(article)
             print(f"{i}. {article['title']} ({article['source']['name']})")
             print(article['url'])
             print()
       
        else:
         print("Failed to fetch news:", response.status_code, response.text)


def breaking_headlines():
    c1 = input("Enter the name of your country (2 letter initial): ")
    url = "https://newsapi.org/v2/top-headlines"
    params = {
        "country": c1,
        "apiKey": API_KEY
    }

    response = requests.get(url, params=params)

    if response.status_code == 200:
        data = response.json()
        for i, article in enumerate(data.get("articles", []), 1):
            breaking_news_collection.insert_one(article)
            print(f"{i}. {article['title']} ({article['source']['name']})")
            print(article['url'])
            print()
    else:
        print("Failed to fetch news:", response.status_code, response.text)

sources = newsapi.get_sources()

