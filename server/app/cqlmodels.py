from cassandra.cqlengine import columns
from cassandra.cqlengine.models import Model
from cassandra.cqlengine.usertype import UserType


class Beacon(Model):
    __table_name__ = "beacon"
    mac            = columns.Text(primary_key=True)
    ssid           = columns.Text()

class LocationRecent(Model):
    __table_name__ = "location_recent_data"
    location       = columns.Text(primary_key=True)
    sensor         = columns.Text()
    mac            = columns.Text()
    arrival        = columns.Decimal(primary_key=True)
    subtype        = columns.Text()
    seq            = columns.Integer()
    signal         = columns.Integer()

class MacRecent(Model):
    __table_name__ = "mac_recent_data"
    location       = columns.Text()
    sensor         = columns.Text()
    mac            = columns.Text(primary_key=True)
    arrival        = columns.Decimal(primary_key=True)
    subtype        = columns.Text()
    seq            = columns.Integer()
    signal         = columns.Integer()

class DeviceIndex(Model):
    __table_name__  = "device_index"
    mac             = columns.Text(primary_key=True)
    recent_location = columns.Text()
    recent_sensor   = columns.Text()
    recent_arrival  = columns.Decimal()

class VisitIndex(Model):
    __table_name__  = "visit_index"
    mac             = columns.Text(primary_key=True)
    location        = columns.Text()
    first_arrival   = columns.Decimal(primary_key=True)
    recent_arrival  = columns.Decimal()




