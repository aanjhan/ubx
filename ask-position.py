#!/usr/bin/python

# Ask position from GPS chip. Assumes that the chip is in FixNow(tm)
# mode, talks only UBX and does not periodically report any values
# (but must be asked for the explicitely).

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
start = time.time()
TIMEOUT = 20
loop = gobject.MainLoop()
state = 0

def timeout(*args):
    print("timeout")
    loop.quit()

def poll_nav_status(*args):
    #print("poll_nav_status")
    t.sendraw(("\xff" * 8) + "\xB5\x62\x02\x40\x00\x00\x42\xC8")
    t.send("NAV-STATUS", 0, [])

def poll_nav_posllh(*args):
    #print("poll_nav_status")
    t.sendraw(("\xff" * 8) + "\xB5\x62\x02\x40\x00\x00\x42\xC8")
    t.send("NAV-POSLLH", 0, [])
    
def callback(ty, *args):
    global state
    global d
    
    print("callback %s %s" % (ty, repr(args)))
    d[ty] = args
    if ty == "NAV-STATUS":
        if d["NAV-STATUS"][0][0]["GPSfix"] != 0:
            #print("fix acquired")
            state = 1
            poll_nav_posllh()
        else:
            #print("poll scheduled")
            gobject.timeout_add(1000, poll_nav_status)
    elif state == 1 and ty == "NAV-POSLLH":
        print("%s %s %s %s %s %s" %
              (d["NAV-STATUS"][0][0]["GPSfix"],
               d["NAV-STATUS"][0][0]["TTFF"] * 10**-3,
               int(time.time() - start),
               d["NAV-POSLLH"][0][0]["LAT"] * 10**-7,
               d["NAV-POSLLH"][0][0]["LON"] * 10**-7,
               d["NAV-POSLLH"][0][0]["Hacc"] * 10**-3))
               
        #print("done")
        loop.quit()

if __name__ == "__main__":
    t = ubx.Parser(callback)
    poll_nav_status()
    gobject.timeout_add(TIMEOUT * 1000, timeout)
    loop.run()
