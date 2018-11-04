import os
import subprocess
FIFO_FILENAME = "srv_transmit"

with open(FIFO_FILENAME, "a") as f:
	f.write("IPU!") 
