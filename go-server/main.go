package main

import (
	"./handlers"
	"fmt"
	"log"
	"net/http"
	"strconv"
)

func attach_handlers() {
	http.HandleFunc("/", handlers.Index)
	http.HandleFunc("/packet", handlers.Packet)
}

func start_server(port int) {
	port_str := ":" + strconv.Itoa(port)
	fmt.Println("Starting server at 127.0.0.1" + port_str)
	attach_handlers()
	log.Fatal(http.ListenAndServe(port_str, nil))
}

func main() {
	start_server(5000)
}
