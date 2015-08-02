INSERT INTO hour_summary (
    location,
    sensor,
    arrival,
    mac,
    manuf,
    subtype,
    signal,
    pings
) ( 
     SELECT
        location,
        sensor,
        (floor(arrival /  300.0) * 300)::integer AS arrival,
        mac,
        manuf,
        subtype,
        avg(signal)::integer,
        count(data_id)
    FROM stream
    WHERE
        signal IS NOT NULL AND
        arrival >= (floor(
            extract(epoch from now()) / (3600.0)) * 3600 - 3600
        )::integer AND
        arrival < (floor(
            extract(epoch from now()) / (3600.0)) * 3600
        )::integer
    GROUP BY
        location,
        sensor,
        (floor(arrival /  300.0) * 300)::integer,
        mac,
        manuf,
        subtype
    ORDER BY arrival, mac
);


