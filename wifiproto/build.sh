#!/bin/bash
protoc -I=$PWD --python_out=$PWD $PWD/wifi.proto
protoc -I=$PWD --go_out=$PWD $PWD/wifi.proto

cp $PWD/wifi.pb.go ../go-server/wifiproto/wifi.pb.go
