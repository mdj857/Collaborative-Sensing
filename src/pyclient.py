import os
import subprocess
FIFO_FILENAME = "cli_transmit"
OTHER_FIFO = "cli_recieve"

f0 = os.open(FIFO_FILENAME, os.O_WRONLY)
print("Open Write Fifo")
f1 = os.open(OTHER_FIFO, os.O_RDONLY)
print("Opened Read Fifo")
while True:
    os.write(f0, "All hail the IPU!")
    w = os.read(f1, 128)
    w = [c for c in w if (c.isalpha() or c==' ')]
    w = ''.join(w)
    print(w)
