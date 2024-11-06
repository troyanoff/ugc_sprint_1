#!/usr/bin/env bash

clickhouse-client --query "CREATE DATABASE IF NOT EXISTS events_replica"


clickhouse-client --query "\
    CREATE TABLE IF NOT EXISTS events_replica.click_events \
    (id UUID, user_id UUID, event_dt DateTime, clicked_element_id UUID) \
    Engine=ReplicatedMergeTree('/clickhouse/tables/events_shard2/click_events', 'replica_2') \
    PARTITION BY toYYYYMMDD(event_dt) ORDER BY event_dt"



clickhouse-client --query "\
    CREATE TABLE IF NOT EXISTS events_replica.view_events \
    (id UUID, user_id UUID, event_dt DateTime, event_type Enum('load', 'refresh', 'close')) \
    Engine=ReplicatedMergeTree('/clickhouse/tables/events_shard2/view_events', 'replica_2') \
    PARTITION BY toYYYYMMDD(event_dt) ORDER BY event_dt"



clickhouse-client --query "\
    CREATE TABLE IF NOT EXISTS events_replica.quality_change_events \
    (id UUID, user_id UUID, event_dt DateTime, movie_id UUID, current_quality Int32, chosen_quality Int32) \
    Engine=ReplicatedMergeTree('/clickhouse/tables/events_shard2/quality_change_events', 'replica_2') \
    PARTITION BY toYYYYMMDD(event_dt) ORDER BY event_dt"



clickhouse-client --query "\
    CREATE TABLE IF NOT EXISTS events_replica.video_progress_events \
    (id UUID, user_id UUID, event_dt DateTime, movie_id UUID, seconds Int32, is_stopped Boolean) \
    Engine=ReplicatedMergeTree('/clickhouse/tables/events_shard2/video_progress_events', 'replica_2') \
    PARTITION BY toYYYYMMDD(event_dt) ORDER BY event_dt"



clickhouse-client --query "\
    CREATE TABLE IF NOT EXISTS events_replica.query_events \
    (id UUID, user_id UUID, event_dt DateTime, is_genre_filtered Boolean, is_rating_filtered Boolean, is_actor_filtered Boolean) \
    Engine=ReplicatedMergeTree('/clickhouse/tables/events_shard2/query_events', 'replica_2') \
    PARTITION BY toYYYYMMDD(event_dt) ORDER BY event_dt"
