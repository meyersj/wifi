import os, sys, time
from uuid import uuid1
from datetime import datetime

import pyshark

from wifi_pb2 import Packet


def cast(value, new_type):
    if value: return new_type(value)
    return value


class PacketProcessor(object):
    """
    PacketProcessor will process packets received from pyshark.

    The process method will take as input a pyshark packet object
    and return a protobuf Packet object.
    """
   
    def process(self, packet):
        out = Packet()  
        out.subtype = packet.wlan.get_field_value("fc_type_subtype")
        self.fetch_address_data(out, packet)
        self.fetch_meta_data(out, packet) 
        return out
    
    def fetch_address_data(self, p, packet):
        source, destination = self.parse_addr(packet)
        if source: p.source = source
        if destination: p.destination = destination
    
    def fetch_meta_data(self, p, packet):
        arrival, freq, signal = self.parse_meta(packet)
        p.uuid = str(uuid1())
        p.arrival = arrival
        if freq: p.freq = freq
        if signal: p.signal = signal
        if p.subtype == "0x08": p.ssid = packet.wlan_mgt.get_field_value("ssid")
   
    def parse_addr(self, packet):
        source = packet.wlan.get_field_value("sa")
        destination = packet.wlan.get_field_value("da")
        return source, destination
   
    def parse_meta(self, packet):
        arrival = float(packet.frame_info.get_field_value("time_epoch"))
        freq = cast(packet.radiotap.get_field_value("channel_freq"), int)
        signal = cast(packet.radiotap.get_field_value("dbm_antsignal"), int)
        return arrival, freq, signal

class Listener(object):
    """
    The Listener will start sniffing for packets using the pyshark library.

    Each received packet will be processed by the PacketProcessor object which
    will extract relavent data fields and build a Packet protobuf object.

    If a handler was attached to the Listener the packet will be passed to
    that object. The handler object must implement a handle method which
    takes as input the protobuf Packet object.
    """
   
    def __init__(self, config=None, display_filter="", bpf_filter="", handler=None):
        self.config = config
        self.display_filter = display_filter
        self.bpf_filter = bpf_filter
        self.processor = PacketProcessor()
        if handler: self.handler = handler(config)
        else: self.handler = None
    
    def start(self):
        capture = pyshark.LiveCapture(
            interface=self.config.interface,
            display_filter=self.display_filter,
            bpf_filter=self.bpf_filter
        )
       
        # continue sniffing forever
        for packet in capture.sniff_continuously():
            proto_packet = self.processor.process(packet)
            if self.handler: self.handler.handle(proto_packet)
