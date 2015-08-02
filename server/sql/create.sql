DROP TABLE IF EXISTS stream;
CREATE TABLE stream (
    data_id serial PRIMARY KEY,
    location varchar,
    sensor varchar,
    arrival numeric,
    mac varchar, 
    manuf varchar,
    subtype varchar,
    seq integer,
    signal integer
);

CREATE INDEX ON stream (arrival);

DROP TABLE IF EXISTS hour_summary;
CREATE TABLE hour_summary (
    data_id serial PRIMARY KEY,
    location varchar,
    sensor varchar,
    arrival numeric,
    mac varchar, 
    manuf varchar,
    subtype varchar,
    signal integer,
    pings integer
);

CREATE INDEX ON stream (arrival);

