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
	insert := "INSERT INTO packets " +
		"(arrival, subtype, src, dest, freq, signal) " +
		"VALUES " +
		"($1, $2, $3, $4, $5, $6)"
	_, err := c.DB.Exec(
		insert,
		p.Arrival, p.Subtype, p.Source, p.Destination, p.Freq, p.Signal,
	)
	if err != nil {
		log.Fatal("failed to insert packet:", err)
	}
}

func (c *DBClient) QueryLast(n int) {
	var (
		arrival float64
		subtype string
		src     string
		signal  int
	)
	query := "SELECT arrival, subtype, src, signal " +
		"FROM packets " +
		"WHERE signal IS NOT NULL " +
		"ORDER BY arrival DESC " +
		"LIMIT $1"
	rows, err := c.DB.Query(query, n)
	if err != nil {
		log.Fatal("failed to select packets:", err)
	}
	defer rows.Close()
	for rows.Next() {
		err := rows.Scan(&arrival, &subtype, &src, &signal)
		if err != nil {
			log.Fatal(err)
		}
		log.Println(arrival, subtype, src, signal)
	}
}
