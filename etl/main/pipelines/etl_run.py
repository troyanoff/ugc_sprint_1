from time import sleep
from typing import Type

from main.repositories.ch_writer import ClickHouseWriter
from main.repositories.kafka_reader import KafkaReader
from main.settings import T, settings


class ETLPipeline:
    def __init__(
        self,
        kafka_brokers: str,
        kafka_group_id: str,
        kafka_topic: str,
        clickhouse_host: str,
        clickhouse_port: int,
        model: Type[T],
        batch_size_to_read: int,
        batch_size_to_write: int,
    ) -> None:
        self.kafka_reader = KafkaReader(
            brokers=kafka_brokers,
            group_id=kafka_group_id,
            topic=kafka_topic,
            model=model,
            batch_size=batch_size_to_read,
        )
        self.clickhouse_writer = ClickHouseWriter(
            host=clickhouse_host, port=clickhouse_port, batch_size=batch_size_to_write
        )
        self.table_name = model.get_table_name()

    def run(self) -> None:
        while True:
            messages = self.kafka_reader.read_messages()
            if messages:
                messages_dicts = [message.model_dump() for message in messages]
                self.clickhouse_writer.insert_data(self.table_name, messages_dicts)
                self.kafka_reader.consumer.commit()
            sleep(settings.etl_sleep_time_seconds)
