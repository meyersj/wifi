"""
Construct tshark command to be ran as subprocess
"""

import os


DEVNULL = open(os.devnull, 'w')
FIELDS = [
    'frame.time_epoch',
    'wlan.fc.type_subtype',
    'wlan_mgt.ssid',
    'wlan.sa',
    'wlan.da',
    'radiotap.channel.freq',
    'radiotap.dbm_antsignal'
]
SUBTYPES = ['0x04', '0x05', '0x20', '0x28']


class TSharkBuilder(object):
    """ helper class to construct tshark command """

    def __init__(self, interface='wlan0'):
        self.interface = interface
        self.fields = FIELDS
        self.subtypes = SUBTYPES

    def build(self):
        """ construct tshark command """
        tshark = "tshark -i {0} -f 'not multicast' -l -Y '{1}' -T fields {2}"
        return tshark.format(self.interface, self._subtypes(), self._fields())

    def set_fields(self, fields):
        """ set fields that tshark should output """
        self.fields = fields
        return self

    def set_subtypes(self, subtypes):
        """ set subtype of packets that should be included in output """
        self.subtypes = subtypes
        return self

    def _fields(self):
        """ construct fields that tshark should output """
        cmd = "-e {0}"
        return " ".join([cmd.format(field) for field in self.fields])

    def _subtypes(self):
        """ construct subtype display filter """
        filter_ = "wlan.fc.type_subtype == {0}"
        filters = [filter_.format(subtype) for subtype in self.subtypes]
        if self.subtypes:
            return " || ".join(filters)
        return ""
