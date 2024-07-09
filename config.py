import os
from urllib.parse import quote_plus
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY')
    MONGO_USERNAME = quote_plus(os.getenv('MONGO_USERNAME'))
    MONGO_PASSWORD = quote_plus(os.getenv('MONGO_PASSWORD'))
    MONGO_CLUSTER_URL = os.getenv('MONGO_CLUSTER_URL')
    MONGO_DBNAME = os.getenv('MONGO_DBNAME')

    MONGO_URI = f'mongodb+srv://{MONGO_USERNAME}:{MONGO_PASSWORD}@{MONGO_CLUSTER_URL}/{MONGO_DBNAME}?retryWrites=true&w=majority'

