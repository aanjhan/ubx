#!/usr/bin/python


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
val = ord(sys.stdin.read()[0])

def callback(ty, *args):
    print("callback %s %s" % (ty, repr(args)))
    if ty == "UPD-DOWNL":
        assert args[0][0]["Flags"] == 1
        loop.quit()
        
if __name__ == "__main__":
    t = ubx.Parser(callback)
    t.send("UPD-DOWNL", 8 + 1, {"StartAddr" : start, "Flags" : 0, "B0" : val})
    loop.run()
