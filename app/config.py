import os
from pathlib import Path
from datetime import timedelta
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent


def sqlite_uri(database_path):
    return f"sqlite:///{Path(database_path).resolve().as_posix()}"


class Config:
    DATABASE = str(
        BASE_DIR / "instance" / os.getenv("DATABASE", "expenses.db")
    )

    SQLALCHEMY_DATABASE_URI = sqlite_uri(DATABASE)

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    SECRET_KEY = os.getenv("SECRET_KEY")

    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")

    JWT_ACCESS_TOKEN_EXPIRES = timedelta(minutes=15)


class TestingConfig(Config):
    TESTING = True
    DATABASE = str(BASE_DIR / "instance" / "tests.db")
    SQLALCHEMY_DATABASE_URI = sqlite_uri(DATABASE)


class DevelopmentConfig(Config):
    DEBUG = True


class ProductionConfig(Config):
    DEBUG = False