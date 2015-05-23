CREATE KEYSPACE networks WITH REPLICATION = {
    'class': 'SimpleStrategy',
    'replication_factor': 1
};

USE networks;

CREATE TABLE location_recent_data (
    location TEXT,
    stamp TIMEUUID,
    sensor TEXT,
    mac TEXT,
    arrival DECIMAL,
    subtype TEXT,
    seq INT,
    signal INT,
    PRIMARY KEY (location, stamp)
) WITH CLUSTERING ORDER BY (stamp DESC);

CREATE TABLE location_recent_data (



) WITH CLUSTERING ORDER BY (stamp DESC);



CREATE TABLE mac_recent_data (
    location TEXT,
    stamp TIMEUUID,
    sensor TEXT,
    mac TEXT,
    arrival DECIMAL,
    subtype TEXT,
    seq INT,
    signal INT,
    PRIMARY KEY (mac, stamp)
) WITH CLUSTERING ORDER BY (stamp DESC);




CREATE TABLE beacon (
    mac TEXT,
    ssid TEXT,
    PRIMARY KEY (mac)
);

CREATE TABLE device_index (
    mac TEXT PRIMARY KEY,
    recent_location TEXT,
    recent_sensor TEXT,
    recent_arrival DECIMAL
);
    
CREATE TABLE visit_index (
    mac TEXT,
    stamp TIMEUUID,
    location TEXT,
    first_arrival DECIMAL,
    recent_arrival DECIMAL,
    pings LIST <DECIMAL>,
    signals LIST <INT>,
    counts <INT>,
    PRIMARY KEY (mac, stamp)
) WITH CLUSTERING ORDER BY (stamp DESC);



