import time
from uuid import uuid4

from cassandra.cluster import Cluster
from cassandra.cqlengine import connection
from cassandra.cqlengine.query import DoesNotExist

from app import app, debug, error
from cqlmodels import Stream, Manuf, Beacon, Recent, Visit, LocationIndex


class FrameHandler(object):
    
    def __init__(self, data, location="", sensor=""):
        self.location = location
        self.sensor = sensor
        self.data = data
    
    def construct(self):
        params = {
            "location":self.location,
            "stamp":self.data.stamp,
            "sensor":self.sensor,
            "source":self.data.source,
            "dest":self.data.destination,
            "arrival":self.data.arrival,
            "subtype":self.data.subtype,
        }
        if self.data.HasField("signal"): params["signal"] = self.data.signal
        return params
    
    def insert(self, params):
        stream = Stream(**params)
        stream.save()

    def process(self):
        self.insert(self.construct())
        #raise NotImplemented


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

    def update_visit(self, mac):
        recent = self.data.arrival - 60 * 15.0
        record = Visit.objects\
            .filter(mac=mac)\
            .first()
        # if a previous record exists, it may or may not be recent
        if record and record.recent_arrival > recent:
            # delete record in location index (location, record.recent_stamp)
            LocationIndex.objects(
                location=self.location,
                recent_stamp=record.recent_stamp
            ).delete()

            # update visit with new recent_stamp
            Visit.objects(mac=mac, stamp=record.stamp).update(
                recent_arrival=self.data.arrival,
                recent_stamp=self.data.stamp
            )
            
            # insert new record into location index with
            # recent_stamp == self.data.stamp
            location = LocationIndex(
                location=self.location,
                recent_stamp=self.data.stamp,
                mac=mac,
                first_stamp=record.stamp
            )
            location.save()

        # record exists but it is old
        # create new visit and new location_index
        else:
            manuf = Manuf.objects.filter(prefix=mac[0:8].upper()).first()
            if manuf: manuf = manuf.manuf
            else: manuf = None
            location = LocationIndex(
                location=self.location,
                recent_stamp=self.data.stamp,
                first_stamp=self.data.stamp,
                mac=mac
            )
            device = Visit(
                mac=mac,
                manuf=manuf,
                stamp=self.data.stamp,
                recent_stamp=self.data.stamp,
                location=self.location,
                first_arrival=self.data.arrival,
                recent_arrival=self.data.arrival
            )
            location.save()
            device.save()

    def insert(self, params):
        recent = Recent(**params)
        recent.save()
        self.update_visit(params["mac"])


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
            Beacon.get(mac=self.data.source)
        except DoesNotExist:
            beacon = Beacon(mac=self.data.source, ssid=self.data.ssid)
            beacon.save()


