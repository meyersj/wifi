DROP SCHEMA IF EXISTS data CASCADE;
CREATE SCHEMA data;

SET search_path = data;

CREATE TABLE packets (
    id serial PRIMARY KEY,
    arrival numeric,
    subtype varchar,
    ssid varchar,
    src varchar,
    src_manuf varchar,
    dest varchar,
    dest_manuf varchar,
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
