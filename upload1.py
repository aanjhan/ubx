#!/usr/bin/python

# Upload firmware of GPS chip to file.

import ubx
import struct
import calendar
import os
import gobject
import logging
import sys
import socket
import time

d = {}

loop = gobject.MainLoop()
start = int(sys.argv[1])
len = int(sys.argv[2])
refresh_time = time.time()
retval = 0

def timeout_occured(*args):
    global retval
    if time.time() - refresh_time > 2:
        retval = 1
        loop.quit()
    return True

def callback(ty, *args):
    global len
    global start
    global f
    global t
    #print("callback %s %s" % (ty, repr(args)))
    if ty == "UPD-UPLOAD" and args[0][0]["Flags"] == 1:
        refresh_time = time.time()
        sys.stdout.write(chr(args[0][0]["B0"]))
        time.sleep(0.1)
        if len <= 0:
            loop.quit()
        else:
            t.send("UPD-UPLOAD", 12 + 1, {"StartAddr" : start, "DataSize" : 1, "Flags" : 0, "B0" : 0})
            start += 1
            len -= 1
        
if __name__ == "__main__":
    t = ubx.Parser(callback)
    gobject.timeout_add(2000, timeout_occured)
    t.send("UPD-UPLOAD", 12 + 1, {"StartAddr" : start, "DataSize" : 1, "Flags" : 0, "B0" : 0})
    start += 1
    len -= 1
    loop.run()
    sys.exit(retval)

