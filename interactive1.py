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

class ControlInstance():
    def __init__(self, conn, t):
        self.t = t
        gobject.io_add_watch(conn, gobject.IO_IN, self.handler)
    def handler(self, conn, *args):
        line = conn.recv(4096)
        if not line:
            print("connection closed")
            return False
        print("read %s" % repr(line))
        try:
            print(eval(line))
        except Exception, e:
            print("Exception %s" % e)
        return True

class Control():
    def __init__(self, t):
        self.t = t
        sock = socket.socket()
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.bind(("localhost", 1234))
        sock.listen(1)
        print("Listening...")
        gobject.io_add_watch(sock, gobject.IO_IN, self.listener)
    def listener(self, sock, *args):
        conn, addr = sock.accept()
        print "Connected"
        c = ControlInstance(conn, self.t)
        return True

def callback(ty, packet):
    print("callback %s" % repr([ty, packet]))

if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    t = ubx.Parser(callback)
    #t.initializeDevice()
    c = Control(t)
    gobject.MainLoop().run()
