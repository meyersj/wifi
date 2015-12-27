import config
from Listener import Listener
from Handler import PostHandler


ASSOCIATION_REQUEST = "0x00"
ASSOCIATION_RESPONSE = "0x01"
REASSOCIATION_REQUEST = "0x02"
REASSOCIATION_RESPONSE = "0x03"
PROBE_REQUEST = "0x04"
PROBE_RESPONSE = "0x05"
BEACON = "0x08"
DATA = "0x20"
QOS_DATA = "0x28"


EXCLUDE  = [config.sensor_mac]
FRAME_TYPES   = [
    ASSOCIATION_REQUEST,
    #ASSOCIATION_RESPONSE,
    REASSOCIATION_REQUEST,
    #REASSOCIATION_RESPONSE,
    PROBE_REQUEST
    #PROBE_RESPONSE,
    #BEACON
]


def construct(expr, joiner, iterable):
    if not iterable: return ""
    elif len(iterable) == 1: return expr.format(iterable[0])
    else: return joiner.join([expr.format(text) for text in iterable])


def main():
    subtype_expr = "wlan.fc.type_subtype == {0}"
    exclude_expr = "wlan.addr != {0}"
    subtype = construct(subtype_expr, " || ", FRAME_TYPES)
    exclude = construct(exclude_expr, " && ", EXCLUDE)
    
    display_filter = "({0}) && ({1})".format(subtype, exclude)

    listener = Listener(display_filter=display_filter, handler=PostHandler)
    listener.start()


if __name__ == '__main__':
    main()



