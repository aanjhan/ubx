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
import os
import gobject
import fcntl
import sys
input_event_struct = "@LLHHi"
input_event_size = struct.calcsize(input_event_struct)

ubxfile = open(sys.argv[1], "w")
keyfile = open(sys.argv[2], "w")
itow = False
week = False

def cbUbxPacket(ty, packet):
    #print("cbUbxPacket %s %s" % (ty, repr(packet)))
    if ty == "RXM-RAW":
        global week
        global itow
        week = packet[0]["Week"]
        itow = packet[0]["ITOW"]

def cbUbxRaw(payload):
    #print("cbUbxRaw %s" % " ".join("%02x" % ord(x) for x in payload))
    ubxfile.write(payload)

def cbButtonPress(source, condition):
    print("cbButtonPress %s %s" % (source, condition))
    data = os.read(source, 512)
    events = [ data[i:i+input_event_size] for i in range(0, len(data), input_event_size) ]
    for e in events:
        timestamp, microseconds, typ, code, value = struct.unpack( input_event_struct, e )
        # We need more then just second accuracy
        timestamp = timestamp + microseconds/1000000.0
        if typ != 0x00: # ignore EV_SYN (synchronization event)
            print("event %s %s %s %s %s %s" % (week, itow, timestamp, typ, code, value))
            keyfile.write("event %s %s %s %s %s %s\n" % (week, itow, timestamp, typ, code, value))
            keyfile.flush()
            if code == 169 and value == 1:
                pass
            if code == 116 and value == 1:
                pass
    return True

if __name__ == "__main__":
    fd = os.open("/dev/input/event4", os.O_NONBLOCK | os.O_RDONLY)
    fcntl.ioctl(fd, 0x40044590, 1) # EVIOCGRAB
    gobject.io_add_watch(fd, gobject.IO_IN, cbButtonPress)
    ubx.Parser(cbUbxPacket, rawCallback = cbUbxRaw)
    gobject.MainLoop().run()
