from filterpy.common import Q_discrete_white_noise
from filterpy.kalman import ExtendedKalmanFilter
from math import *
from numpy import eye, array, asarray
from numpy.random import randn

import numpy as np

import time
import os
import subprocess

# Number of pixels that represents distance d0
p = 185
# sampling rate for images
dt = 0.2
# length of time to analyze for
testPeriod = 20

def merge_estimates(w_sensor1, w_hat_sensor1, w_var_sensor1, w_hat_var_sensor1,
                    w_sensor2, w_hat_sensor2, w_var_sensor2, w_hat_var_sensor2):
    a_w = (w_var_sensor1 / (w_var_sensor1 + w_var_sensor2))
    merged_w = (1 - a_w) * w_sensor1 + a_w * w_sensor2

    # compute merged estimate for w_hat
    a_w_hat = (w_var_sensor1 / (w_var_sensor1 + w_var_sensor2))
    merged_w_hat = (1 - a_w_hat) * w_hat_sensor1 + a_w_hat * w_hat_sensor2

    return merged_w, merged_w_hat

def HJacobian_at(x):
    angular_vel = x[1]
    angular_pos = x[0]
    return array([[sin(angular_pos) * p, 0.]])


def get_pixel_between_sun_and_planet(x):
    return p * cos(x[0])


class EKF_class:
    def __init__(self, planetDetector, FIFO_FILENAME, OTHER_FIFO):
        # Haar classifier
        self.detector = planetDetector

        # EKF model
        self.rk = ExtendedKalmanFilter(dim_x=2, dim_z=1)
        self.initialize_rk()
        # FIFO
        self.writeFiFo = os.open(FIFO_FILENAME, os.O_WRONLY)
        self.readFiFo = os.open(OTHER_FIFO, os.O_RDONLY)

        if FIFO_FILENAME == "srv_transmit":
            self.server = True
        else:
            self.server = False
	
	#Merge values
        self.omega = self.rk.x[0]
        self.omega_hat = self.rk.x[1]
	
	#Client sensor values
        self.omega_client = self.rk.x[0]
        self.omega_hat_client = self.rk.x[1]

    def initialize_rk(self):
        # make an imperfect starting guess
        self.rk.x = array([0, 2 * np.pi / 10])

        # state transition matrix
        self.rk.F = np.asarray([[1, dt], [0, 1]])

        # measurement noise matrix
        self.rk.R = np.diag([(p ** 2)/8])

        # process noise -- basically, how close our process (i.e kinematics eqns)
        omega_noise = np.pi / 12
        self.rk.Q[0:2, 0:2] = np.array([[omega_noise, 0], [0, 0.01]])

        # covariance matrix -- set initial apriori values for "uncertainty"
        self.rk.P *= 0.1
        
        self.prevX = 0

    def run_EKF(self):

        # Init mobile simulator
        #mobile = MobileSim(0.05, np.pi / 2, 2 * np.pi / 6.55)
        while(1):
            self.detector.runCascadeClassifier()
            z = self.detector.get_last_measurement()
            self.rk.x[0] = self.rk.x[0] % (2 * np.pi)
            self.rk.predict()
            
            
            zPrime = get_pixel_between_sun_and_planet(self.rk.x)
            
            if(self.prevX == z or np.abs(zPrime - z) > 33):
              print()
            else:
              self.rk.update(array([z]), HJacobian_at, get_pixel_between_sun_and_planet)
            self.prevX = z

            # TODO: Send Values to write FiFo
            #write_msg = str(
            #    [np.round(self.rk.x[0], 3), np.round(self.rk.x[1], 3), np.round(self.rk.P[0][0], 3), np.round(self.rk.P[1][1], 3)]) + ";"
            #numBytes = os.write(self.writeFiFo, write_msg)
            # TODO: Get Values from read FiFO

            write_msg = str(
                [np.round(self.rk.x[0], 3), np.round(self.rk.x[1], 3), np.round(self.rk.P[0][0], 3), np.round(self.rk.P[1][1], 3)]) + ";"
            numBytes = os.write(self.writeFiFo, write_msg)
            otherX = os.read(self.readFiFo, 128)
            otherX = otherX.split(";")[0]
            otherX = otherX[1:-1]
            values = otherX.split(',')
            #Update sensor client values
            self.omega_client = (float(values[0]) - np.pi/2) % (2 * np.pi)
            self.omega_hat_client = float(values[1])
            
            #Compute merge values
            if self.server:
            	try:
            #Adjust the client sensor angle	
	                w_sensor2 = (float(values[0]) - np.pi/2) % (2 * np.pi)
	                w_hat_sensor2 = float(values[1])
	                w_var_sensor2 = float(values[2])
	                w_hat_var_sensor2 = float(values[3])
            #Update merge value
	                self.omega, self.omega_hat = merge_estimates(np.round(self.rk.x[0], 3), np.round(self.rk.x[1], 3),
	                  np.round(self.rk.P[0][0], 3),
	                  np.round(self.rk.P[1][1], 3), w_sensor2, w_hat_sensor2, w_var_sensor2,
	                  w_hat_var_sensor2)
            	except:
	                pass
