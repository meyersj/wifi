import sys
import os
import logging


# setup logging
FORMAT = '%(levelname)s %(asctime)s %(filename)s %(message)s'   
logging.basicConfig(format=FORMAT)
logger = logging.getLogger('wifi')
logger.setLevel(logging.INFO)
#logger.setLevel(logging.DEBUG)


parent = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
sys.path.insert(0, parent)
try:
    import conf.config as config
    if config.sensor_mac == "XX:XX:XX:XX:XX:XX":
        logger.error("Failed to set config variable 'sensor_mac' in conf/config.py")
        sys.exit(2)
except Exception as e:
    logger.error("Failed to import config file at conf/config.py")
    sys.exit(1)


from listener import Listener
#from handler import Handler
from handler import PostHandler as Handler
from constants import Frames


EXCLUDE_MACS  = [config.sensor_mac]
INCLUDE_FRAME_TYPES   = [
    Frames.ASSOCIATION_REQUEST,
    Frames.ASSOCIATION_RESPONSE,
    Frames.REASSOCIATION_REQUEST,
    Frames.PROBE_REQUEST,
    Frames.PROBE_RESPONSE,
    #Frames.BEACON,
    Frames.DATA,
    Frames.QOS_DATA
]


def construct_filter_expr(expr, joiner, iterable):
    if not iterable: return ""
    elif len(iterable) == 1: return expr.format(iterable[0])
    else: return joiner.join([expr.format(text) for text in iterable])


def main():
    # build filter for packet frame types to pass through
    # and a filter to ignore frames from sensor
    subtype_expr = "wlan.fc.type_subtype == {0}"
    exclude_expr = "wlan.sa != {0}"
    subtype = construct_filter_expr(subtype_expr, " || ", INCLUDE_FRAME_TYPES)
    exclude = construct_filter_expr(exclude_expr, " && ", EXCLUDE_MACS)
    display_filter = "({0}) && ({1})".format(subtype, exclude)
    
    logger.info("filtering for frame subtypes: {0}".format(INCLUDE_FRAME_TYPES))
    logger.info("excluding MAC address: {0}".format(EXCLUDE_MACS))

    # create listener object with an associated handler 
    listener = Listener(
        config=config,
        display_filter=display_filter,
        handler=Handler
    )

    # start sniffing for packets
    listener.start()


if __name__ == '__main__':
    main()
