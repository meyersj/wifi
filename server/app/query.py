import time, hashlib


from cassandra.util import max_uuid_from_time

from app import app, debug, error
from cqlmodels import Recent
from cqlmodels import LocationIndex, Visit
from processor import query_wrapper


HOUR_24 = 60 * 24


class Select(object):
   
    def visits(self, location="", age=HOUR_24, min_records=0):
        recent = time.time() - age * 60
        resultset = LocationIndex.objects\
            .filter(location=location)\
            .filter(LocationIndex.recent_stamp > max_uuid_from_time(recent))
        visits = []
        for record in resultset:
            visit = Visit.objects(mac=record.mac, stamp=record.first_stamp).first()
            if visit and len(visit.pings) >= min_records:
                data = zip(
                    [float(ping) for ping in visit.pings],
                    visit.signals,
                    visit.counts
                )
                mac_hash = hashlib.md5(record.mac).hexdigest()[0:6]
                if visit.manuf:
                    device = visit.manuf + "-" + mac_hash
                else: device = mac_hash
                
                visits.append({
                    "device":device,
                    "first_arrival":float(visit.first_arrival),
                    "recent_arrival":float(visit.recent_arrival),
                    "data":data
                })
        return {"visits":visits}




