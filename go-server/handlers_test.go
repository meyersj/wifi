package main

import (
	"./utils"
	"./wifiproto"
	"bytes"
	"encoding/json"
	"github.com/golang/protobuf/proto"
	"io/ioutil"
	"log"
	"net/http"
	"net/http/httptest"
	"testing"
)

func BuildPostPayload() *bytes.Buffer {
	packet := &wifiproto.Packet{
		Arrival:     proto.Float64(1451328466.85),
		Subtype:     proto.String("0x04"),
		Source:      proto.String("00:00:00:00:00:00"),
		Destination: proto.String("FF:FF:FF:FF:FF:FF"),
		Freq:        proto.Int32(2437),
		Signal:      proto.Int32(-50),
	}

	data, err := proto.Marshal(packet)
	if err != nil {
		log.Fatal("marshaling error: ", err)
	}

	return bytes.NewBuffer(data)
}

func TestIndexHandler(t *testing.T) {
	handler := IndexHandler{}
	req, _ := http.NewRequest("GET", "/", nil)
	rec := httptest.NewRecorder()
	handler.ServeHTTP(rec, req)
	utils.Assert(t, rec.Code == http.StatusOK, "GET / status code failed")
}

func TestPostPacketHandler(t *testing.T) {
	db := InitDBClient("postgres://jeff:password@localhost/wifi")
	handler := PacketHandler{Db: db}
	defer handler.Db.DB.Close()

	// construct test data
	payload := BuildPostPayload()

	req, _ := http.NewRequest("POST", "/packet", payload)
	rec := httptest.NewRecorder()
	handler.ServeHTTP(rec, req)

	// check that request was succesful
	utils.Assert(t, rec.Code == http.StatusOK, "POST /packet status code failed")
	body, err := ioutil.ReadAll(rec.Body)
	if err != nil {
		t.Fatal(err)
	}
	res := &PacketResponse{}
	err = json.Unmarshal(body, res)
	if err != nil {
		t.Fatal(err)
	}
	utils.Assert(t, res.Success == true, "error: "+res.Msg)
}

func TestQueryHandler(t *testing.T) {
	db := InitDBClient("postgres://jeff:password@localhost/wifi")
	handler := QueryHandler{Db: db}
	defer handler.Db.DB.Close()

	req, _ := http.NewRequest("GET", "/query", nil)
	rec := httptest.NewRecorder()
	handler.ServeHTTP(rec, req)

	// check that request was succesful
	utils.Assert(t, rec.Code == http.StatusOK, "GET /query status code failed")
}
