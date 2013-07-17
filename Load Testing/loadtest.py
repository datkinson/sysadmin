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
RESPONSE_200 = 0
RESPONSE_301 = 0
RESPONSE_400 = 0
RESPONSE_401 = 0
RESPONSE_403 = 0
RESPONSE_404 = 0
RESPONSE_500 = 0

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
            TIME_AT_PEAK_QPS = int(a)
    elif o == '-d':
        if a.isdigit():
            DELAY_BETWEEN_THREAD_START = int(a)
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
    global RESPONSE_200
    global RESPONSE_301
    global RESPONSE_400
    global RESPONSE_401
    global RESPONSE_403
    global RESPONSE_404
    global RESPONSE_500

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
            if resp.status == 200:
                RESPONSE_200 += 1
            if resp.status == 301:
                RESPONSE_301 += 1
            if resp.status == 400:
                RESPONSE_400 += 1
            if resp.status == 401:
                RESPONSE_401 += 1
            if resp.status == 403:
                RESPONSE_403 += 1
            if resp.status == 404:
                RESPONSE_404 += 1
            if resp.status == 500:
                RESPONSE_500 += 1
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
    print "200 response: %d" % RESPONSE_200
    print "301 response: %d" % RESPONSE_301
    print "400 response: %d" % RESPONSE_400
    print "401 response: %d" % RESPONSE_401
    print "403 response: %d" % RESPONSE_403
    print "404 response: %d" % RESPONSE_404
    print "500 response: %d" % RESPONSE_500
    print "\nTotal requests: %d" % TOTAL
    print "Success rate: %d%%" % percentage(RESPONSE_200,TOTAL)
