#!/usr/bin/python

import ubx
import struct
import calendar
import os
import gobject
import logging
import sys
import time

def callback(ty, *args):
    if ty == 'RXM-RAW':
        NSV = args[0][0]["NSV"]
        ITOW = args[0][0]["ITOW"]
        #print(repr(NSV))
        for i in xrange(NSV):
            block = args[0][1 + i]
            # {'MesQI': 7, 'DOMes': -947.04443359375, 'SV': 16, 'LLI': 0, 'CPMes': 127712782.07132973, 'CNO': 38, 'PRMes': 24302931.671289716}
            print("%d %s %s %s" % (block["SV"], ITOW, block["PRMes"], block["CPMes"]))

if __name__ == "__main__":
    print("""<?xml version="1.0" encoding="UTF-8"?>
<gpx
  version="1.0"
  creator="GPSBabel - http://www.gpsbabel.org"
  xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
  xmlns="http://www.topografix.com/GPX/1/0"
  xsi:schemaLocation="http://www.topografix.com/GPX/1/0 http://www.topografix.com/GPX/1/0/gpx.xsd">""")
    t = ubx.Parser(callback, device=False)
    data = sys.stdin.read()
    t.parse(data)
    print("</gpx>")
