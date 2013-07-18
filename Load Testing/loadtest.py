#!/usr/bin/python
__author__ = 'ajmills, datkinson'
import sys, getopt
import httplib2
import random
import socket
import time
from threading import Event
from threading import Thread
from threading import current_thread
from urllib import urlencode

# Set up counters
TOTAL = 0
RESPONSES = {}

# Default values
# How many threads should be running at peak load.
NUM_THREADS = 10

# How many minutes the test should run with all threads active.
TIME_AT_PEAK_QPS = 10 # minutes

# How many seconds to wait between starting threads.
# Shouldn't be set below 30 seconds.
DELAY_BETWEEN_THREAD_START = 1 # seconds

# URL of the site to test
URL = ''

# o == option
# a == argument passed to the o
USAGE = "Usage: %s -t threads -m mins_to_run_test -d delay_between_threads -u url_of_site_to_test"
try:
    myopts, args = getopt.getopt(sys.argv[1:],"t:m:d:u:")
except getopt.GetoptError as e:
    print (str(e))
    print(USAGE % sys.argv[0])
    sys.exit(2)

for o, a in myopts:
    if o == '-t':
        if a.isdigit():
            NUM_THREADS = int(a)
    elif o == '-m':
        if a.isdigit():
            TIME_AT_PEAK_QPS = float(a)
    elif o == '-d':
        if a.isdigit():
            DELAY_BETWEEN_THREAD_START = float(a)
    elif o == '-u':
        URL = a
if not URL:
    print("Error: No URL specified")
    print(USAGE % sys.argv[0])
    sys.exit(2)

quitevent = Event()

def percentage(part, whole):
  return 100 * float(part)/float(whole)

def threadproc():
    global TOTAL
    global RESPONSES

    """This function is executed by each thread."""
    print "Thread started: %s" % current_thread().getName()
    h = httplib2.Http(timeout=30)
    while not quitevent.is_set():
        TOTAL += 1
        try:
            # HTTP requests to exercise the server go here
            # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
            resp, content = h.request(URL)
            if resp.status != 200:
                print "Response not OK"
            # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
            if resp.status in RESPONSES:
                RESPONSES[resp.status] = RESPONSES[resp.status]+1
            else:
                RESPONSES[resp.status] = 1
        except socket.timeout:
            pass

    print "Thread finished: %s" % current_thread().getName()

if __name__ == "__main__":
    runtime = (TIME_AT_PEAK_QPS * 60 + DELAY_BETWEEN_THREAD_START * NUM_THREADS)
    print "Total runtime will be: %d seconds" % runtime
    threads = []
    try:
        for i in range(NUM_THREADS):
            t = Thread(target=threadproc)
            t.start()
            threads.append(t)
            time.sleep(DELAY_BETWEEN_THREAD_START)
        print "All threads running"
        time.sleep(TIME_AT_PEAK_QPS*60)
        print "Completed full time at peak qps, shutting down threads"
    except:
        print "Exception raised, shutting down threads"
        print TOTAL

    quitevent.set()
    time.sleep(3)
    for t in threads:
        t.join(1.0)
    print "Finished"
    for key, value in RESPONSES.items():
        print "%d response: %d" % (key, value)
    print "\nTotal requests: %d" % TOTAL
    print "Success rate: %d%%" % percentage(RESPONSES.get(200),TOTAL)
