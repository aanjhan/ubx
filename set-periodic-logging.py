#!/usr/bin/python
# Copyright (C) 2010 Timo Juhani Lindfors <timo.lindfors@iki.fi>

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.


# Set periodic reporting of various attributes on or off.

import ubx
import struct
import calendar
import os
import gobject
import logging
import sys
import socket
import time

def callback(ty, packet):
    print("callback %s" % repr([ty, packet]))

if __name__ == "__main__":
    assert len(sys.argv) == 2
    t = ubx.Parser(callback)
    if sys.argv[1] == "on":
        t.send("CFG-MSG", 3, {"Class" : ubx.CLIDPAIR["NAV-STATUS"][0] , "MsgID" : ubx.CLIDPAIR["NAV-STATUS"][1] , "Rate" : 1 })
        # Send NAV POSLLH
        t.send("CFG-MSG", 3, {"Class" : ubx.CLIDPAIR["NAV-POSLLH"][0] , "MsgID" : ubx.CLIDPAIR["NAV-POSLLH"][1] , "Rate" : 1 })
        # Send NAV VELNED
        t.send("CFG-MSG", 3, {"Class" : ubx.CLIDPAIR["NAV-VELNED"][0] , "MsgID" : ubx.CLIDPAIR["NAV-VELNED"][1] , "Rate" : 1 })
        # Send NAV POSUTM
        #t.send("CFG-MSG", 3, {"Class" : ubx.CLIDPAIR["NAV-POSUTM"][0] , "MsgID" : ubx.CLIDPAIR["NAV-POSUTM"][1] , "Rate" : 1 })
        # Send NAV TIMEUTC
        t.send("CFG-MSG", 3, {"Class" : ubx.CLIDPAIR["NAV-TIMEUTC"][0] , "MsgID" : ubx.CLIDPAIR["NAV-TIMEUTC"][1] , "Rate" : 1 })
        # Send NAV DOP
        t.send("CFG-MSG", 3, {"Class" : ubx.CLIDPAIR["NAV-DOP"][0] , "MsgID" : ubx.CLIDPAIR["NAV-DOP"][1] , "Rate" : 1 })
        # Send NAV SVINFO
        t.send("CFG-MSG", 3, {"Class" : ubx.CLIDPAIR["NAV-SVINFO"][0] , "MsgID" : ubx.CLIDPAIR["NAV-SVINFO"][1] , "Rate" : 5 })
    else:
        t.send("CFG-MSG", 3, {"Class" : ubx.CLIDPAIR["NAV-STATUS"][0] , "MsgID" : ubx.CLIDPAIR["NAV-STATUS"][1] , "Rate" : 0 })
        t.send("CFG-MSG", 3, {"Class" : ubx.CLIDPAIR["NAV-POSLLH"][0] , "MsgID" : ubx.CLIDPAIR["NAV-POSLLH"][1] , "Rate" : 0 })
        t.send("CFG-MSG", 3, {"Class" : ubx.CLIDPAIR["NAV-VELNED"][0] , "MsgID" : ubx.CLIDPAIR["NAV-VELNED"][1] , "Rate" : 0 })
        t.send("CFG-MSG", 3, {"Class" : ubx.CLIDPAIR["NAV-TIMEUTC"][0] , "MsgID" : ubx.CLIDPAIR["NAV-TIMEUTC"][1] , "Rate" : 0 })
        t.send("CFG-MSG", 3, {"Class" : ubx.CLIDPAIR["NAV-DOP"][0] , "MsgID" : ubx.CLIDPAIR["NAV-DOP"][1] , "Rate" : 0 })
        t.send("CFG-MSG", 3, {"Class" : ubx.CLIDPAIR["NAV-SVINFO"][0] , "MsgID" : ubx.CLIDPAIR["NAV-SVINFO"][1] , "Rate" : 0 })
