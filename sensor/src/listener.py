import os
import sys
import time
import logging
import random
from uuid import uuid1
from datetime import datetime

import pyshark

from monitor import is_monitoring, start_monitoring
from wifi_pb2 import Packet


# grab logger that has already been configured
logger = logging.getLogger('wifi')


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
        logger.debug('received packet: {0}'.format(out))
        return out
    
    def fetch_address_data(self, p, packet):
        source, destination = self.parse_addr(packet)
        if source: p.source = source
        if destination: p.destination = destination
    
    def fetch_meta_data(self, p, packet):
        arrival, freq, signal = self.parse_meta(packet)
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
        logger.info('starting listener')
        while True:
            # if listener crashes because network card disconnects restart
            self._listen()
            logger.error('listener stopped unexpectedly, restarting')

    def _listen(self):
        # make sure monitoring interface is active
        self._init_mon_interface()
        # setup pyshark which provides bindings to tshark
        capture = pyshark.LiveCapture(
            interface=self.config.interface,
            display_filter=self.display_filter,
            bpf_filter=self.bpf_filter
        )
        # continue sniffing forever (unless we crash)
        for packet in capture.sniff_continuously():
            now = float(time.time())
            arrival = float(packet.frame_info.get_field_value("time_epoch"))
            logger.debug("default {0}".format(now - arrival))
            proto_packet = self.processor.process(packet)
            if self.handler: self.handler.handle(proto_packet)

    def _init_mon_interface(self, delay=5):
        interface = self.config.interface
        if not is_monitoring(interface):
            logger.info('start monitoring on interface {0}'.format(interface))
            # try and start monitoring
            start_monitoring(interface)
            # if initial start failed, the network card might be in the process
            # of reconnecting so wait a little before retrying
            while not is_monitoring(interface) and delay < 360:
                logger.warn('failed to start, waiting {0}s'.format(delay))
                time.sleep(delay)
                delay = delay * 2
                msg = 'trying to start monitoring on interface {0}'
                logger.warn(msg.format(interface))
                start_monitoring(interface)
        # check if we were succesful at starting to monitor interface
        if not is_monitoring(interface):
            logger.error("interface {0} is not currently available.".format(interface))
            sys.exit(1)


class SleepListener(Listener):
    """ Listen for data packets (0x20, 0x28) for short intervals then sleep """

    def start(self):
        logger.info('starting data listener')
        while True:
            # if listener crashes because network card disconnects restart
            self._listen()
            logger.info('restarting after sleep')

    def _listen(self):
        # make sure monitoring interface is active
        self._init_mon_interface()
        # setup pyshark which provides bindings to tshark
        capture = pyshark.LiveCapture(
            interface=self.config.interface,
            display_filter=self.display_filter,
            bpf_filter=self.bpf_filter
        )
        # continue sniffing forever (unless we crash)
        start = time.time()
        for packet in capture.sniff_continuously():
            if int(time.time()) - start > 10:
                time.sleep(random.randrange(10, 20, 1))
                break
            now = float(time.time())
            arrival = float(packet.frame_info.get_field_value("time_epoch"))
            logger.debug("data {0}".format(now - arrival))
            proto_packet = self.processor.process(packet)
            if self.handler:
                self.handler.handle(proto_packet)
