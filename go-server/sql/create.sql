BEGIN;

DROP SCHEMA IF EXISTS data CASCADE;
CREATE SCHEMA data;

SET search_path = data;

CREATE TABLE manuf (
    prefix varchar PRIMARY KEY,
    manuf varchar
);

CREATE TABLE devices (
    mac varchar PRIMARY KEY,
    manuf varchar
);

CREATE TABLE access_points (
    mac varchar PRIMARY KEY,
    manuf varchar
);

CREATE TABLE packets (
    id serial PRIMARY KEY,
    arrival numeric,
    subtype varchar,
    src varchar,
    dest varchar,
    freq integer,
    signal integer
);

CREATE INDEX ON packets (arrival);

CREATE TABLE bucket5 (
    bucket numeric,
    mac varchar,
    min_signal integer,
    max_signal integer,
    avg_signal integer,
    ping_count integer,
    PRIMARY KEY (bucket, mac)
);

CREATE TABLE hourly (
    hour numeric,
    mac varchar,
    avg_signal integer,
    bucket5_count integer,
    PRIMARY KEY (hour, mac)
);

CREATE TABLE daily (
    day numeric,
    mac varchar,
    avg_signal integer,
    hour_count integer,
    PRIMARY KEY (day, mac)
);

CREATE TABLE weekly (
    week numeric,
    mac varchar,
    day_count integer,
    PRIMARY KEY (week, mac)
);

COMMIT;
