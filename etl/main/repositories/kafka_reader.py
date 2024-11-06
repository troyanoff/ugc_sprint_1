import json
from typing import List, Type

from kafka import KafkaConsumer
from main.logger import logger
from main.settings import T
from pydantic import ValidationError


class KafkaReader:
    def __init__(
        self, brokers: str, group_id: str, topic: str, model: Type[T], batch_size: int
    ) -> None:
        self.consumer = KafkaConsumer(
            topic,
            bootstrap_servers=brokers,
            group_id=group_id,
            auto_offset_reset="earliest",
            value_deserializer=lambda x: json.loads(x.decode("utf-8")),
            enable_auto_commit=False,
        )
        self.batch_size = batch_size
        self.model = model

    def read_messages(self) -> List[T]:
        messages = []
        for message in self.consumer:
            try:
                logger.info("Reading message %s", message)
                validated_message = self.model(**message.value)
                messages.append(validated_message)
            except ValidationError as error:
                logger.error("Validation error: %s", error)
            if len(messages) >= self.batch_size:
                break
        return messages

    def close(self) -> None:
        self.consumer.close()
