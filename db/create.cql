DROP KEYSPACE IF EXISTS networks;
CREATE KEYSPACE networks WITH REPLICATION = {
    'class': 'SimpleStrategy',
    'replication_factor': 1
};

USE networks;

CREATE TABLE stream (
    location TEXT,
    stamp TIMEUUID,
    sensor TEXT,
    source TEXT,
    dest TEXT,
    arrival DECIMAL,
    subtype TEXT,
    signal INT,
    PRIMARY KEY (location, stamp)
) WITH CLUSTERING ORDER BY (stamp DESC) AND
default_time_to_live = 86400;

CREATE TABLE processed (
    location TEXT PRIMARY KEY,
    last_process TIMEUUID
);

CREATE TABLE recent (
    location TEXT,
    stamp TIMEUUID,
    sensor TEXT,
    mac TEXT,
    arrival DECIMAL,
    subtype TEXT,
    seq INT,
    signal INT,
    PRIMARY KEY (location, stamp)
) WITH CLUSTERING ORDER BY (stamp DESC) AND
default_time_to_live = 86400;

CREATE TABLE location_index (
    location TEXT,
    recent_stamp TIMEUUID,
    first_stamp TIMEUUID,
    mac TEXT,
    PRIMARY KEY (location, recent_stamp)
) WITH CLUSTERING ORDER BY (recent_stamp DESC);

CREATE TABLE visit (
    mac TEXT,
    manuf TEXT,
    stamp TIMEUUID,
    recent_stamp TIMEUUID,
    location TEXT,
    first_arrival DECIMAL,
    recent_arrival DECIMAL,
    pings LIST <DECIMAL>,
    signals LIST <INT>,
    counts LIST <INT>,
    PRIMARY KEY (mac, stamp)
) WITH CLUSTERING ORDER BY (stamp DESC);

CREATE TABLE beacon (
    mac TEXT,
    ssid TEXT,
    PRIMARY KEY (mac)
);

CREATE TABLE manuf (
    prefix TEXT PRIMARY KEY,
    manuf TEXT
);

CREATE TABLE process_status (
    location TEXT PRIMARY KEY,
    last_process TIMEUUID
);

COPY manuf (prefix, manuf) FROM '/root/manuf.csv';

