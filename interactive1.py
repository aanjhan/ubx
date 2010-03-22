#!/usr/bin/python

# Simple repl (read-eval-print loop) in tcp port 1234 for easy
# evaluation of python code that can send/receive UBX packets.

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
