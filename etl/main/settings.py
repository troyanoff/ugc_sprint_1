import os
from typing import TypeVar

from pydantic import BaseModel, Field
from pydantic_settings import BaseSettings, SettingsConfigDict

T = TypeVar("T", bound=BaseModel)

env_file_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), ".env")


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=env_file_path, env_file_encoding="utf-8")

    project_name: str = Field("etl_for_bi", alias="PROJECT_NAME")
    is_test_run: bool = Field(False, alias="IS_TEST_RUN")
    kafka_brokers: str = Field("localhost:9094", alias="KAFKA_BROKERS")
    kafka_batch_size: int = Field(2, alias="KAFKA_BATCH_SIZE")
    ch_host: str = Field("localhost", alias="CLICKHOUSE_HOST")
    ch_port: int = Field(9000, alias="CLICKHOUSE_PORT")
    ch_batch_size: int = Field(50, alias="CH_BATCH_SIZE")
    etl_sleep_time_seconds: int = Field(0, alias="ETL_SLEEP_TIME_IN_SECONDS")


settings = Settings()
