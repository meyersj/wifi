""" main runnner to listen for wifi packets """


import os
import logging
import time
from multiprocessing import Process

from .tshark import TSharkBuilder
from .listener import Listener, SleepListener
from .handler import PostHandler as Handler
from .constants import Frames


# setup logging
FORMAT = '%(levelname)s %(asctime)s %(filename)s %(message)s'
logging.basicConfig(format=FORMAT)
LOGGER = logging.getLogger('wifi')
#LOGGER.setLevel(logging.INFO)
LOGGER.setLevel(logging.DEBUG)


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


def start_listener(listener_cls, handler_cls, frame_types):
    """ start main packet listening process """
    # construct tshark shell command
    builder = TSharkBuilder(interface=INTERFACE)
    tshark_cmd = builder.set_subtypes(frame_types).build()
    LOGGER.info("COMMAND: {0}".format(tshark_cmd))
    # create Listener object with correct filter and handler
    listener = listener_cls(
        cmd=tshark_cmd,
        handler=handler_cls
    )
    # start listening for packets in another process
    process = Process(target=listener.start)
    process.start()
    return process


def basic_runner(frame_types):
    """ create basic runner for probe requests/responses """
    return start_listener(Listener, Handler, frame_types)


def default_data_runner():
    """ create listener for both management and data frames """
    # create Listener for probe requests/responses
    default_process = start_listener(Listener, Handler, DEFAULT_FRAME_TYPES)
    # wait for monitoring to start before starting data listener
    time.sleep(5)
    # create SleepListener to listen for data frames in short intervals
    # to prevent those frames from taking over resources
    data_process = start_listener(SleepListener, Handler, DATA_FRAME_TYPES)

    # poll whether our subprocess has died and restart if so
    while True:
        if not default_process.is_alive():
            LOGGER.error("default process died, restarting")
            default_process = start_listener(
                Listener, Handler, DEFAULT_FRAME_TYPES)
        if not data_process.is_alive():
            LOGGER.error("data process died, restarting")
            data_process = start_listener(
                SleepListener, Handler, DATA_FRAME_TYPES)
        time.sleep(30)

def main():
    """ main function """
    default_data_runner()
    #basic_runner()


if __name__ == '__main__':
    main()
