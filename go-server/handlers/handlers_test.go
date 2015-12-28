package handlers

import (
	"../../wifiproto"
	test "../utils"
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
	server := httptest.NewServer(http.HandlerFunc(Index))

	defer server.Close()

	resp, err := http.Get(server.URL)
	if err != nil {
		t.Fatal(err)
	}
	test.Equals(t, resp.StatusCode, 200)

	expected := "INDEX"
	actual, err := ioutil.ReadAll(resp.Body)
	if err != nil {
		t.Fatal(err)
	}
	test.Equals(t, expected, string(actual))
}

func TestPostPacketHandler(t *testing.T) {
	// construct test data
	payload := BuildPostPayload()

	// post to test server
	server := httptest.NewServer(http.HandlerFunc(Packet))
	defer server.Close()
	resp, err := http.Post(server.URL, "application/octet-stream", payload)
	if err != nil {
		t.Fatal(err)
	}

	// check that request was succesful
	test.Equals(t, resp.StatusCode, 200)
	body, err := ioutil.ReadAll(resp.Body)
	if err != nil {
		t.Fatal(err)
	}
	success := &SuccessResponse{}
	err = json.Unmarshal(body, success)
	if err != nil {
		t.Fatal(err)
	}
	test.Assert(t, success.Success, "error: "+success.Msg)
}
