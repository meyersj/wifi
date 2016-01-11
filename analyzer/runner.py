import os
import sys
import time
import subprocess
import math


SCRIPT_DIR = os.path.dirname(os.path.realpath(__file__))
SQL_DIR = os.path.join(SCRIPT_DIR, "psql")


def run(sql, start_time, db):
    command = "psql -f {0} -v start_time={1} -d {2}".format(sql, start_time, db)
    subprocess.call(command, shell=True)


def bucket5_runner(db, start_time=None):
    interval = 60 * 5
    if not start_time:
        start_time = int((math.floor(time.time() / interval) * interval)  - interval)
    sql = os.path.join(SQL_DIR, "bucket5.psql")
    run(sql, start_time, db)


def hourly_runner(db, start_time=None):
    interval = 60 * 60
    if not start_time:
        start_time = int((math.floor(time.time() / interval) * interval)  - interval)
    sql = os.path.join(SQL_DIR, "hourly.psql")
    run(sql, start_time, db)

    
def daily_runner(db, start_time=None):
    interval = 60 * 60 * 24
    if not start_time:
        #start_time = int((math.floor(time.time() / interval) * interval)  - interval)
        start_time = int((math.floor(time.time() / interval) * interval))
    sql = os.path.join(SQL_DIR, "daily.psql")
    run(sql, start_time, db)


def weekly_runner(db, start_time=None):
    interval = 60 * 60 * 24 * 7
    if not start_time:
        #start_time = int((math.floor(time.time() / interval) * interval)  - interval)
        start_time = int((math.floor(time.time() / interval) * interval))
    sql = os.path.join(SQL_DIR, "weekly.psql")
    run(sql, start_time, db)


def main(args):
    if args and len(args) < 3:
        print "Error: No runner specified as argument"
        sys.exit(1)
    
    runner = args[1]
    db = args[2]
    start_time = None
    if len(args) == 4:
        start_time = args[3]
    
    try:
        func_runner = "{0}_runner".format(runner.lower())
        globals()[func_runner](db, start_time=start_time)
    except KeyError:
        print "Error: Invalid runner < {0} >".format(runner)
        print "Valid runners available: [bucket5, hourly, daily, weekly]"
        sys.exit(2)

if __name__ == "__main__":
    main(sys.argv)
