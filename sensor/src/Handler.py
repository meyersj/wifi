import requests
import time
import threading

from proto.packets_pb2 import Payload


class IHandler(object):
   
    def handle(self, packet):
        pass


class Handler(IHandler):

    def handle(self, packet):
        print packet


class PostHandler(IHandler):

    def __init__(self, config):
        self.config = config
        self.start = self.unique = float(time.time())
        self.data = []
        self.keys = set()

    def handle(self, packet):
        self.flush()
        print packet.arrival, packet.source
        if packet.source not in self.keys:
            self.keys.add(packet.source)
            self.data.append(packet)

    def flush(self):
        now = float(time.time())
        if self.unique + config.unique < now:
            self.keys = set()
            self.unique = now
        if self.start + config.interval < now:
            self.send()
            self.start = now
            self.data = []

    def payload_builder(self):
        payload = Payload()
        payload.location = self.config.location
        payload.sensor = self.config.sensor
        payload.data.extend(self.data)
        return payload.SerializeToString()
      
    # runs in a background thread
    def post(self, payload=None):
        headers = {'Content-type':'application/x-protobuf'}
        response = requests.post(self.config.endpoint,
            data=payload, headers=headers, verify=False, timeout=5)
        print response.text

    def send(self):
        payload = self.payload_builder()
        thread = threading.Thread(
            name="submit",
            target=self.post,
            kwargs={"payload":payload}
        )
        thread.start()




