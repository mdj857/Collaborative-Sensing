from EKF_class import *
from planetDetector import *


client = EKF_class(0, "cli_transmit", "cli_recieve")
client.run_EKF()


