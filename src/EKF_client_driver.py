from EKF_class import *
from planetDetector import *


detector = PlanetDetector('../model/cascade.xml', 1, False, False)
client = EKF_class(detector, "cli_transmit", "cli_recieve")
client.run_EKF()

