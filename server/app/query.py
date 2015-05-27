import time, hashlib, datetime


from cassandra.util import max_uuid_from_time

from app import app, debug, error
from cqlmodels import Recent
from cqlmodels import LocationIndex, Visit
from processor import query_wrapper


HOUR_24 = 60 * 24


class Select(object):

    @query_wrapper
    def visits(self, location="", age=HOUR_24, rate=5):
        recent = time.time() - age * 60
        resultset = LocationIndex.objects\
            .filter(location=location)\
            .filter(LocationIndex.recent_stamp > max_uuid_from_time(recent))
        visits = []
        for record in resultset:
            visit = Visit.objects(mac=record.mac, stamp=record.first_stamp).first()
            if visit:
                duration = int(visit.recent_arrival - visit.first_arrival)
               
                if duration == 0: ping_rate = 0
                else: ping_rate = len(visit.pings) / (duration / 60.0)
                
                if rate / 60.0 < ping_rate and duration / 60.0 > 5:
                    debug(str(len(visit.pings)) + " " + str(duration / 60.0))
                    debug(rate)
                
                    pings = filter(
                        lambda x: x > recent,
                        [float(ping) for ping in visit.pings]
                    )
                    data = zip(
                        pings,
                        visit.signals[0:len(pings)],
                        visit.counts[0:len(pings)]
                    )
                    mac_hash = hashlib.md5(record.mac).hexdigest()[0:6]
                    dev = record.mac[-8:]
                    if visit.manuf:
                        device = visit.manuf + "-" + dev
                    else: device = mac_hash
                    
                    m, s = divmod(duration, 60)
                    h, m = divmod(m, 60)
                    stamp = "%d:%02d" % (h, m)
                    
                    visits.append({
                        "mac":record.mac,
                        "duration":stamp,
                        "device":device,
                        "first_arrival":float(visit.first_arrival),
                        "recent_arrival":float(visit.recent_arrival),
                        "data":data
                    })
                else: debug("NONE")
        return {"visits":visits}


    @query_wrapper
    def visitor_history(self, mac=""):
        resultset = Visit.objects.filter(mac=mac).limit(5)
        visits = []
        device = None
        for record in resultset:
            duration = int(record.recent_arrival - record.first_arrival)
            pings = len(record.pings) 
            if duration == 0: ping_rate = 0
            else: ping_rate = pings / (duration / 60.0)
            
            if duration > 1: 
                device = record.mac[-8:]
                if record.manuf: device = record.manuf + "-" + record.mac[-8:]
                else: device = record.mac

                start_time =  time.localtime(int(record.first_arrival))
                end_time =  time.localtime(int(record.recent_arrival))

                datestamp = time.strftime('%A %m/%d', start_time)
                timerange = time.strftime('%I:%M am - ', start_time)
                timerange += time.strftime('%I:%M am', end_time)
                
                m, s = divmod(duration, 60)
                h, m = divmod(m, 60)
                durationstamp = "{0} hr {1} min".format(h, m)
                    
                visits.append({
                    "mac":record.mac,
                    "datestamp":datestamp,
                    "timerange":timerange,
                    "duration":durationstamp,
                    "first_arrival":int(record.first_arrival),
                    "recent_arrival":int(record.recent_arrival),
                    "activity":pings,
                    "rate":int(ping_rate * 60),
                })
        return {"visits":visits, "device":device}



