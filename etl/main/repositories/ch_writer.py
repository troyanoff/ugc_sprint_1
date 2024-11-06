from typing import Any, Dict, List, Tuple

from clickhouse_driver import Client
from clickhouse_driver.errors import Error
from main.logger import logger
from main.settings import settings
from more_itertools import chunked
from tenacity import (retry, retry_if_exception_type, wait_incrementing,
                      wait_random)


class ClickHouseWriter:
    def __init__(self, host: str, port: int, batch_size: int) -> None:
        self.client = Client(host=host, port=port)
        self.batch_size = batch_size
        if settings.is_test_run:
            self.create_tables()

    def _create_click_table(self) -> None:
        self.client.execute(
            "CREATE TABLE IF NOT EXISTS events.click_events ("
            "id UUID, user_id UUID, event_dt DateTime, clicked_element_id UUID) "
            "Engine=MergeTree() ORDER BY event_dt"
        )

    def _create_view_table(self) -> None:
        self.client.execute(
            "CREATE TABLE IF NOT EXISTS events.view_events ("
            "id UUID, user_id UUID, event_dt DateTime, "
            "event_type Enum('load', 'refresh', 'close')) "
            "Engine=MergeTree() ORDER BY event_dt"
        )

    def _create_quality_change_table(self) -> None:
        self.client.execute(
            "CREATE TABLE IF NOT EXISTS events.quality_change_events ("
            "id UUID, user_id UUID, event_dt DateTime, movie_id UUID, "
            "current_quality Int32, chosen_quality Int32) "
            "Engine=MergeTree() ORDER BY event_dt"
        )

    def _create_video_progress_table(self):
        self.client.execute(
            "CREATE TABLE IF NOT EXISTS events.video_progress_events ("
            "id UUID, user_id UUID, event_dt DateTime, movie_id UUID, "
            "seconds Int32, is_stopped Boolean) "
            "Engine=MergeTree() ORDER BY event_dt"
        )

    def _create_query_table(self) -> None:
        self.client.execute(
            "CREATE TABLE IF NOT EXISTS events.query_events ("
            "id UUID, user_id UUID, event_dt DateTime, "
            "is_genre_filtered Boolean, is_rating_filtered Boolean, "
            "is_actor_filtered Boolean) "
            "Engine=MergeTree() ORDER BY event_dt"
        )

    def create_tables(self) -> None:
        self.client.execute("CREATE DATABASE IF NOT EXISTS events")
        self._create_click_table()
        self._create_view_table()
        self._create_quality_change_table()
        self._create_video_progress_table()
        self._create_query_table()

    def insert_data(self, table_name: str, data: List[Dict[str, Any]]) -> None:
        if not data:
            return
        logger.info(
            "Insert %s rows with batch %s to table %s",
            len(data),
            self.batch_size,
            table_name,
        )
        columns = data[0].keys()
        insert_query = f"INSERT INTO {table_name} ({', '.join(columns)}) VALUES"

        batch_data = [tuple(record.values()) for record in data]

        for index, chunk in enumerate(chunked(batch_data, self.batch_size)):
            logger.info(
                "Attempting to insert batch number %s into table %s",
                index + 1,
                table_name,
            )
            self._insert_chunk(insert_query, chunk)

    @retry(
        wait=wait_incrementing(start=1, increment=1, max=10)
        + wait_random(min=0, max=5),
        retry=retry_if_exception_type(Error),
    )
    def _insert_chunk(self, query: str, chunk: List[Tuple]) -> None:
        logger.info("Retryable chunk insert")
        self.client.execute(query, chunk)

    def close(self) -> None:
        self.client.disconnect()
