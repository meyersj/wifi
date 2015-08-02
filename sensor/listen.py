#!env/bin/python

import config
from Listener import Listener
from Handler import PostHandler


EXCLUDE  = [config.sensor_mac]
FRAMES   = ["0x04"]


def construct(expr, joiner, iterable):
    if not iterable: return ""
    elif len(iterable) == 1: return expr.format(iterable[0])
    else: return joiner.join([expr.format(text) for text in iterable])


def main():
    subtype_expr = "wlan.fc.type_subtype == {0}"
    exclude_expr = "wlan.addr != {0}"
    subtype = construct(subtype_expr, " || ", FRAMES)
    exclude = construct(exclude_expr, " && ", EXCLUDE)
    
    display_filter = "({0}) && ({1})".format(subtype, exclude)

    listener = Listener(display_filter=display_filter, handler=PostHandler)
    listener.start()


if __name__ == '__main__':
    main()



