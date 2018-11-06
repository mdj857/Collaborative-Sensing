from src.EKF_class import *
from src.planetDetector import *

temp = EKF_class(0, "srv_transmit", "srv_recieve")
temp.run_EKF()

