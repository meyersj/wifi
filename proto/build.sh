#!/bin/bash
protoc -I=$PWD --python_out=$PWD $PWD/packets.proto
