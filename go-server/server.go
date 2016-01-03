package main

import (
	"log"
	"net/http"
)

func StartServer(c *Config) {
	db := InitDBClient(c.Postgres)
	AttachHandlers(db)
	port := ":" + c.Port
	log.Println("Starting server at 127.0.0.1" + port)
	log.Fatal(http.ListenAndServe(port, nil))
}

func AttachHandlers(db *DBClient) {
	http.Handle("/", &IndexHandler{})
	http.Handle("/packet", &PacketHandler{Db: db})
	http.Handle("/query", &QueryHandler{Db: db})
}
