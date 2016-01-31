package main

import (
	"log"
	"net/http"
)

func StartServer(c *Config) {
	db := InitDBClient(c.Postgres)
	AttachHandlers(db)
	port := ":" + c.Port
	if c.Cert != "" && c.Key != "" {
		log.Println("Starting SECURE server at 127.0.0.1" + port)
		log.Fatal(http.ListenAndServeTLS(port, c.Cert, c.Key, nil))
	} else {
		log.Println("Starting server at 127.0.0.1" + port)
		log.Fatal(http.ListenAndServe(port, nil))
	}
}

func AttachHandlers(db *DBClient) {
	http.Handle("/", &IndexHandler{})
	http.Handle("/packet", &PacketHandler{Db: db})
	http.Handle("/query", &QueryHandler{Db: db})
	http.Handle("/user/summary", &UserSummaryHandler{Db: db})
}
