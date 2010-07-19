#!/bin/bash

function readmem() {
    i=$1
    ./upload1.py $(expr 1024 \* 1024 \* $i) 4 > a
    ret=$?
    echo "${i}M $ret $(od -t x1 a | head -n1|cut --bytes=9-)"
    if [ "$ret" != "0" ]; then
	sleep 1
	./set-periodic-logging.py off > /dev/null
	./set-nmea.py off > /dev/null
	sleep 1
    fi
}

for i in $(seq 63 64 4095); do
    readmem $i
    readmem 0
done
