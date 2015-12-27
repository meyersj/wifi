#!env/bin/python

import sys

try:
    import conf.config as config
except:
    print "Failed to import `conf/config.py`"
    print "Copy `conf/sample-config.py` to `conf/config.py` and set to correct values"
    sys.exit(1)

from src.Listener import Listener
from src.Handler import PostHandler
from src.Constants import Frames


EXCLUDE  = [config.sensor_mac]
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
    subtype_expr = "wlan.fc.type_subtype == {0}"
    exclude_expr = "wlan.addr != {0}"
    subtype = construct_filter_expr(subtype_expr, " || ", INCLUDE_FRAME_TYPES)
    exclude = construct_filter_expr(exclude_expr, " && ", EXCLUDE)
    display_filter = "({0}) && ({1})".format(subtype, exclude)
    listener = Listener(
        config.interface,
        display_filter=display_filter#, handler=PostHandler
    )
    listener.start()


if __name__ == '__main__':
    main()
