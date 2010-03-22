#!/usr/bin/python

# Enable or disable the use of NMEA.

import ubx
import struct
import calendar
import os
import gobject
import logging
import sys
import socket
import time

loop = gobject.MainLoop()

def callback(ty, packet):
    print("callback %s" % repr([ty, packet]))
    if ty == "CFG-PRT":
        if sys.argv[1] == "on":
            # NMEA and UBX
            packet[0]["In_proto_mask"] = 1 + 2
            packet[0]["Out_proto_mask"] = 1 + 2
        else:
            # only UBX
            packet[0]["In_proto_mask"] = 1
            packet[0]["Out_proto_mask"] = 1
        t.send("CFG-PRT", 20, packet)
    elif ty == "ACK-ACK":
        loop.quit()
    return True

assert len(sys.argv) == 2
t = ubx.Parser(callback)
t.send("CFG-PRT", 0, [])
loop.run()
