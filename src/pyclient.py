import os
import subprocess
FIFO_FILENAME = "cli_transmit"
OTHER_FIFO = "cli_recieve"

with open(FIFO_FILENAME, "a") as f:
	f.write("IPU!")
with open(OTHER_FIFO, "r") as f1:
        print("Opened Fifo")
        w = f1.read()
        print(f1)
        print(w)
