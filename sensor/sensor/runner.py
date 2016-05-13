""" main runnner to listen for wifi packets """


import os
import logging
import time
import sys
from threading import Thread

from .tshark import TSharkBuilder
from .listener import Listener
from .handler import PostHandler as Handler
from .constants import Frames
from .network import is_available, channel_hopper

# setup logging
FORMAT = '%(levelname)s %(asctime)s %(filename)s %(message)s'
logging.basicConfig(format=FORMAT)
LOGGER = logging.getLogger('wifi')
LOGGER.setLevel(logging.INFO)
#LOGGER.setLevel(logging.DEBUG)


INTERFACE = os.getenv('WIFISENSOR_INTERFACE', 'wlan0')
DEFAULT_FRAME_TYPES = [
    Frames.ASSOCIATION_REQUEST,
    Frames.ASSOCIATION_RESPONSE,
    Frames.REASSOCIATION_RESPONSE,
    Frames.REASSOCIATION_REQUEST,
    Frames.PROBE_REQUEST,
    Frames.PROBE_RESPONSE,
]
DATA_FRAME_TYPES = [
    Frames.DATA,
    Frames.QOS_DATA
]
ALL_FRAME_TYPES = DEFAULT_FRAME_TYPES + DATA_FRAME_TYPES


# check if network interface actually exists
if not is_available(INTERFACE):
    LOGGER.error("interface %s not available, exiting", INTERFACE)
    sys.exit(1)


def start_listener(listener_cls, handler_cls, frame_types):
    """ start main packet listening process """
    # construct tshark shell command
    builder = TSharkBuilder(interface=INTERFACE)
    tshark_cmd = builder.set_subtypes(frame_types).build()
    LOGGER.info("COMMAND: %s", tshark_cmd)
    # create Listener object with correct filter and handler
    listener = listener_cls(
        cmd=tshark_cmd,
        handler=handler_cls
    )
    # start listening for packets in another thread
    thread = Thread(target=listener.start)
    thread.start()
    args = [listener_cls, handler_cls, frame_types]
    return (thread, start_listener, args)


def start_channel_hopping(ifname):
    """ start listening for packets in another thread """
    thread = Thread(target=channel_hopper, args=(ifname,))
    thread.start()
    return (thread, start_channel_hopping, (ifname,))


def basic_runner():
    """ create basic runner for probe requests/responses """
    start_listener(Listener, Handler, ALL_FRAME_TYPES)


def main_runner():
    """ create listener for both management and data frames """
    threads = [
        # start thread that will hop between the different wifi frequencies
        start_channel_hopping(INTERFACE),
        # create listener for probe requests/responses
        start_listener(Listener, Handler, DEFAULT_FRAME_TYPES),
        # create listener to data frames
        start_listener(Listener, Handler, DATA_FRAME_TYPES)
    ]

    # poll to see if any of our threads have died and restart if so
    while True:
        for thread, func, args in threads:
            if not thread.is_alive():
                LOGGER.error("process died, restarting")
                thread, func, args = func(*args) # pylint: disable=bad-option-value
        time.sleep(30)
