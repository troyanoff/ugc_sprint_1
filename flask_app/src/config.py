import os

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

env_file_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), ".env")


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=env_file_path, env_file_encoding="utf-8", extra="ignore"
    )

    SECRET_KEY: str = Field(None, alias="SECRET_KEY")
    JWT_SECRET_KEY: str = Field(None, alias="JWT_SECRET_KEY")
    ALGORITHM: str = Field(None, alias="ALGORITHM")
    KAFKA_BOOTSTRAP_SERVERS: str = Field(
        "localhost:9092", alias="KAFKA_BOOTSTRAP_SERVERS"
    )
    KAFKA_TOPIC: str = Field("user_actions", alias="KAFKA_TOPIC")


settings = Settings()
