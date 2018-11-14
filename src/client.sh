#!/bin/sh
rm cli_*
./client 127.0.0.1 57681 128 &
python EKF_client_driver.py &

