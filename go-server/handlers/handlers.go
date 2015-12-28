package handlers

import (
	"../../wifiproto"
	"encoding/json"
	"fmt"
	"github.com/golang/protobuf/proto"
	"io/ioutil"
	"log"
	"net/http"
)

type SuccessResponse struct {
	Success bool
	Msg     string
}

func build_success_response(r *SuccessResponse) string {
	res, _ := json.Marshal(r)
	return string(res[:])
}

func Index(w http.ResponseWriter, r *http.Request) {
	w.Header().Set("Access-Control-Allow-Origin", "*")
	w.Header().Set("Content-type", "text/plain")
	log.Println(r.Method, r.URL)
	fmt.Fprintf(w, "INDEX")
}

func Packet(w http.ResponseWriter, r *http.Request) {
	w.Header().Set("Access-Control-Allow-Origin", "*")
	w.Header().Set("Content-type", "text/plain")
	res := &SuccessResponse{Success: false, Msg: "invalid request"}
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
		res.Success = true
		res.Msg = ""
	}
	res_body := build_success_response(res)
	log.Println(res_body)
	fmt.Fprintf(w, res_body)
}
