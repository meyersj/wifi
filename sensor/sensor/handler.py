""" classes to handle packets that are picked up from sensor """


import os
import logging
import threading
import time
import requests

from .wifi_pb2 import Payload


PAYLOAD_TIMER = int(os.getenv('WIFISENSOR_PAYLOAD_TIMER', 5))
DISTINCT_TIMER = int(os.getenv('WIFISENSOR_DISTINCT_TIMER', 15))
SERVER_ENDPOINT = os.getenv('WIFISENSOR_SERVER_ENDPOINT', '')

LOGGER = logging.getLogger('wifi')


class Handler(object):  # pylint: disable-msg=too-few-public-methods
    """ default handler """

    def handle(self, packet):   # pylint: disable-msg=no-self-use
        """ handle packet """
        print packet


class PostHandler(Handler): # pylint: disable-msg=too-few-public-methods
    """ handler to HTTP POST data to go-server API """

    def __init__(self):
        now = float(time.time())
        self.payload_timer = now + PAYLOAD_TIMER
        self.distinct_timer = now + DISTINCT_TIMER
        self.data = []
        self.distinct = {}

    def handle(self, packet):
        # check if timer is expired to send payload
        now = float(time.time())
        self.flush(now)
        key = "{0}-{1}".format(packet.source, packet.destination)
        if key not in self.distinct:
            self.distinct[key] = now + PAYLOAD_TIMER
            self.data.append(packet)
        elif self.distinct[key] < now - DISTINCT_TIMER:
            self.data.append(packet)
            self.distinct[key] = now + DISTINCT_TIMER

    def send(self):
        """ call internal send """
        if not self.data:
            return
        self.__send()

    def __send(self):
        """ build protobuf payload and make request """
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

    def post(self, payload=None): # pylint: disable-msg=no-self-use
        """ POST data to server, this function runs in background thread """
        if not SERVER_ENDPOINT:
            msg = 'WIFISENSOR_SERVER_ENDPOINT environment variable not set\n'
            msg += 'data is not being persisted'
            LOGGER.error(msg)
            return
        headers = {'Content-type':'application/x-protobuf'}
        response = requests.post(
            SERVER_ENDPOINT,
            data=payload,
            headers=headers,
            verify=True,
            timeout=5
        )
        LOGGER.debug("status code: %s", response.status_code)

    def flush(self, now):
        """ flush data every N seconds to limit network calls """
        if now < self.payload_timer:
            return
        LOGGER.info("flusing %s records", len(self.data))
        self.send()
        self.payload_timer = float(time.time()) + PAYLOAD_TIMER
        new_distinct = {}
        for key, value in self.distinct.iteritems():
            if value >= now - DISTINCT_TIMER:
                new_distinct[key] = value
        self.distinct = new_distinct
        self.data = []
