DROP TABLE IF EXISTS packets;
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
