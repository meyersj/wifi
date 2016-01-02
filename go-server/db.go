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
	stmt := "INSERT INTO packets " +
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
		"FROM packets " +
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
