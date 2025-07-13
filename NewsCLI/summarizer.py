from google import genai
from db import conn
from newspaper import Article
import os
from dotenv import load_dotenv

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    print("ERROR: GEMINI_API_KEY not found in .env file")
    exit(1)

client = genai.Client(api_key=GEMINI_API_KEY)

db = conn.news
summarizer_collection = db.summarizer

def summarize_news():
    while True:
        print("Available Collections")
        print("1. Queried News")
        print("2. Top Headlines")
        print("3. Breaking Headlines")
        print("0. To exit the app")

        try:
            choice = int(input("Enter Collection ID: "))
            
            if choice == 0:
                print("Goodbye!")
                break
            
            collections = {
                1: db.get_news,
                2: db.top_news,
                3: db.breaking_news,
            }

            if choice not in collections:
                print("Invalid collection ID")
                continue

            collection = collections[choice]
            articles = list(collection.find().sort("_id", -1).limit(5))
            
            if not articles:
                print("No articles found in this collection!")
                continue
            
            for i, article in enumerate(articles, 1):
                print(f"{i}. {article.get('title', 'No title')} by {article.get('author', 'Unknown')}")

            article_choice = int(input("Enter the ID of the article: "))
            
            if article_choice < 1 or article_choice > len(articles):
                print("Invalid Article ID")
                continue

            selected_article = articles[article_choice - 1]

   
            print("Scraping article content...")
            
            try:
                
                news = Article(selected_article['url'])
                
                news.download()
                
                news.parse()
                
                scraped_title = news.title
                scraped_text = news.text
                scraped_authors = news.authors
                scraped_publish_date = news.publish_date
                scraped_summary = news.summary if hasattr(news, 'summary') else None
                
                print(f"Successfully scraped {len(scraped_text)} characters")
                print("Generating summary of your article...")
               
                prompt = f"""Summarize the following news article using both the API data and the scraped content:

                API Data:
                Title: {selected_article.get('title', 'No title')}
                Author: {selected_article.get('author', 'Unknown')}
                Description: {selected_article.get('description', 'No description')}
                URL: {selected_article.get('url', 'No URL')}
                
                Scraped Content:
                Scraped Title: {scraped_title}
                Scraped Authors: {', '.join(scraped_authors) if scraped_authors else 'Unknown'}
                Scraped Publish Date: {scraped_publish_date}
                Full Article Text: {scraped_text[:2000]}...  
                
                Provide a comprehensive summary that combines information from both sources while maintaining accuracy and avoiding duplication."""
                
                response = client.models.generate_content(
                    model="gemini-2.5-flash",
                    contents=prompt,
                )
                
                print("\n--- SUMMARY ---")
                print(response.text)
                print(f"\n\nRead the original article at: {selected_article['url']}")
                print("\n---------------")

                # Store both scraped data and summary in MongoDB
                scraped_data = {
                    "api_title": selected_article.get('title', 'No title'),
                    "scraped_title": scraped_title,
                    "scraped_text": scraped_text,
                    "scraped_authors": scraped_authors,
                    "ai_generated_summary": response.text,
                    "url": selected_article['url'],
                }
                
                summarizer_collection.insert_one(scraped_data)
                print("Summary and scraped data saved successfully!")
                
            except Exception as scraping_error:
                print(f"Error scraping article: {scraping_error}")
                

        except (ValueError, IndexError):
            print("Invalid input!")
        except Exception as e:
            print(f"Error: {e}")


