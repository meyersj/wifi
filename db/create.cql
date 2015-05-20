CREATE KEYSPACE networks WITH REPLICATION = {
    'class': 'SimpleStrategy',
    'replication_factor': 1
};

USE networks;

CREATE TABLE location_recent_data (
    location TEXT,
    sensor TEXT,
    mac TEXT,
    arrival DECIMAL,
    subtype TEXT,
    seq INT,
    signal INT,
    PRIMARY KEY (location, arrival)
) WITH CLUSTERING ORDER BY (arrival DESC);

CREATE TABLE mac_recent_data (
    location TEXT,
    sensor TEXT,
    mac TEXT,
    arrival DECIMAL,
    subtype TEXT,
    seq INT,
    signal INT,
    PRIMARY KEY (mac, arrival)
) WITH CLUSTERING ORDER BY (arrival DESC);

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
    location TEXT,
    first_arrival DECIMAL,
    recent_arrival DECIMAL,
    PRIMARY KEY (mac, first_arrival)
) WITH CLUSTERING ORDER BY (first_arrival DESC);



