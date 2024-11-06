#!/usr/bin/env bash

clickhouse-client --query "CREATE DATABASE IF NOT EXISTS events"

clickhouse-client --query "CREATE DATABASE IF NOT EXISTS events_shard"



clickhouse-client --query "\
    CREATE TABLE IF NOT EXISTS events_shard.click_events \
    (id UUID, user_id UUID, event_dt DateTime, clicked_element_id UUID) \
    Engine=ReplicatedMergeTree('/clickhouse/tables/events_shard2/click_events', 'replica_1') \
    PARTITION BY toYYYYMMDD(event_dt) ORDER BY event_dt"

clickhouse-client --query "\
    CREATE TABLE IF NOT EXISTS events.click_events \
    (id UUID, user_id UUID, event_dt DateTime, clicked_element_id UUID) \
    ENGINE = Distributed('company_cluster', '', click_events, rand())"



clickhouse-client --query "\
    CREATE TABLE IF NOT EXISTS events_shard.view_events \
    (id UUID, user_id UUID, event_dt DateTime, event_type Enum('load', 'refresh', 'close')) \
    Engine=ReplicatedMergeTree('/clickhouse/tables/events_shard2/view_events', 'replica_1') \
    PARTITION BY toYYYYMMDD(event_dt) ORDER BY event_dt"

clickhouse-client --query "\
    CREATE TABLE IF NOT EXISTS events.view_events \
    (id UUID, user_id UUID, event_dt DateTime, event_type Enum('load', 'refresh', 'close')) \
    ENGINE = Distributed('company_cluster', '', view_events, rand())"



clickhouse-client --query "\
    CREATE TABLE IF NOT EXISTS events_shard.quality_change_events \
    (id UUID, user_id UUID, event_dt DateTime, movie_id UUID, current_quality Int32, chosen_quality Int32) \
    Engine=ReplicatedMergeTree('/clickhouse/tables/events_shard2/quality_change_events', 'replica_1') \
    PARTITION BY toYYYYMMDD(event_dt) ORDER BY event_dt"

clickhouse-client --query "\
    CREATE TABLE IF NOT EXISTS events.quality_change_events \
    (id UUID, user_id UUID, event_dt DateTime, movie_id UUID, current_quality Int32, chosen_quality Int32) \
    ENGINE = Distributed('company_cluster', '', quality_change_events, rand())"



clickhouse-client --query "\
    CREATE TABLE IF NOT EXISTS events_shard.video_progress_events \
    (id UUID, user_id UUID, event_dt DateTime, movie_id UUID, seconds Int32, is_stopped Boolean) \
    Engine=ReplicatedMergeTree('/clickhouse/tables/events_shard2/video_progress_events', 'replica_1') \
    PARTITION BY toYYYYMMDD(event_dt) ORDER BY event_dt"

clickhouse-client --query "\
    CREATE TABLE IF NOT EXISTS events.video_progress_events \
    (id UUID, user_id UUID, event_dt DateTime, movie_id UUID, seconds Int32, is_stopped Boolean) \
    ENGINE = Distributed('company_cluster', '', video_progress_events, rand())"



clickhouse-client --query "\
    CREATE TABLE IF NOT EXISTS events_shard.query_events \
    (id UUID, user_id UUID, event_dt DateTime, is_genre_filtered Boolean, is_rating_filtered Boolean, is_actor_filtered Boolean) \
    Engine=ReplicatedMergeTree('/clickhouse/tables/events_shard2/query_events', 'replica_1') \
    PARTITION BY toYYYYMMDD(event_dt) ORDER BY event_dt"

clickhouse-client --query "\
    CREATE TABLE IF NOT EXISTS events.query_events \
    (id UUID, user_id UUID, event_dt DateTime, is_genre_filtered Boolean, is_rating_filtered Boolean, is_actor_filtered Boolean) \
    ENGINE = Distributed('company_cluster', '', query_events, rand())"
