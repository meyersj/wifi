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
   
    def __init__(self, interface):
        self.interface = interface
        self.fields = FIELDS
    
    def build(self):
        bpf_filter = "not broadcast and not multicast"
        tshark = "tshark -i {0} -l -f '{1}' -Y '{2}' -T fields {3}"
        display_filter = "({0}) && ({1})".format(self._subtypes(), self._macs())
        return tshark.format(
                self.interface, bpf_filter, display_filter, self._fields()
        ) 

    def set_fields(self, fields):
        self.fields = fields

    def set_subtypes(self, subtypes):
        self.subtypes = subtypes
    
    def set_macs(self, macs):
        self.macs = macs
    
    def _fields(self):
        cmd = "-e {0}"
        return " ".join([cmd.format(field) for field in self.fields])
    
    def _subtypes(self):
        filter_ = "wlan.fc.type_subtype == {0}"
        if self.subtypes:
            return " || ".join([filter_.format(subtype) for subtype in self.subtypes])
        return ""

    def _macs(self):
        filter_ = "wlan.sa != {0}"
        if self.macs:
            return " && ".join([filter_.format(mac) for mac in self.macs])
        return ""
