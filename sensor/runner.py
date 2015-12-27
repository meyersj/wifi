#!env/bin/python

import sys

try:
    import conf.config as config
    if confg.sensor_mac == "XX:XX:XX:XX:XX:XX":
        print "Failed to set config variable `sensor_mac`"
        print "Run `ifconfig` to find mac address of wifi chip"
        print "Set `sensor_mac` in `conf/config.py`"
        sys.exit(2)
except:
    print "Failed to import `conf/config.py`"
    print "Copy `conf/sample-config.py` to `conf/config.py` and set to correct values"
    sys.exit(1)

from src.Listener import Listener
from src.Handler import Handler
from src.Constants import Frames


EXCLUDE_MACS  = [config.sensor_mac]
INCLUDE_FRAME_TYPES   = [
    Frames.ASSOCIATION_REQUEST,
    Frames.ASSOCIATION_RESPONSE,
    Frames.REASSOCIATION_REQUEST,
    Frames.PROBE_REQUEST
]


def construct_filter_expr(expr, joiner, iterable):
    if not iterable: return ""
    elif len(iterable) == 1: return expr.format(iterable[0])
    else: return joiner.join([expr.format(text) for text in iterable])


def main():
    # build filter for which packet frame types to pass through
    # and filter to ignore frames from sensor
    subtype_expr = "wlan.fc.type_subtype == {0}"
    exclude_expr = "wlan.addr != {0}"
    subtype = construct_filter_expr(subtype_expr, " || ", INCLUDE_FRAME_TYPES)
    exclude = construct_filter_expr(exclude_expr, " && ", EXCLUDE_MACS)
    display_filter = "({0}) && ({1})".format(subtype, exclude)
    
    # create listener object with an associated handler 
    listener = Listener(
        config=config,
        display_filter=display_filter,
        Handler=Handler
    )

    # start sniffing for packets
    listener.start()


if __name__ == '__main__':
    main()
