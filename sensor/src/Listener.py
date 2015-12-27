import os, sys, time, threading
from uuid import uuid1
from datetime import datetime

import pyshark, requests

from proto.packets_pb2 import Packet, Payload

requests.packages.urllib3.disable_warnings()


def cast(value, new_type):
    if value: return new_type(value)
    return value


"""
PacketProcessor will process packets received from pyshark.

The process method will take as input a pyshark packet object
and return a protobuf Packet object.
"""
class PacketProcessor(object):
    
    def process(self, packet):
        out = Packet()  
        out.subtype = packet.wlan.get_field_value("fc_type_subtype")
        self.fetch_address_data(out, packet)
        self.fetch_meta_data(out, packet) 
        return out
    
    def fetch_address_data(self, p, packet):
        sa, ta, da, ra = self.parse_addr(packet)
        if sa: p.source = sa
        if ta: p.transmitter = ta
        if da: p.destination = da
        if ra: p.receiver = ra
    
    def fetch_meta_data(self, p, packet):
        arrival, seq, freq, signal = self.parse_meta(packet)
        p.uuid = str(uuid1())
        p.arrival = arrival
        if seq: p.seq = seq
        if freq: p.freq = freq
        if signal: p.signal = signal
        if p.subtype == "0x08": p.ssid = packet.wlan_mgt.get_field_value("ssid")
   
    def parse_addr(self, packet):
        sa = packet.wlan.get_field_value("sa")
        ta = packet.wlan.get_field_value("ta")
        da = packet.wlan.get_field_value("da")
        ra = packet.wlan.get_field_value("ra")
        return sa, ta, da, ra
   
    def parse_meta(self, packet):
        arrival = float(packet.frame_info.get_field_value("time_epoch"))
        seq = cast(packet.wlan.get_field_value("seq"), int)
        freq = cast(packet.radiotap.get_field_value("channel_freq"), int)
        signal = cast(packet.radiotap.get_field_value("dbm_antsignal"), int)
        return arrival, seq, freq, signal


class Listener(object):
    
    def __init__(self, interface, display_filter="", bpf_filter="", Handler=None):
        self.interface = interface
        self.display_filter = display_filter
        self.bpf_filter = bpf_filter
        self.processor = PacketProcessor()
        if Handler: self.handler = Handler()
        else: self.handler = None
    
    def start(self, timeout=60):
        now = float(time.time()) 
        stop = now + timeout

        capture = pyshark.LiveCapture(
            interface=self.interface,
            display_filter=self.display_filter,
            bpf_filter=self.bpf_filter
        )
        
        for packet in capture.sniff_continuously():
        #self.handler.flush()
        #    if float(time.time()) > stop: break
            proto_packet = self.processor.process(packet)
            #if self.handler:
            #    self.handler.handle(proto_packet)
            #else:
            print proto_packet
            #print p.subtype, p.arrival, p.stamp
