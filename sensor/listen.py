import os, sys, time, threading
from uuid import uuid1
from datetime import datetime

import pyshark, requests

import config
from packets_pb2 import Packet, Payload

requests.packages.urllib3.disable_warnings()

INTERVAL = config.interval
TIMEOUT  = config.timeout
UNIQUE   = config.unique

EXCLUDE  = [config.sensor_mac]
FRAMES   = ["0x04", "0x05"]#, "0x08"]

class Handler(object):
    
    def __init__(self, unique, dump, interval):
        self.endpoint = config.endpoint
        self.unique = unique
        self.dump = dump
        self.interval = interval
        self.keys = set()
        self.data = []

    def cast(self, value, new_type):
        if value: return new_type(value)
        return value
    
    def payload_builder(self):
        payload = Payload()
        payload.location = config.location
        payload.sensor = config.sensor
        payload.data.extend(self.data)
        return payload.SerializeToString()

    def flush(self):
        now = float(time.time())
        if now >= self.unique:
            self.unique = now + UNIQUE
            self.keys = set()
        if now >= self.dump:
            self.dump = now + self.interval
            self.send()
            self.data = []
      
    # runs in a background thread
    def post(self, payload=None):
        headers = {'Content-type':'application/x-protobuf'}
        response = requests.post(self.endpoint,
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
    
    def set_field(self, field, value):
        if value: field = value
    
    def parse(self, packet):
        sub = packet.wlan.get_field_value("fc_type_subtype")
        sa = packet.wlan.get_field_value("sa")
        ta = packet.wlan.get_field_value("ta")
        da = packet.wlan.get_field_value("da")
        ra = packet.wlan.get_field_value("ra")
        
        key = (sub, sa, ta, da, ra)
        if key in self.keys: return
        
        p = Packet()  
        p.subtype = sub
        if sa: p.source = sa
        if ta: p.transmitter = ta
        if da: p.destination = da
        if ra: p.receiver = ra
        p.stamp = str(uuid1())
        p.arrival = float(packet.frame_info.get_field_value("time_epoch"))
        seq = self.cast(packet.wlan.get_field_value("seq"), int)
        freq = self.cast(packet.radiotap.get_field_value("channel_freq"), int)
        signal = self.cast(packet.radiotap.get_field_value("dbm_antsignal"), int)

        if seq: p.seq = seq
        if freq: p.freq = freq
        if signal: p.signal = signal
        if sub == "0x08": p.ssid = packet.wlan_mgt.get_field_value("ssid")

        self.keys.add(key)
        self.data.append(p)
        
        #print datetime.fromtimestamp((uuid1().time - 0x01b21dd213814000L)*100/1e9)
        print sub, p.arrival

        
class Listener(object):

    
    def __init__(self, display_filter="", bpf_filter=""):
        self.display_filter = display_filter
        self.bpf_filter = bpf_filter

    def listen(self, timeout=TIMEOUT, interval=INTERVAL):
        now = float(time.time()) 
        stop = now + timeout
        self.handler = Handler(now + UNIQUE, now + interval, interval)

        capture = pyshark.LiveCapture(
            interface=config.interface,
            display_filter=self.display_filter,
            bpf_filter=self.bpf_filter)
        for packet in capture.sniff_continuously():
            if float(time.time()) > stop: break
            self.handler.flush()
            self.handler.parse(packet)
        self.handler.send()

def construct(expr, joiner, iterable):
    if not iterable: return ""
    elif len(iterable) == 1: return expr.format(iterable[0])
    else: return joiner.join([expr.format(text) for text in iterable])


def main():
    subtype_expr = "wlan.fc.type_subtype == {0}"
    exclude_expr = "wlan.addr != {0}"
    subtype = construct(subtype_expr, " || ", FRAMES)
    exclude = construct(exclude_expr, " && ", EXCLUDE)
    
    display_filter = "({0}) && ({1})".format(subtype, exclude)

    listener = Listener(display_filter=display_filter)
    for i in range(0, 5): listener.listen()


if __name__ == '__main__':
    main()



