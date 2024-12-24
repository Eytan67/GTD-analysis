import requests
import time
from app.config import EVENT_REGISTRY_URL
from app.realtime_server.grok import classify_news_article
from app.realtime_server.mongodb import collection



def fetch_articles(page):
    response = requests.get(f"{EVENT_REGISTRY_URL}{page}")
    if response.status_code == 200:
        return response.json().get('articles')
    else:
        print(f"Error fetching articles: {response.status_code}")
        return []

def extract_relevant_data(data):
    extracted = {
        "dt": data.get("dateTime"),
        "title": data.get("title"),
        "body": data.get("body", ""),
        "first_200_words": " ".join(data.get("body", "").split()[:200])
    }

    return extracted

def main():
    articles_page = 1
    while True:
        articles = fetch_articles(articles_page)
        if not articles:
            break
        results = articles.get("results")

        for article in results[:3]:
            skin_article = extract_relevant_data(article)
            Condensation = classify_news_article(skin_article)
            result = {
                'classification': Condensation.get('classification'),
                'location': Condensation.get('location'),
                'latitude': Condensation.get('location'),
                'longitude': Condensation.get('location'),
                'dt': skin_article.get('dt'),
                'title': skin_article.get('title'),
                'body': skin_article.get('body'),
                'new_data': True
            }
            print(result)
            collection.insert_one(result)

        articles_page += 1
        time.sleep(120)

if __name__ == "__main__":
    main()