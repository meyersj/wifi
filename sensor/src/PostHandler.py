import requests
import time
import threading

from Handler import IHandler


class Handler(IHandler):

    def __init__(self, config):
        self.config = config
        self.start = self.unique = float(time.time())
        self.data = []
        self.keys = set()

    def handle(self, packet):
        thread = threading.Thread(
            name="post",
            target=self.post,
            kwargs={"packet":packet}
        )
        thread.start()

    # runs in a background thread
    def post(self, packet=None):
        headers = {'Content-type':'application/x-protobuf'}
        payload = packet.SerializeToString()
        response = requests.post(
            self.config.endpoint,
            data=payload,
            headers=headers,
            verify=False,
            timeout=5
        )
        print "Status: " + str(response.status_code), "\n", packet
