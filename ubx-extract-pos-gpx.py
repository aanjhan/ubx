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
    if ty == 'NAV-POSLLH':
        lat = float(args[0][0]["LAT"])/10000000
        lon = float(args[0][0]["LON"])/10000000
        print("<wpt lat=\"%s\" lon=\"%s\"></wpt>" % (lat, lon))

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
