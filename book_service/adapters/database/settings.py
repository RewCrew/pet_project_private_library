import os

from pydantic import BaseSettings

user = os.getenv('USER', 'postgres')
password = os.getenv('PASSWORD', 'password')
host = os.getenv('HOST', 'localhost')
port = os.getenv('PORT', '5432')
database = os.getenv('DATABASE', 'pet_project')


class Settings(BaseSettings):
    DB_URL: str = f"postgresql+psycopg2://{user}:{password}@{host}:{port}/{database}"
