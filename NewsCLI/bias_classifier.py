from google import genai
from db import conn
import os
from dotenv import load_dotenv

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    print("ERROR: GEMINI_API_KEY not found in .env file")
    exit(1)

client = genai.Client(api_key=GEMINI_API_KEY)

db = conn.news
bias_collection = db.bias_classifier

def bias_check():
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

   
            print("Checking for biasedness...")
            
            try:
                
               
                prompt = f"""Analyze the biasedness of a news article from the API Data provided:

                API Data:
                Title: {selected_article.get('title', 'No title')}
                Author: {selected_article.get('author', 'Unknown')}
                Description: {selected_article.get('description', 'No description')}
                URL: {selected_article.get('url', 'No URL')}
                Content: {selected_article.get('content', 'No Content')}
                 
                
                To do this, first, examine the URL of the article to infer the potential leanings of the source. Consider established media bias charts (like AllSides or Ad Fontes Media) to determine the source's general political alignment. Second, scrutinize the article's content for indicators of legitimacy and bias, such as:
Language: Is the language emotionally charged, extreme, or opinionated rather than factual?

Factuality: Are claims supported by evidence, data, or expert citations? Is there a lack of context or selective presentation of facts?

Balance: Does the article present multiple perspectives on an issue, or is it one-sided? Are there instances of false balance or false equivalence?

Attribution: Are sources clearly identified and credible?

Headlines vs. Content: Does the headline accurately reflect the article's content, or is it sensationalized or misleading?

Author Credentials: If an author is listed, what are their qualifications and affiliations?

Based on this analysis, provide a short output (not more than 20 words) that includes:

Biasedness Score: A numerical rating from 0 (completely unbiased) to 10 (highly biased).

Political Alignment: A categorical description (e.g., "Left-leaning," "Center-left," "Centrist," "Center-right," "Right-leaning," or "No discernible alignment")."""
                
                response = client.models.generate_content(
                    model="gemini-2.5-flash",
                    contents=prompt,
                )
                
                print("\n--- BIAS ANALYSIS ---")
                print(response.text)
                print(f"\n\nRead the original article at: {selected_article['url']}")
                print("\n---------------")

                bias_data = {
                    'title': selected_article['title'],
                    'bias_analysis': response.text
                }

                
                bias_collection.insert_one(bias_data)
                
            except Exception as analysis_error:
                print(f"Error analyzing bias: {analysis_error}")
                

        except (ValueError, IndexError):
            print("Invalid input!")
        except Exception as e:
            print(f"Error: {e}")
