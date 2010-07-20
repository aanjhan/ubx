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

# Enable or disable FixNow(tm) power saving mode.

import ubx
import struct
import calendar
import os
import gobject
import logging
import sys
import socket
import time

def callback(*args):
    print("callback %s" % args)

if __name__ == "__main__":
    assert len(sys.argv) == 2
    t = ubx.Parser(callback)
    if sys.argv[1] == "on":
        t.send("CFG-RXM", 2, {'gps_mode': 3, 'lp_mode': 1})
        t.send("CFG-FXN", 36, {'t_acq': 120000, 't_reacq': 120000, 't_reacq_off': 600000, 't_on': 36000, 'flags': 18, 't_off': 1800000, 'base_tow': 0, 't_acq_off': 600000})
    else:
        t.sendraw(("\xff" * 8) + "\xB5\x62\x02\x40\x00\x00\x42\xC8")
        t.send("CFG-RXM", 2, {'gps_mode': 3, 'lp_mode': 0})

