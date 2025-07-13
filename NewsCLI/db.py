from pymongo import MongoClient
import os
from dotenv import load_dotenv

load_dotenv()

MONGO_URI= os.getenv("MONGO_URI")
if not MONGO_URI:
    print("ERROR: MONGO_URI not found in .env file")
    print("Please check your .env file contains: MONGO_URI=mongodb+srv://...")
    exit(1)

conn = MongoClient(MONGO_URI)