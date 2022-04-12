from pydantic import BaseSettings
import os

user = os.getenv('USER', 'superuser')
password = os.getenv('PASSWORD', 'password')
host = os.getenv('HOST', 'localhost')
port = os.getenv('PORT', '5432')
database = os.getenv('DATABASE', 'users')


class Settings(BaseSettings):
    DB_URL: str = f"postgresql+psycopg2://{user}:{password}@{host}:{port}/{database}"
