import time


from cassandra.util import max_uuid_from_time

from app import app, debug, error
from cqlmodels import Beacon as BeaconTable
from cqlmodels import MacRecent, LocationRecent
from cqlmodels import DeviceIndex, VisitIndex
from processor import query_wrapper


HOUR_24 = 60 * 24


class Select(object):
   
    def aggregate_recent(self, resultset):
        # aggregate each device into a seperate group
        # sum total of record signal then divide by number
        # of records to get average signal
        devices = {}
        for record in resultset:
            if record.mac not in devices:
                devices[record.mac] = {
                    "count":0,
                    "signal_total":0,
                    "signal_count":0,
                    "last_arrival":record.arrival
                }
            devices[record.mac]["count"] += 1
            devices[record.mac]["first_arrival"] = record.arrival
            if record.signal:
                devices[record.mac]["signal_total"] += record.signal
                devices[record.mac]["signal_count"] += 1
        # formate data export
        # each row is a list of records with the
        # index denoted by the fields list
        summary = []
        for mac, data in devices.iteritems():
            summary.append([
                mac,
                float(data["first_arrival"]),
                float(data["last_arrival"]),
                data["signal_total"] / data["signal_count"],
                data["count"]
            ])
        first_arrival = resultset[len(resultset) - 1]
        recent_arrival = resultset[0].arrival
        return {
            "data":summary,
            "fields":["mac", "first_arrival", "last_arrival", "avg_signal", "count"]
        }

    @query_wrapper
    def recent_location(self, location="", age=15):
        # query cassandra table using location
        # as partition key and using age in minutes
        # as filter
        recent = time.time() - age * 60
        resultset = LocationRecent.objects\
            .filter(location=location)\
            .filter(LocationRecent.stamp > max_uuid_from_time(recent))
        return self.aggregate_recent(resultset)


    @query_wrapper
    def recent_mac(self, mac="", age=HOUR_24):
        # query cassandra table using mac address
        # as partition key and using age in minutes
        # as filter
        recent = time.time() - age * 60
        resultset = MacRecent.objects\
            .filter(MacRecent.mac == mac)\
            .filter(MacRecent.stamp > max_uuid_from_time(recent))
        return self.aggregate_recent(resultset)








