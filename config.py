import os 
from dotenv import load_dotenv

load_dotenv()

class Config:
    ENV = os.getenv("ENV", "LOCAL")
    SECRET_KEY = os.getenv("SECRET_KEY")
    if ENV == "production":
        MONGO_URI = os.getenv("MONGODB_URI_PROD")
        MONGO_DB_NAME = os.getenv("MONGO_DB_NAME_PROD")
    else:
        MONGO_URI = os.getenv("MONGODB_URI_LOCAL")
        MONGO_DB_NAME = os.getenv("MONGO_DB_NAME_LOCAL")
