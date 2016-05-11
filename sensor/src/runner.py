""" main runnner to listen for wifi packets """


import os
import logging
import time
import sys
from multiprocessing import Process

from .tshark import TSharkBuilder
from .listener import Listener#, SleepListener
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


# check if provided interface actually exists
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
    # start listening for packets in another process
    process = Process(target=listener.start)
    process.start()
    args = [listener_cls, handler_cls, frame_types]
    return (process, start_listener, args)


def start_channel_hopping(ifname):
    """ start listening for packets in another process """
    process = Process(target=channel_hopper, args=(ifname,))
    process.start()
    return (process, start_channel_hopping, (ifname,))


def basic_runner(frame_types):
    """ create basic runner for probe requests/responses """
    return start_listener(Listener, Handler, frame_types)


def default_data_runner():
    """ create listener for both management and data frames """
    processes = []

    # start process that will hop between the different wifi frequencies
    processes.append(start_channel_hopping(INTERFACE))
    # create listener for probe requests/responses
    processes.append(start_listener(Listener, Handler, DEFAULT_FRAME_TYPES))
    # create listener to data frames
    processes.append(start_listener(Listener, Handler, DATA_FRAME_TYPES))

    # poll to see if any of our subprocesses have died and restart if so
    while True:
        for process, func, args in processes:
            if not process.is_alive():
                LOGGER.error("process died, restarting")
                print "before", processes
                process, func, args = func(*args) # pylint: disable=bad-option-value
                print "after", processes
        time.sleep(30)


def main():
    """ main function """
    default_data_runner()
    #basic_runner()


if __name__ == '__main__':
    main()
