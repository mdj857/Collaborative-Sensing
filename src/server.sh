#!/bin/sh
rm srv_*
killall -9 server
./server 127.0.0.1 128 &
python display.py &
