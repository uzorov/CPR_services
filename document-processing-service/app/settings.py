from pydantic_settings import BaseSettings, SettingsConfigDict
from pathlib import Path
import os
from dotenv import load_dotenv

env_path = Path(__file__).resolve().parents[1] / ".env"
load_dotenv(dotenv_path=env_path)


print(f"Current working directory: {os.getcwd()}")
print(f"Is .env file present: {os.path.isfile(env_path)}")
print(f"env_path: {env_path}")


class Settings(BaseSettings):
    postgres_url: str = os.getenv("POSTGRES_URL")


settings = Settings()
