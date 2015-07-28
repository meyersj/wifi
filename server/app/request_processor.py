from flask import jsonify

from app import app, debug, error
from packets_pb2 import Payload
from packet_handler import ProbeRequestHandler, ProbeResponseHandler


class Processor(object):
    
    def __init__(self, data=None):
        self.success = True
        self.error = ""
        self.payload = self.parse(data)

    def parse(self, data):
        payload = None
        try:
            payload = Payload()
            payload.ParseFromString(data)
        except Exception as e:
            self.success = False
            self.error = e
        return payload
    
    def response(self):
        ret_val = {"success":self.success}
        if self.error: ret_val["error"] = self.error
        if self.success: ret_val["count"] = len(self.payload.data)
        ret_val["type"] = type(self).__name__
        return jsonify(ret_val)
   
    def run(self):
        if not self.success or not self.payload.data: return self.response()
        kwargs = {"location":self.payload.location, "sensor":self.payload.sensor}
        for data in self.payload.data:
            handler = None
            if data.subtype == "0x05":
                handler = ProbeResponseHandler(data, **kwargs)
            elif data.subtype == "0x04":
                handler = ProbeRequestHandler(data, **kwargs)
            else: error("unhandled packet type")
            handler.process()
        return self.response()


