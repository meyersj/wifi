package main

import (
	"./wifiproto"
	"encoding/json"
	"fmt"
	"github.com/golang/protobuf/proto"
	"io/ioutil"
	"log"
	"net/http"
)

type IndexHandler struct{}

func (i *IndexHandler) ServeHTTP(w http.ResponseWriter, r *http.Request) {
	w.Header().Set("Access-Control-Allow-Origin", "*")
	w.Header().Set("Content-type", "text/plain")
	i.WriteResponse(w, "INDEX")
}

func (i *IndexHandler) WriteResponse(w http.ResponseWriter, r string) {
	fmt.Fprintf(w, r)
}

type PacketHandler struct {
	Db *DBClient
}

type PacketResponse struct {
	Success bool
	Msg     string
}

func (p *PacketHandler) ServeHTTP(w http.ResponseWriter, r *http.Request) {
	w.Header().Set("Access-Control-Allow-Origin", "*")
	w.Header().Set("Content-type", "text/plain")
	res := &PacketResponse{Success: false, Msg: "invalid request"}
	switch r.Method {
	case "POST":
		data, err := ioutil.ReadAll(r.Body)
		if err != nil {
			res.Msg = "failed to read request body"
			break
		}
		packet := &wifiproto.Packet{}
		err = proto.Unmarshal(data, packet)
		if err != nil {
			res.Msg = "failed to parse protobuf payload"
			break
		}
		p.Db.InsertPacket(packet)
		res.Success = true
		res.Msg = ""
	}
	p.WriteResponse(w, res)
}

func (p *PacketHandler) WriteResponse(w http.ResponseWriter, r *PacketResponse) {
	res, err := json.Marshal(r)
	if err == nil {
		res_str := string(res[:])
		log.Println(res_str)
		fmt.Fprintf(w, res_str)
	}
}

type QueryHandler struct {
	Db *DBClient
}

func (q *QueryHandler) ServeHTTP(w http.ResponseWriter, r *http.Request) {
	w.Header().Set("Access-Control-Allow-Origin", "*")
	w.Header().Set("Content-type", "text/plain")
	switch r.Method {
	case "GET":
		q.Db.QueryLast(100)
	}
	q.WriteResponse(w, "QUERY")
}

func (q *QueryHandler) WriteResponse(w http.ResponseWriter, r string) {
	fmt.Fprintf(w, r)
}
