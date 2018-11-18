#!/bin/sh
rm cli_*
killall python server client
./client 10.0.0.1 57681 128 &
python EKF_client_driver.py &

