## WiFi Traffic Listener

This project contains code used to set up a WiFi traffic listener using
a Raspberry Pi. It also contains code to create some endpoints for
a web server to recieve the data from the Pi. Those endpoints
are written in Python using Flask. This requires some way to deploy
using WSGI. The endpoints recieve the data from the sensor
and insert it into a Cassandra database.

You should be able to run the sensor code on any computer with a network card
that can be switched into monitor mode.

The current setup I am using consists of two DigitalOcean virtual machines
both with 512MB RAM. One machine runs as the web server for the sensors
to communicate with which then sends the data to a second machine running a
Cassandra instance.

### Project Structure

#### db
 - create.cql : contains Cassandra database creation script

#### proto
Contains protocol buffer definitions used for serialization of data
sent between the Pi and web server.
 - build.sh : Execute this to rebuild packets_pb2.py after making changes to packets.proto

#### sensor
This folder contains all the client code that is running on the sensor.
There is a README in this folder than goes over some commands that are
required to install the dependencies and setup permissions.

- setup.sh : Run this script to set up the environment. This sets up a python
virtual environment so that must already be available on your system. It will
install the necessary python packages for you. It will also make copy
sample-config.py into config.py. This file must be filled out correctly
for your environment before running.

- listen.py : Once all the dependencies have been met you can run this script. It will
listen for wifi track for a given amount of time as defined as a constant in the top of this file.
It will serialize all the packets using protocol buffers and then send it the the endpoint
as specifed in config.py. It is assumed that the server code is running at that location.

  ./env/bin/python listen.py

#### server
This folder contains a Python web app built using Flask. The app consists of a single
endpoint used for the sensors to send pings to. Each ping is then classified
base on the packet subtype.

###### subtypes
 - 0x04 Probe Request - devices send probe requests to locate access points
 - 0x05 Probe Response - response from access points to devices that send Probe Requests
 - 0x08 Broadcast - broadcast sent by access point to let devices know it exists

Depending on the packet type different actions are taken. There is a beacon table that
maintains a list of all access points identified in each location. The data from devices
are mostly stored in location_recent_data and mac_recent_data. Both these tables
store the same data but location_recent_data is partitioned by location of sensor,
while mac_recent_data is partitioned by mac address of device. Both of these tables
are also clustered by an arrival TimeUUID to complete the primary key.

visit_index also keeps a log of first_arrival and recent_arrival for visits of each device.
If a new packet is much older than that devices last most recent visit a new visit is
created for that device.

