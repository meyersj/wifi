import requests
import time
import threading
import logging

from wifi_pb2 import Payload


logger = logging.getLogger('wifi')


class Handler(object):
    
    def __init__(self, config):
        pass

    def handle(self, packet):
        print packet


class PostHandler(Handler):

    def __init__(self, config):
        now = float(time.time())
        self.config = config
        self.payload_timer = now + self.config.payload_timer
        self.distinct_timer = now + self.config.distinct_timer
        self.data = []
        self.distinct = {}
   
    def handle(self, packet):
        # check if timer is expired to send payload
        now = float(time.time())
        self.flush(now)
        key = "{0}-{1}".format(packet.source, packet.destination)
        if key not in self.distinct:
            self.distinct[key] = now + self.config.distinct_timer
            self.data.append(packet)
        elif self.distinct[key] < now - self.config.distinct_timer:
            self.data.append(packet)
            self.distinct[key] = now + self.config.distinct_timer
    
    def send(self):
        if not self.data:
            return
        self.__send()

    def __send(self):
        # construct payload
        payload = Payload()
        payload.location = "location"
        payload.sensor = "sensor"
        payload.data.extend(self.data)

        # make request in background thread
        thread = threading.Thread(
            name="post",
            target=self.post,
            kwargs={"payload":payload.SerializeToString()}
        )
        thread.start()

    # runs in a background thread
    def post(self, payload=None):
        headers = {'Content-type':'application/x-protobuf'}
        response = requests.post(
            self.config.endpoint,
            data=payload,
            headers=headers,
            verify=True,
            timeout=5
        )
        logger.debug("status code: {0}".format(response.status_code))

    def flush(self, now):
        if now < self.payload_timer:
            return
        logger.info("flusing {0} records".format(len(self.data)))
        self.send()
        self.payload_timer = float(time.time()) + self.config.payload_timer
        new_distinct = {} 
        for key, value in self.distinct.iteritems():
            if value >= now - self.config.distinct_timer:
                new_distinct[key] = value
        self.distinct = new_distinct
        self.data = []
