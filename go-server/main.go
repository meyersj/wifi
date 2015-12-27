package main

import (
    "fmt"
    "net/http"
    "strconv"
)

func packet_handler(w http.ResponseWriter, r *http.Request) {
    // set response headers
    w.Header().Set("Access-Control-Allow-Origin", "*")
    w.Header().Set("Content-type", "application/json")
    
    // send response
    fmt.Fprintf(w, "Hello")
}

func start_server(port int) {
    port_str := ":" + strconv.Itoa(port)
    fmt.Println("Starting server at 127.0.0.1" + port_str)
    http.HandleFunc("/packet", packet_handler)
    http.ListenAndServe(port_str, nil)
}

func main() {
    start_server(5000)
}
