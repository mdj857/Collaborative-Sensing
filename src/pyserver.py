import os
import subprocess
FIFO_FILENAME = "srv_transmit"
OTHER_FIFO = "srv_recieve"

f0 = os.open(FIFO_FILENAME, os.O_WRONLY)
print("Open Write Fifo")
f1 = os.open(OTHER_FIFO, os.O_RDONLY)
print("Opened Read Fifo")
while True:
    os.write(f0, "IPU42.0")
    w = os.read(f1, 128)
    #w = [c for c in w if (c.isalpha() or c==' ')]
    #w = ''.join(w)
    print(type(w))
    print(w)
