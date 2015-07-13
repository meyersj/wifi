from flask import jsonify
from cassandra.cqlengine import connection
from cassandra.cqlengine.management import sync_table, sync_type

from app import app, debug, error
from packets_pb2 import Payload
from cqlmodels import Stream as StreamTable
from cqlmodels import Manuf, Beacon, Recent, Visit, LocationIndex, ProcessStatus
from handlers import FrameHandler
from handlers import BeaconHandler, ProbeRequestHandler, ProbeResponseHandler


def query_wrapper(func):
    """ connects to the cluster, excutes the input function
        and disconnects from the cluster """
    def execute(*args, **kwargs):
        connection.setup(
            app.config["CASSANDRA_NODES"],
            app.config["CASSANDRA_KEYSPACE"],
            retry_connect=True
        )
        cluster = connection.get_cluster()
        sync_table(Beacon)
        sync_table(Recent)
        sync_table(Visit) 
        sync_table(LocationIndex) 
        sync_table(ProcessStatus) 
        sync_table(Manuf) 
        sync_table(StreamTable) 
        return func(*args, **kwargs)
    return execute

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
    
    @query_wrapper
    def run(self):
        if not self.success or not self.payload.data: return self.response()
        kwargs = {"location":self.payload.location, "sensor":self.payload.sensor}
        for data in self.payload.data:
            handler = None
            if data.subtype == "0x08":
                handler = BeaconHandler(data, **kwargs)
            elif data.subtype == "0x05":
                handler = ProbeResponseHandler(data, **kwargs)
            elif data.subtype == "0x04":
                handler = ProbeRequestHandler(data, **kwargs)
            else: error("unhandled packet type")
            handler.process()
        return self.response()


class Stream(Processor):
    
    @query_wrapper
    def run(self):
        if not self.success or not self.payload.data: return self.response()
        kwargs = {"location":self.payload.location, "sensor":self.payload.sensor}
        for data in self.payload.data:
            handler = FrameHandler(data, **kwargs)
            handler.process()
        return self.response()
   

