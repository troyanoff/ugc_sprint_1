import threading

from main.models import (ClickEvent, QualityChangeEvent, QueryEvent,
                         VideoProgressEvent, ViewEvent)
from main.pipelines.etl_run import ETLPipeline
from main.settings import settings


def run_pipeline(etl_pipeline: ETLPipeline) -> None:
    etl_pipeline.run()


if __name__ == "__main__":
    pipelines = [
        ETLPipeline(
            kafka_brokers=settings.kafka_brokers,
            kafka_group_id="group1",
            kafka_topic="click_events",
            clickhouse_host=settings.ch_host,
            clickhouse_port=settings.ch_port,
            model=ClickEvent,
            batch_size_to_read=settings.kafka_batch_size,
            batch_size_to_write=settings.ch_batch_size,
        ),
        ETLPipeline(
            kafka_brokers=settings.kafka_brokers,
            kafka_group_id="group2",
            kafka_topic="view_events",
            clickhouse_host=settings.ch_host,
            clickhouse_port=settings.ch_port,
            model=ViewEvent,
            batch_size_to_read=settings.kafka_batch_size,
            batch_size_to_write=settings.ch_batch_size,
        ),
        ETLPipeline(
            kafka_brokers=settings.kafka_brokers,
            kafka_group_id="group3",
            kafka_topic="quality_change_events",
            clickhouse_host=settings.ch_host,
            clickhouse_port=settings.ch_port,
            model=QualityChangeEvent,
            batch_size_to_read=settings.kafka_batch_size,
            batch_size_to_write=settings.ch_batch_size,
        ),
        ETLPipeline(
            kafka_brokers=settings.kafka_brokers,
            kafka_group_id="group4",
            kafka_topic="video_progress_events",
            clickhouse_host=settings.ch_host,
            clickhouse_port=settings.ch_port,
            model=VideoProgressEvent,
            batch_size_to_read=settings.kafka_batch_size,
            batch_size_to_write=settings.ch_batch_size,
        ),
        ETLPipeline(
            kafka_brokers=settings.kafka_brokers,
            kafka_group_id="group5",
            kafka_topic="query_events",
            clickhouse_host=settings.ch_host,
            clickhouse_port=settings.ch_port,
            model=QueryEvent,
            batch_size_to_read=settings.kafka_batch_size,
            batch_size_to_write=settings.ch_batch_size,
        ),
    ]

    threads = []
    for pipeline in pipelines:
        thread = threading.Thread(target=run_pipeline, args=(pipeline,))
        thread.start()
        threads.append(thread)

    for thread in threads:
        thread.join()

# создание нескольких коннектов/клиентов параллельно
# будет наиболее тредобезопасным решением, но, конечно, более затратным по ресурсам
# (на стороне баз тоже, но и обработка на их стороне также будет быстрее)
