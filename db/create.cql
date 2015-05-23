CREATE KEYSPACE networks WITH REPLICATION = {
    'class': 'SimpleStrategy',
    'replication_factor': 1
};

USE networks;

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
    mac TEXT,
    stamp TIMEUUID,
    first_arrival DECIMAL,
    recent_arrival DECIMAL,
    PRIMARY KEY (location, stamp)
) WITH CLUSTERING ORDER BY (stamp DESC);

CREATE TABLE visit (
    mac TEXT,
    stamp TIMEUUID,
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

CREATE TABLE process_status (
    location TEXT PRIMARY KEY,
    last_process TIMEUUID
);


