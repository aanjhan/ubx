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

def callback(ty, *args):
    global len
    global start
    global f
    global t
    #print("callback %s %s" % (ty, repr(args)))
    if ty == "UPD-UPLOAD" and args[0][0]["Flags"] == 1:
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
    t.send("UPD-UPLOAD", 12 + 1, {"StartAddr" : start, "DataSize" : 1, "Flags" : 0, "B0" : 0})
    start += 1
    len -= 1
    loop.run()
