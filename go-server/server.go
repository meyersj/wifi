package main

import (
	"log"
	"net/http"
	"strconv"
)

func StartServer(in_port int) {
	db := InitDBClient("postgres://jeff:password@localhost/wifi")
	attachHandlers(db)
	port := ":" + strconv.Itoa(in_port)
	log.Println("Starting server at 127.0.0.1" + port)
	log.Fatal(http.ListenAndServe(port, nil))
}

func attachHandlers(db *DBClient) {
	http.Handle("/", &IndexHandler{})
	http.Handle("/packet", &PacketHandler{Db: db})
	http.Handle("/query", &QueryHandler{Db: db})
}
