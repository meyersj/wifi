""" Start tshark subprocess and pass received packets to a handler """


import os
import time
import logging
import random
import subprocess
import signal

from .wifi_pb2 import Packet


DEVNULL = open(os.devnull, 'w')
# grab logger that has already been configured
LOGGER = logging.getLogger('wifi')


def cast(value, new_type):
    """ cast value if exists """
    if value:
        return new_type(value)
    return value


class PacketProcessor(object):
    """
    PacketProcessor will process packets received from pyshark.

    The process method will take as input a pyshark packet object
    and return a protobuf Packet object.
    """

    def process(self, packet):
        """ process output from tshark into protobuf 'Packet' object """
        out = Packet()
        out.subtype = "0x" + hex(int(packet[1]))[2:].zfill(2)
        self.fetch_address_data(out, packet)
        self.fetch_meta_data(out, packet)
        return out

    def fetch_address_data(self, proto, packet):
        """ grab source and destination fields from tshark output """
        source, destination = self.parse_addr(packet)
        if source:
            proto.source = source
        if destination:
            proto.destination = destination

    def fetch_meta_data(self, proto, packet):
        """ grab meta data from tshark output """
        arrival, freq, signal_ = self.parse_meta(packet)
        proto.arrival = arrival
        if freq:
            proto.freq = freq
        if signal_:
            proto.signal = signal_
        if proto.subtype == "0x05":
            proto.ssid = packet[2]

    def parse_addr(self, packet):   # pylint: disable-msg=no-self-use
        """ extract address fields via index """
        source = packet[3]
        destination = packet[4]
        return source, destination

    def parse_meta(self, packet):   # pylint: disable-msg=no-self-use
        """ extract meta data fields via index """
        arrival = float(packet[0])
        freq = cast(packet[5], int)
        signal_ = None
        if len(packet) >= 7:
            try:
                # depending on tshark version sometimes signal fields
                # has the form '-64' while sometimes it has the form '-64,-64'
                signal_ = cast(packet[6], int)
            except ValueError:
                signal_ = cast(packet[6].split(',')[0], int)
        return arrival, freq, signal_


class Listener(object): # pylint: disable-msg=too-few-public-methods
    """
    The Listener will start sniffing for packets using a tshark subprocess

    Each received packet will be processed by the PacketProcessor object which
    will extract relavent data fields and build a Packet protobuf object.

    If a handler was attached to the Listener the packet will be passed to
    that object. The handler object must implement a handle method which
    takes as input the protobuf Packet object.
    """

    def __init__(self, cmd="tshark -Ii wlan0", handler=None):
        self.cmd = cmd
        self.processor = PacketProcessor()
        if handler:
            self.handler = handler()
        else:
            self.handler = None

    def start(self):
        """ start packet listener, loop forever in case of crash """
        LOGGER.info('starting listener')
        while True:
            # if listener crashes because network card disconnects restart
            self._listen()
            LOGGER.error('listener stopped unexpectedly, restarting')

    def _create_proc(self):
        """ create tshark process and send output to pipe we will read from """
        return subprocess.Popen(
            self.cmd,
            shell=True,
            stdout=subprocess.PIPE,
            stderr=DEVNULL,
            preexec_fn=os.setsid
        )

    def _listen(self):
        """ start process and read from output pipe """
        proc = self._create_proc()
        # continue sniffing forever (unless we crash)
        for line in iter(proc.stdout.readline, b''):
            data = line.rstrip().split('\t')
            proto_packet = self.processor.process(data)
            if self.handler:
                self.handler.handle(proto_packet)


class SleepListener(Listener):  # pylint: disable-msg=too-few-public-methods
    """ Listen for data packets (0x20, 0x28) for short intervals then sleep """

    def start(self):
        """ start tshark listener, will go to sleep occasionally """
        LOGGER.info('starting data listener')
        while True:
            # if listener crashes because network card disconnects restart
            self._listen()
            LOGGER.info('restarting after sleep')

    def _listen(self):
        proc = self._create_proc()
        # continue sniffing until timeout
        start = time.time()
        for line in iter(proc.stdout.readline, b''):
            packet = line.rstrip().split('\t')
            if int(time.time()) - start > 10:
                time.sleep(random.randrange(10, 20, 1))
                # kill current process after sleep and exit loop
                os.killpg(os.getpgid(proc.pid), signal.SIGTERM)
                break
            # process packet
            proto_packet = self.processor.process(packet)
            if self.handler:
                self.handler.handle(proto_packet)
