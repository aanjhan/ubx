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

f = open("upload.dat", "w+")
loop = gobject.MainLoop()

def callback(ty, *args):
    global f
    global t
    print("callback %s %s" % (ty, repr(args)))
    if ty == "UPD-UPLOAD" and args[0][0]["Flags"] == 1:
        for i in xrange(16):
            f.write(chr(args[0][0]["B%s" % i]))
        f.flush()
        time.sleep(0.1)
        t.send("UPD-UPLOAD", 12 +16, {"StartAddr" : args[0][0]["StartAddr"] + 16, "DataSize" : 16, "Flags" : 0, "B0" : 0, "B1" : 0, "B2" : 0, "B3" : 0, "B4" : 0, "B5" : 0, "B6" : 0, "B7" : 0, "B8" : 0, "B9" : 0, "B10" : 0, "B11" : 0, "B12" : 0, "B13" : 0, "B14" : 0, "B15" : 0})
        
if __name__ == "__main__":
    t = ubx.Parser(callback)
    t.send("UPD-UPLOAD", 12 + 16, {"StartAddr" : 0, "DataSize" : 16, "Flags" : 0, "B0" : 0, "B1" : 0, "B2" : 0, "B3" : 0, "B4" : 0, "B5" : 0, "B6" : 0, "B7" : 0, "B8" : 0, "B9" : 0, "B10" : 0, "B11" : 0, "B12" : 0, "B13" : 0, "B14" : 0, "B15" : 0})
    loop.run()
