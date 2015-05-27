import time, sys, os

from cassandra.cqlengine import connection
from cassandra.cqlengine.management import sync_table, sync_type
from cassandra.util import LOWEST_TIME_UUID

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import CASSANDRA_NODES, CASSANDRA_KEYSPACE
from app.cqlmodels import Beacon, Recent, Visit, LocationIndex, ProcessStatus


DEFAULT_LOCATION = "apartment"


def query_wrapper(func):
    """ closure that connects to the cluster, excutes the input function
        and disconnects from the cluster """
    def execute(*args, **kwargs):
        connection.setup(
            CASSANDRA_NODES,
            CASSANDRA_KEYSPACE,
            retry_connect=True
        )   
        cluster = connection.get_cluster()
        sync_table(Beacon)
        sync_table(Recent)
        sync_table(LocationIndex) 
        sync_table(Visit) 
        sync_table(ProcessStatus) 
        return func(*args, **kwargs)
    return execute


@query_wrapper
def runner():
    last_process = get_last_process()
    if last_process: stamp = last_process
    else: stamp = LOWEST_TIME_UUID
    resultset = query_recent(stamp=stamp)
    if resultset:
        new_stamp = resultset[0].stamp
        # pipeline: group -> process -> update
        print update(process(group(resultset)))
        set_last_process(new_stamp)


def group(resultset):
    # it is assumed the data comes sorted in descending
    # order so data is reveresed to be returned in ascending order
    devices = {}
    for record in resultset:
        if record.mac not in devices:
            devices[record.mac] = []
        devices[record.mac].insert(0, record)
    return devices 


def process(groups):
    data = []
    for mac, records in groups.iteritems():
        count = len(records)
        try:
            avg_signal = reduce(
                lambda x,y: x+y,
                [ record.signal for record in records ]
            ) / count
        except TypeError: avg_signal = 99999 # record.signal was probably null
        timestamp = (records[0].arrival + records[count-1].arrival) / 2
        data.append({
            "mac":mac,
            "signal":avg_signal,
            "ping":timestamp,
            "count":count
        })
    return data


def update(data):
    updated = 0
    total = 0
    for device in data:
        total += 1
        visit = Visit.objects.filter(mac=device["mac"]).first()
        if visit:
            updated += 1
            keys = {"mac":visit.mac, "stamp":visit.stamp}
            Visit.objects(**keys).update(pings__append=[device["ping"]])
            Visit.objects(**keys).update(signals__append=[device["signal"]])
            Visit.objects(**keys).update(counts__append=[device["count"]])
    return {"total":total, "updated":updated}


def get_last_process(location=DEFAULT_LOCATION):
    status = ProcessStatus.objects.filter(location=location).first()
    if status: return status.last_process
    return None


def set_last_process(stamp, location=DEFAULT_LOCATION):
    ProcessStatus.objects(location=location)\
        .update(last_process=stamp)


def query_recent(stamp=LOWEST_TIME_UUID, location=DEFAULT_LOCATION):
    print stamp
    resultset = Recent.objects\
        .filter(location=location)\
        .filter(Recent.stamp > stamp)
    return resultset


def main():
    runner()


if __name__ == "__main__":
   time.sleep(15)
   main()



