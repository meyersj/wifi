package main

import (
	"./utils"
	"./wifiproto"
	"bytes"
	"database/sql"
	"encoding/json"
	"github.com/golang/protobuf/proto"
	"io/ioutil"
	"log"
	"net/http"
	"net/http/httptest"
	"testing"
)

var conf *Config = ReadConfig("config.toml")
var arrival float64 = 1451328466.85

func BuildTestPacket(offset float64) *wifiproto.Packet {
	return &wifiproto.Packet{
		Arrival:     proto.Float64(arrival + offset),
		Subtype:     proto.String("0x04"),
		Source:      proto.String("00:00:00:00:00:00"),
		Destination: proto.String("FF:FF:FF:FF:FF:FF"),
		Freq:        proto.Int32(2437),
		Signal:      proto.Int32(-50),
	}
}

func BuildTestPayload() *bytes.Buffer {
	packet1 := BuildTestPacket(0)
	packet2 := BuildTestPacket(15)
	packet3 := BuildTestPacket(350)

	location := "Test Location"
	sensor := "Test Sensor"

	payload := &wifiproto.Payload{
		Location: &location,
		Sensor:   &sensor,
		Data:     []*wifiproto.Packet{packet1, packet2, packet3},
	}

	data, err := proto.Marshal(payload)
	if err != nil {
		log.Fatal("marshaling error: ", err)
	}
	return bytes.NewBuffer(data)
}

func CleanupTestDB(db *sql.DB) {
	delete_packets := "DELETE FROM data.packets WHERE src = '00:00:00:00:00:00';"
	delete_bucket5 := "DELETE FROM data.bucket5 WHERE mac = '00:00:00:00:00:00';"
	delete_hourly := "DELETE FROM data.hourly WHERE mac = '00:00:00:00:00:00';"
	_, err := db.Exec(delete_packets)
	if err != nil {
		log.Fatal("failed to delete test data <data.packets>: ", err)
	}
	_, err = db.Exec(delete_bucket5)
	if err != nil {
		log.Fatal("failed to delete test data <data.bucket5>: ", err)
	}
	_, err = db.Exec(delete_hourly)
	if err != nil {
		log.Fatal("failed to delete test data <data.hourly>: ", err)
	}

}

func TestIndexHandler(t *testing.T) {
	handler := IndexHandler{}
	req, _ := http.NewRequest("GET", "/", nil)
	rec := httptest.NewRecorder()
	handler.ServeHTTP(rec, req)
	utils.Assert(t, rec.Code == http.StatusOK, "GET / status code failed")
}

func TestPostPacketHandler(t *testing.T) {
	db := InitDBClient(conf.Postgres)
	handler := PacketHandler{Db: db}
	defer db.DB.Close()
	defer CleanupTestDB(db.DB)

	// construct test data
	payload := BuildTestPayload()

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

func TestQueryHandlerArgs(t *testing.T) {
	db := InitDBClient(conf.Postgres)
	handler := QueryHandler{Db: db}
	defer handler.Db.DB.Close()
	req, _ := http.NewRequest("GET", "/query", nil)

	// set minute param to query recent records
	req.ParseForm()
	req.Form.Set("window", "5")
	rec := httptest.NewRecorder()
	handler.ServeHTTP(rec, req)

	// check that request was succesful
	utils.Assert(t, rec.Code == http.StatusOK, "GET /query status code failed")
}
