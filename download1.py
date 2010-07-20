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
