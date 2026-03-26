import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("API_KEY")
PICOVOICE_ACCESS_KEY = os.getenv("PICOVOICE_ACCESS_KEY")