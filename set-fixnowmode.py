#!/usr/bin/python

# Enable or disable FixNow(tm) power saving mode.

import ubx
import struct
import calendar
import os
import gobject
import logging
import sys
import socket
import time

def callback(*args):
    print("callback %s" % args)

if __name__ == "__main__":
    assert len(sys.argv) == 2
    t = ubx.Parser(callback)
    if sys.argv[1] == "on":
        t.send("CFG-RXM", 2, {'gps_mode': 3, 'lp_mode': 1})
        t.send("CFG-FXN", 36, {'t_acq': 120000, 't_reacq': 120000, 't_reacq_off': 600000, 't_on': 36000, 'flags': 18, 't_off': 1800000, 'base_tow': 0, 't_acq_off': 600000})
    else:
        t.sendraw(("\xff" * 8) + "\xB5\x62\x02\x40\x00\x00\x42\xC8")
        t.send("CFG-RXM", 2, {'gps_mode': 3, 'lp_mode': 0})

