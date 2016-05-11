""" Basic Constants """


class Frames(object):   # pylint: disable=too-few-public-methods
    """ subtypes for interesting wifi frames """

    ASSOCIATION_REQUEST = "0x00"            # device
    ASSOCIATION_RESPONSE = "0x01"           # AP
    REASSOCIATION_REQUEST = "0x02"          # device
    REASSOCIATION_RESPONSE = "0x03"         # AP
    PROBE_REQUEST = "0x04"                  # device
    PROBE_RESPONSE = "0x05"                 # AP
    BEACON = "0x08"                         # AP
    DATA = "0x20"                           # device | AP
    QOS_DATA = "0x28"                       # device | AP
