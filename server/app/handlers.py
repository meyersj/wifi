import time
from uuid import uuid4

from cassandra.cluster import Cluster
from cassandra.cqlengine import connection
from cassandra.cqlengine.query import DoesNotExist

from app import app, debug, error
from cqlmodels import Beacon as BeaconTable
from cqlmodels import MacRecent, LocationRecent
from cqlmodels import DeviceIndex, VisitIndex


class FrameHandler(object):
    
    def __init__(self, data, location="", sensor=""):
        self.location = location
        self.sensor = sensor
        self.data = data

    def process(self): raise NotImplemented


class ProbeHandler(FrameHandler):
    
    def construct(self, mac):
        params = {
            "location":self.location,
            "stamp":self.data.stamp,
            "sensor":self.sensor,
            "mac":mac,
            "arrival":self.data.arrival,
            "subtype":self.data.subtype,
            "source":self.data.source
        }
        if self.data.HasField("seq"): params["seq"] = self.data.seq
        if self.data.HasField("signal"): params["signal"] = self.data.signal
        return params

    def visit_index(self, mac):
        recent = self.data.arrival - 60 * 15.0
        record = VisitIndex.objects\
            .filter(mac=mac)\
            .first()
        if record and record.recent_arrival > recent:
            VisitIndex.objects(mac=mac, stamp=self.data.stamp)\
                .update(recent_arrival=self.data.arrival)
        else:
            device = VisitIndex(
                mac=mac,
                stamp=self.data.stamp,
                location=self.location,
                first_arrival=self.data.arrival,
                recent_arrival=self.data.arrival
            )
            device.save()

    def device_index(self, mac):
        DeviceIndex.objects(mac=mac).update(
            recent_location=self.location,
            recent_sensor=self.sensor,
            recent_arrival=self.data.arrival)

    def insert(self, params):
        recent = MacRecent(**params)
        location = LocationRecent(**params)
        recent.save()
        location.save()
        self.device_index(params["mac"])
        self.visit_index(params["mac"])


class ProbeRequestHandler(ProbeHandler):
    
    def process(self):
        params = self.construct(self.data.source)
        self.insert(params)


class ProbeResponseHandler(ProbeHandler):
    
    def process(self):
        params = self.construct(self.data.destination)
        self.insert(params)


class BeaconHandler(FrameHandler):

    def process(self):
        try:
            BeaconTable.get(mac=self.data.source)
        except DoesNotExist:
            beacon = BeaconTable(mac=self.data.source, ssid=self.data.ssid)
            beacon.save()


