## WiFi Device Activity

[Live Demo](http://meyersj.github.io/wifi)

### Summary

This project contains code used to monitor Wifi activity with a Raspberry Pi.
It also contains code to create some endpoints for
a web server to receive WiFi packet headers from the Pi, and for querying the
data for visualizations. The web server endpoints are written in Go.
The request payload is encoded/decoded using protocol buffers by the client and server.
The server will insert the received packet headers into a PostgreSQL database.

You should be able to run the sensor code on any computer with a compatible network card
that can be switched into monitor mode.

+ **Supported OS:** Ubuntu Linux and Raspbian
+ **Example Configuration:** Raspberry Pi running `sensor` application with DigitalOcean droplet
with PostgreSQL instance and running `go-server` application that handles request sent from Raspberry Pi. 

### Project Structure

#### wifiproto
Contains protocol buffer definitions used for serialization of data
sent between the Pi and web server.
 - **build.sh** Execute this to rebuild **wifi_pb2.py** and **wifi.pb.go** if you make changes to **wifi.proto**

#### go-server
Contains the `sql` scripts to build a PostgreSQL database and `go-server` application to handle API requests
from Raspberry Pi and from web-clients.
There is a [README](https://github.com/meyersj/wifi/blob/master/go-server/README.md)
for getting it setup and running.

#### sensor
This folder contains all the client code that is running on the sensor.
There is a [README](https://github.com/meyersj/wifi/blob/master/sensor/README.md)
in this folder that covers setting up and running the sensor code.

#### analyzer
Simple python and psql script to bin data into `5 min`, `hour`, `day` and `week` buckets. This aggregated
data is used for answering queries

Once `go-server` and `sensor` applications or both running and communicating succesfully with the database
you can follow directions in `analyzer/CRON_EXAMPLE` for example entries that should be added to a crontab to
run the aggregate scripts. You will need to correct to path to the scripts.

#### gh-pages branch
Contains D3 Live Demo visualization, hosted at http://meyersj.github.io/wifi

