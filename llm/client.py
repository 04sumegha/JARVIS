import logging
from groq import Groq
from config import API_KEY

api_key = API_KEY
client = Groq(api_key=API_KEY)