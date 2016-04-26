package main

import (
	"./wifiproto"
	"database/sql"
	_ "github.com/lib/pq"
	"log"
	"strings"
)

type DBClient struct {
	DB *sql.DB
}

func InitDBClient(uri string) *DBClient {
	db, err := sql.Open("postgres", uri)
	if err != nil {
		log.Fatal(db)
	}
	err = db.Ping()
	if err != nil {
		log.Fatal("failed to ping postgres:", err)
	}
	db.SetMaxIdleConns(25)
	db.SetMaxOpenConns(25)
	return &DBClient{DB: db}
}

func (c *DBClient) UpsertPacketTag(subtype string, mac string) {
	// determine if packet is from device, access point or unknown
	table := ""
	manuf := ""
	switch subtype {
	case "0x00", "0x02", "0x04":
		// packet originated from device
		table = "devices"
	case "0x01", "0x03", "0x05":
		// packet originated from access point
		table = "access_points"
	case "0x20", "0x28":
		// exit if packet was data frame
		return
	}

	// lookup if record already exists in devices or access_points table
	// and exit if so
	query := "SELECT manuf FROM data." + table + " WHERE mac = $1"
	err := c.DB.QueryRow(query, mac).Scan(&manuf)
	if err == nil {
		return
	}

	// lookup manufacture from OUI database using mac prefix
	query = "SELECT manuf FROM data.manuf WHERE prefix = $1"
	c.DB.QueryRow(query, strings.ToUpper(mac[0:8])).Scan(&manuf)

	// insert data into devices or access points table with manufacture
	stmt := "INSERT INTO data." + table + " (mac, manuf) VALUES ($1, $2)"
	_, err = c.DB.Exec(stmt, mac, manuf)
	if err != nil {
		log.Fatal("failed to insert packet:", err)
	}
}

func (c *DBClient) InsertPacket(p *wifiproto.Packet) {
	// tag packet as originating from device or access point
	c.UpsertPacketTag(*p.Subtype, *p.Source)
	// insert packet
	stmt := "" +
		"INSERT INTO data.packets " +
		"(arrival, subtype, src, dest, freq, signal) " +
		"VALUES " +
		"($1, $2, $3, $4, $5, $6)"
	_, err := c.DB.Exec(
		stmt, p.Arrival, p.Subtype, p.Source, p.Destination, p.Freq, p.Signal,
	)
	if err != nil {
		log.Fatal("failed to insert packet:", err)
	}
}

func (c *DBClient) QueryRecent(tstamp int64) []*wifiproto.Packet {
	var r *wifiproto.Packet
	records := []*wifiproto.Packet{}

	query := "" +
		"SELECT arrival, subtype, src, signal " +
		"FROM data.packets " +
		"WHERE signal IS NOT NULL AND arrival > $1 " +
		"ORDER BY src, arrival DESC"

	rows, err := c.DB.Query(query, tstamp)
	if err != nil {
		log.Println("failed to query database\n", query)
		log.Fatal(err)
	}

	defer rows.Close()
	for rows.Next() {
		r = &wifiproto.Packet{}
		err := rows.Scan(&r.Arrival, &r.Subtype, &r.Source, &r.Signal)
		if err != nil {
			log.Fatal(err)
		}
		records = append(records, r)
	}
	return records
}

func (c *DBClient) HourlySummary(mac string, tstamp int64) []*Bucket5DAO {
	var b *Bucket5DAO
	records := []*Bucket5DAO{}

	query := "SELECT bucket, mac, avg_signal, ping_count " +
		"FROM data.bucket5 " +
		"WHERE " +
		"	mac = $1 AND " +
		"	bucket >= $2 " +
		"ORDER BY bucket"

	rows, err := c.DB.Query(query, mac, tstamp)
	if err != nil {
		log.Println("failed to query database\n", query)
		log.Fatal(err)
	}

	defer rows.Close()
	for rows.Next() {
		b = &Bucket5DAO{}
		err := rows.Scan(&b.Bucket, &b.Mac, &b.AvgSignal, &b.PingCount)
		if err != nil {
			log.Fatal(err)
		}
		records = append(records, b)
	}
	return records
}

func (c *DBClient) DailySummary(mac string, tstamp int64) []*HourlyDAO {
	var b *HourlyDAO
	records := []*HourlyDAO{}

	query := "SELECT hour, mac, avg_signal, bucket5_count " +
		"FROM data.hourly " +
		"WHERE " +
		"	mac = $1 AND " +
		"	hour >= $2 " +
		"ORDER BY hour"

	rows, err := c.DB.Query(query, mac, tstamp)
	if err != nil {
		log.Println("failed to query database\n", query)
		log.Fatal(err)
	}

	defer rows.Close()
	for rows.Next() {
		b = &HourlyDAO{}
		err := rows.Scan(&b.Hour, &b.Mac, &b.AvgSignal, &b.Bucket5Count)
		if err != nil {
			log.Fatal(err)
		}
		records = append(records, b)
	}
	return records
}
