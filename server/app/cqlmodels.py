from cassandra.cqlengine import columns
from cassandra.cqlengine.models import Model


class Beacon(Model):
    __table_name__ = "beacon"
    mac            = columns.Text(primary_key=True)
    ssid           = columns.Text()


class Manuf(Model):
    __table_name__ = "manuf"
    prefix         = columns.Text(primary_key=True)
    manuf          = columns.Text()


class Stream(Model):
    __table_name__ = "stream"
    location       = columns.Text(primary_key=True)
    stamp          = columns.TimeUUID(primary_key=True, clustering_order="desc")
    sensor         = columns.Text()
    source         = columns.Text()
    dest           = columns.Text()
    arrival        = columns.Decimal()
    subtype        = columns.Text()
    signal         = columns.Integer()


class Recent(Model):
    __table_name__ = "recent"
    location       = columns.Text(primary_key=True)
    stamp          = columns.TimeUUID(primary_key=True, clustering_order="desc")
    sensor         = columns.Text()
    mac            = columns.Text()
    arrival        = columns.Decimal()
    subtype        = columns.Text()
    seq            = columns.Integer()
    signal         = columns.Integer()


class LocationIndex(Model):
    __table_name__  = "location_index"
    location        = columns.Text(primary_key=True)
    recent_stamp    = columns.TimeUUID(primary_key=True, clustering_order="desc")
    first_stamp     = columns.TimeUUID()
    mac             = columns.Text()

class Visit(Model):
    __table_name__  = "visit"
    mac             = columns.Text(primary_key=True)
    manuf           = columns.Text()
    stamp           = columns.TimeUUID(primary_key=True, clustering_order="desc")
    recent_stamp    = columns.TimeUUID()
    location        = columns.Text()
    first_arrival   = columns.Decimal()
    recent_arrival  = columns.Decimal()
    pings           = columns.List(columns.Decimal, default=[])
    signals         = columns.List(columns.Integer, default=[])
    counts          = columns.List(columns.Integer, default=[])


class ProcessStatus(Model):
    __table_name__  = "process_status"
    location        = columns.Text(primary_key=True)
    last_process    = columns.TimeUUID()




