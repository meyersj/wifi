import sys
import os

parent = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
sys.path.insert(0, parent)
try:
    import conf.config as config
    if config.sensor_mac == "XX:XX:XX:XX:XX:XX":
        print
        print "Failed to set config variable `sensor_mac`"
        print " - run `ifconfig` to find mac address of wifi chip"
        print " - set `sensor_mac` in `conf/config.py`"
        print
        sys.exit(2)
except Exception as e:
    print
    print e
    print
    print "Failed to import `conf/config.py`"
    print " - copy `conf/sample-config.py` to `conf/config.py`"
    print " - set config variables to correct values"
    print
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
    Frames.BEACON,
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
