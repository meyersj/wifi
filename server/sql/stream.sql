
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

