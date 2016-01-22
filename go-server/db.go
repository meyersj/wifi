package main

import (
	"./wifiproto"
	"database/sql"
	_ "github.com/lib/pq"
	"log"
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

func (c *DBClient) InsertPacket(p *wifiproto.Packet) {
	stmt := "INSERT INTO data.packets " +
		"(arrival, subtype, src, dest, freq, signal) " +
		"VALUES " +
		"($1, $2, $3, $4, $5, $6)"
	_, err := c.DB.Exec(
		stmt,
		p.Arrival, p.Subtype, p.Source, p.Destination, p.Freq, p.Signal,
	)
	if err != nil {
		log.Fatal("failed to insert packet:", err)
	}
}

func (c *DBClient) QueryRecent(tstamp int64) []*wifiproto.Packet {
	var r *wifiproto.Packet
	records := []*wifiproto.Packet{}

	query := "SELECT arrival, subtype, src, signal " +
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
