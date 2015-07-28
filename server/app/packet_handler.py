import time
from uuid import uuid4

from app import app, debug, error


class ProbeHandler(object):
    
    def __init__(self, data, location="", sensor=""):
        self.location = location
        self.sensor = sensor
        self.data = data
   
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

    
    def insert(self, params):
        # write to database
        #print params
        pass
    
    def process(self):
        pass

class ProbeRequestHandler(ProbeHandler):
    
    def process(self):
        params = self.construct(self.data.source)
        self.insert(params)


class ProbeResponseHandler(ProbeHandler):
    
    def process(self):
        params = self.construct(self.data.destination)
        self.insert(params)


