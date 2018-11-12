from EKF_class import *
from planetDetector import *

server = EKF_class(0, "srv_transmit", "srv_recieve")
server.run_EKF()


