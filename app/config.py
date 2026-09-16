import os 
from dotenv import load_dotenv

load_dotenv()

class Config:
    DATABASE = os.getenv("DATABASE", "expenses.db")
    SECRET_KEY = os.getenv("SECRET_KEY")


class TestingConfig(Config):
    DATABASE = ("tests.db")
    TESTING = True


class DevelopmentConfig(Config):
    DEBUG = True


class ProductionConfig(Config):
    DEBUG = False