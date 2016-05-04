import sys
import os
from os.path import dirname, abspath
import logging
import time
from multiprocessing import Process

from tshark import TSharkBuilder

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


def start_listener_process(Listener, frame_types):
    # construct tshark shell command
    tshark_cmd_builder = TSharkBuilder(config.interface)
    tshark_cmd_builder.set_subtypes(frame_types)
    tshark_cmd_builder.set_macs(EXCLUDE_MACS)
    tshark_cmd = tshark_cmd_builder.build()
    logger.info(tshark_cmd)
    # create Listener object with correct filter and handler
    listener = Listener(
        config=config,
        cmd=tshark_cmd,
        handler=Handler
    )
    # start listening for packets in another process
    process = Process(target=listener.start)
    process.start()
    return process


def main():
    # create Listener for probe requests/responses
    default_process = start_listener_process(Listener, DEFAULT_FRAME_TYPES)
    # wait for monitoring to start before starting data listener
    time.sleep(5)
    # create SleepListener listens for data frames for short intervals
    # to prevent those frames from taking over resources
    data_process = start_listener_process(SleepListener, DATA_FRAME_TYPES)

    # poll whether our subprocess has died and restart if so
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
