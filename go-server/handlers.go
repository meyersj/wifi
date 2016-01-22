package main

import (
	"./wifiproto"
	"encoding/json"
	"fmt"
	"github.com/golang/protobuf/proto"
	"io/ioutil"
	"log"
	"math"
	"net/http"
	"strconv"
	"time"
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
			res.Msg = "Failed to read request body"
			log.Println(res.Msg)
			break
		}
		payload := &wifiproto.Payload{}
		err = proto.Unmarshal(data, payload)
		if err != nil {
			res.Msg = "Failed to parse protobuf payload"
			log.Println(res.Msg)
			break
		}
		for i := 0; i < len(payload.Data); i++ {
			//log.Println(payload.Data[i])
			p.Db.InsertPacket(payload.Data[i])
		}
		res.Success = true
		res.Msg = ""
	}
	p.WriteResponse(w, res)
}

func (p *PacketHandler) WriteResponse(w http.ResponseWriter, r *PacketResponse) {
	res, err := json.Marshal(r)
	if err == nil {
		fmt.Fprintf(w, string(res[:]))
	}
}

type DeviceSummary struct {
	Mac          string
	FirstArrival float64
	LastArrival  float64
	AvgSignal    int32
	Count        int32
}

func InitDeviceSummary(p *wifiproto.Packet) *DeviceSummary {
	d := &DeviceSummary{}
	d.Mac = *p.Source
	d.FirstArrival = *p.Arrival
	d.LastArrival = *p.Arrival
	d.AvgSignal = *p.Signal
	d.Count = 1
	return d
}

func (d *DeviceSummary) Update(p *wifiproto.Packet) {
	d.FirstArrival = math.Min(d.FirstArrival, *p.Arrival)
	d.LastArrival = math.Max(d.LastArrival, *p.Arrival)
	avg := (d.AvgSignal*d.Count + *p.Signal) / (d.Count + 1)
	d.Count = d.Count + 1
	d.AvgSignal = int32(avg)
}

type QueryResponse struct {
	Start  int64
	Window int
	Data   []*DeviceSummary
	Error  string
}

func (r *QueryResponse) ToJSON() string {
	data, err := json.Marshal(r)
	if err != nil {
		log.Fatal(err)
	}
	return string(data)
}

type QueryHandler struct {
	Db *DBClient
}

func (q *QueryHandler) ServeHTTP(w http.ResponseWriter, r *http.Request) {
	w.Header().Set("Access-Control-Allow-Origin", "*")
	w.Header().Set("Content-type", "text/json")

	res := &QueryResponse{}

	switch r.Method {
	case "GET":
		r.ParseForm()
		window, err := strconv.Atoi(r.Form.Get("window"))
		if err != nil {
			window = 20
			res.Error = "using default window size"
		}
		res.Window = window
		res.Start = time.Now().Unix() - (int64(window) * 60)
		res.Data = q.BinRecords(q.Db.QueryRecent(res.Start))
		q.WriteResponse(w, res.ToJSON())
	default:
		q.WriteResponse(w, "{error:'INVALID REQUEST'}")
	}
}

func (q *QueryHandler) WriteResponse(w http.ResponseWriter, r string) {
	fmt.Fprintf(w, r)
}

func (q *QueryHandler) BinRecords(records []*wifiproto.Packet) []*DeviceSummary {
	var rec *DeviceSummary
	var exists bool
	devices := make(map[string]*DeviceSummary)

	for i := 0; i < len(records); i++ {
		rec, exists = devices[*records[i].Source]
		if !exists {
			rec = InitDeviceSummary(records[i])
			devices[rec.Mac] = rec
		} else {
			rec.Update(records[i])
		}
	}

	data := make([]*DeviceSummary, 0, len(devices))
	for _, value := range devices {
		data = append(data, value)
	}
	return data
}

type Bucket5DAO struct {
	Bucket    int64
	Mac       string
	AvgSignal int32
	PingCount int32
}

type HourlyDAO struct {
	Hour         int64
	Mac          string
	AvgSignal    int32
	Bucket5Count int32
}

//type DailyDAO struct {
//	Day       int64
//	Mac       string
//	AvgSignal int32
//	HourCount int32
//}

type UserSummaryResponse struct {
	HourStart  int64
	HourData   []*Bucket5DAO
	DailyStart int64
	DailyData  []*HourlyDAO
	Error      []string
}

func (r *UserSummaryResponse) ToJSON() string {
	data, err := json.Marshal(r)
	if err != nil {
		log.Fatal(err)
	}
	return string(data)
}

type UserSummaryHandler struct {
	Db *DBClient
}

func (h *UserSummaryHandler) ServeHTTP(w http.ResponseWriter, r *http.Request) {
	w.Header().Set("Access-Control-Allow-Origin", "*")
	w.Header().Set("Content-type", "text/json")

	res := &UserSummaryResponse{Error: []string{}}
	switch r.Method {
	case "GET":
		r.ParseForm()
		mac := r.Form.Get("mac")
		if mac == "" {
			res.Error = append(res.Error, "must include `mac` address parameter")
		} else {
			now := time.Now().Unix()
			// round off to last 5 minute bucket a little over an hour ago
			res.HourStart = ((now - 3600) / 360) * 360
			// round off to last hour bucket a little over a day ago
			res.DailyStart = res.HourStart + (60 * 60) - (60 * 60 * 24)
			res.HourData = h.Db.HourlySummary(mac, res.HourStart)
			res.DailyData = h.Db.DailySummary(mac, res.DailyStart)

		}
		h.WriteResponse(w, res.ToJSON())
	default:
		h.WriteResponse(w, "{error:'INVALID REQUEST'}")
	}
}

func (h *UserSummaryHandler) WriteResponse(w http.ResponseWriter, r string) {
	fmt.Fprintf(w, r)
}
