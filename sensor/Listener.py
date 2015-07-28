import os, sys, time, threading
from uuid import uuid1
from datetime import datetime

import pyshark, requests

import config
from packets_pb2 import Packet, Payload

requests.packages.urllib3.disable_warnings()

TIMEOUT  = config.timeout


class Parser(object):
    
    def cast(self, value, new_type):
        if value: return new_type(value)
        return value
   
    def parse_addr(self, packet):
        sa = packet.wlan.get_field_value("sa")
        ta = packet.wlan.get_field_value("ta")
        da = packet.wlan.get_field_value("da")
        ra = packet.wlan.get_field_value("ra")
        return sa, ta, da, ra
    
    def set_addr(self, p, packet):
        sa, ta, da, ra = self.parse_addr(packet)
        if sa: p.source = sa
        if ta: p.transmitter = ta
        if da: p.destination = da
        if ra: p.receiver = ra
    
    def parse_meta(self, packet):
        arrival = float(packet.frame_info.get_field_value("time_epoch"))
        seq = self.cast(packet.wlan.get_field_value("seq"), int)
        freq = self.cast(packet.radiotap.get_field_value("channel_freq"), int)
        signal = self.cast(packet.radiotap.get_field_value("dbm_antsignal"), int)
        return arrival, seq, freq, signal

    def set_meta(self, p, packet):
        arrival, seq, freq, signal = self.parse_meta(packet)
        p.stamp = str(uuid1())
        p.arrival = arrival
        if seq: p.seq = seq
        if freq: p.freq = freq
        if signal: p.signal = signal
        if p.subtype == "0x08": p.ssid = packet.wlan_mgt.get_field_value("ssid")

    def parse(self, packet):
        p = Packet()  
        p.subtype = packet.wlan.get_field_value("fc_type_subtype")
        self.set_addr(p, packet)
        self.set_meta(p, packet) 
        return p


class Listener(object):
    
    def __init__(self, display_filter="", bpf_filter="", handler=None):
        self.display_filter = display_filter
        self.bpf_filter = bpf_filter
        self.parser = Parser()
        self.handler = handler

    def start(self, timeout=TIMEOUT):
        now = float(time.time()) 
        stop = now + timeout

        capture = pyshark.LiveCapture(
            interface=config.interface,
            display_filter=self.display_filter,
            bpf_filter=self.bpf_filter)
       
        self.handler = self.handler()
        for packet in capture.sniff_continuously():
            self.handler.flush()
            if float(time.time()) > stop: break
            p = self.parser.parse(packet)
            if self.handler:
                self.handler.handle(p)
            else:
                print p.subtype, p.arrival, p.stamp




