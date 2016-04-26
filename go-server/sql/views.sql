BEGIN;


DROP SCHEMA IF EXISTS views CASCADE;
CREATE SCHEMA views;

SET search_path = views, data;

CREATE VIEW mac_index AS
SELECT
    p.src AS mac,
    coalesce(max(a.manuf), max(d.manuf)) AS manuf,
    CASE WHEN max(a.mac) IS NOT NULL
        THEN true
        ELSE false
    END AS ap,
    CASE WHEN max(d.mac) IS NOT NULL
        THEN true
        ELSE false 
    END AS device,
    count(*)
FROM packets AS p
LEFT OUTER JOIN devices AS d ON p.src = d.mac
LEFT OUTER JOIN access_points AS a ON p.src = a.mac
GROUP BY p.src
ORDER BY ap, device, src;


COMMIT;
