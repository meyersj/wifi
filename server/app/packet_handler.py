import time
from uuid import uuid4

from app import app, db, debug, error

from models import Manuf, Stream

class ProbeHandler(object):
    
    def __init__(self, data, location="", sensor=""):
        self.location = location
        self.sensor = sensor
        self.data = data
   
    def construct(self, mac):
        params = {
            "location":self.location,
            "sensor":self.sensor,
            "arrival":self.data.arrival,
            "mac":mac,
            "subtype":self.data.subtype
        }
        if self.data.HasField("seq"): params["seq"] = self.data.seq
        if self.data.HasField("signal"): params["signal"] = self.data.signal
        return params

    
    def insert(self, params):
        record = Stream(**params)
        db.session.add(record)
        db.session.commit()
    
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


