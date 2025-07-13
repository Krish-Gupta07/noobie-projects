from google import genai
import os
from dotenv import load_dotenv
from gmail import get_emails


load_dotenv()

imap_summary = ""

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    print("ERROR: GEMINI_API_KEY not found in .env file")
    exit(1)


def mail_summarizer ():
 
 print("Retrieving mails...")
 email_data = get_emails()
 client = genai.Client(api_key=GEMINI_API_KEY)

 print("Summarizing your inbox...")
 response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents=f"Summarize these mails {email_data} and exclude promotional and spam mail and make sure to format it properly. Keep the responses as short and clean as possible, the response should only have useful information and nothing related to affirmation of prompt shall be there",
 )


 return response.text 






