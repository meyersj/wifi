## WiFi Device Activity

### Summary

This project contains code used to monitor Wifi activity with a Raspberry Pi.
It also contains code to create some endpoints for
a web server to receive the data from the Pi. Those endpoints
are written in Python using Flask. This also requires some way to deploy the app
using WSGI. The endpoints receive the data from the sensor
and insert it into a Postgres database.

You should be able to run the sensor code on any computer with a compatible network card
that can be switched into monitor mode.


### Project Structure

#### db
 - **create.cql** contains Postgres schema definitions
 - **manuf.csv** manufacture lookup table based on mac prefix which must be loaded into the **manuf** table

#### proto
Contains protocol buffer definitions used for serialization of data
sent between the Pi and web server.
 - **build.sh** Execute this to rebuild **packets_pb2.py** after making changes to **packets.proto**

#### sensor
This folder contains all the client code that is running on the sensor.
There is a README in this folder than goes over some commands that are
required to install the dependencies and setup permissions.

- **setup.sh** Run this script to set up the environment. This sets up a python
virtual environment so that must already be available on your system. It will
install the necessary python packages for you. It will also make copy
sample-config.py into config.py. This file must be modified
for your environment before running.

- **listen.py** Once all the dependencies have been met you can run this script. It will
listen for wifi track for a given amount of time as defined as a constant in the top of this file.
It will serialize all the packets using protocol buffers and then send it the the endpoint
as specifed in config.py. It is assumed that the server code is running at that location.

```shell
sudo airmon-ng start wlan0              # virtualize a network card running in monitor mode
wifi/sensor/env/bin/python listen.py    # run listening script (listens for about a minute then sends data)
```

#### server
This folder contains a Python web app built using Flask. The app consists of a single
endpoint used for the sensors to send pings to. Each ping is then classified
based on the packet subtype.

###### subtypes
 - 0x04 Probe Request - devices send probe requests to locate access points
 - 0x05 Probe Response - response from access points to devices that send Probe Requests
 - 0x08 Broadcast - broadcast sent by access point to let devices know it exists

The data recieved from the Pi is stored in table **stream**.


