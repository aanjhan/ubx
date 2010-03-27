#!/usr/bin/python

import ubx
import struct
import calendar
import os
import gobject
import logging
import sys
import time

loop = gobject.MainLoop()

def callback(ty, *args):
    print("callback %s %s" % (ty, repr(args)))
       
if __name__ == "__main__":
    t = ubx.Parser(callback, device=False)
    data = sys.stdin.read()
    t.parse(data)
    loop.run()
