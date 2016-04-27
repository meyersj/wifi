import sys
import os
from os.path import dirname, abspath
import logging
import time
from multiprocessing import Process


# setup logging
FORMAT = '%(levelname)s %(asctime)s %(filename)s %(message)s'   
logging.basicConfig(format=FORMAT)
logger = logging.getLogger('wifi')
logger.setLevel(logging.INFO)
#logger.setLevel(logging.DEBUG)

parent = dirname(dirname(abspath(__file__)))
sys.path.insert(0, parent)
try:
    import conf.config as config
    if config.sensor_mac == "XX:XX:XX:XX:XX:XX":
        logger.error("Failed to set config variable 'sensor_mac' in conf/config.py")
        sys.exit(2)
except Exception as e:
    logger.error("Failed to import config file at conf/config.py")
    sys.exit(1)


from listener import Listener, SleepListener
#from handler import Handler
from handler import PostHandler as Handler
from constants import Frames


EXCLUDE_MACS  = [config.sensor_mac]
DEFAULT_FRAME_TYPES   = [
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


def construct_filter_expr(expr, joiner, iterable):
    if not iterable: return ""
    elif len(iterable) == 1: return expr.format(iterable[0])
    else: return joiner.join([expr.format(text) for text in iterable])


def build_filter(include_frames, exclude_mac):
    exclude_expr = "wlan.sa != {0}"
    subtype_expr = "wlan.fc.type_subtype == {0}"
    # construct expressions
    exclude = construct_filter_expr(exclude_expr, " && ", exclude_mac)
    subtype = construct_filter_expr(subtype_expr, " || ", include_frames)
    display_filter = "({0}) && ({1})".format(subtype, exclude)
    return display_filter


def start_listener_process(Listener, frame_types):
    # construct tshark packet filter
    display_filter = build_filter(frame_types, EXCLUDE_MACS)
    logger.info("filtering for frame subtypes: {0}".format(display_filter))
    # create Listener object with correct filter and handler
    listener = Listener(
        config=config,
        display_filter=display_filter,
        handler=Handler
    )
    # start listening for packets in another process
    process = Process(target=listener.start)
    process.start()
    return process


def main():
    logger.info("excluding MAC address: {0}".format(EXCLUDE_MACS))
    # create Listener for probe requests/responses
    default_process = start_listener_process(Listener, DEFAULT_FRAME_TYPES)
    # wait for monitoring to start before starting data listener
    time.sleep(5)
    # create SleepListener listens for data frames for short intervals
    # to prevent those frames from taking over resources
    data_process = start_listener_process(SleepListener, DATA_FRAME_TYPES)

    # poll whether our subprocess have died and restart if so
    while True:
        if not default_process.is_alive():
            logger.error("default process died, restarting")
            default_process = start_listener_process(Listener, DEFAULT_FRAME_TYPES)
        if not data_process.is_alive():
            logger.error("data process died, restarting")
            data_process = start_listener_process(SleepListener, DATA_FRAME_TYPES)
        time.sleep(30)
    

if __name__ == '__main__':
    main()
