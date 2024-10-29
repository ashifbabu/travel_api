from dotenv import load_dotenv
import os

load_dotenv()

print("API_KEY:", os.getenv('API_KEY'))
print("CLIENT_SECRET:", os.getenv('CLIENT_SECRET'))