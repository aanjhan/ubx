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

loop = gobject.MainLoop()
    
def callback(ty, *args):
    print("callback %s %s" % (ty, repr(args)))
    if ty == "MON-EXCEPT":
        for v in ["code", "num", "ur0", "ur1", "ur2", "ur3", "ur4", "ur5", "ur6", "ur7", "ur8", "ur9", "ur10", "ur11", "ur12", "usp", "ulr", "fr8", "fr9", "fr10", "fr11", "fr12", "fsp", "flr", "fspsr", "isp", "ilr", "ispsr", "cpsr", "pc", "us0", "us1", "us2", "us3", "us4", "us5", "us6", "us7", "us8", "us9", "us10", "us11", "us12", "us13", "us14", "us15", "res", "is0", "is1", "is2", "is3", "is4", "is5", "is6", "is7", "is8", "is9", "is10", "is11", "is12", "is13", "is14", "is15", "fs0", "fs1", "fs2", "fs3", "fs4", "fs5", "fs6", "fs7", "fs8", "fs9", "fs10", "fs11", "fs12", "fs13", "fs14", "fs15"]:
            print("%-8s 0x%08x" % (v, args[0][0][v]))
        loop.quit()

if __name__ == "__main__":
    t = ubx.Parser(callback)
    t.send("MON-EXCEPT", 0, [])
    loop.run()
