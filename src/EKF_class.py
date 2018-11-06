from filterpy.common import Q_discrete_white_noise
from filterpy.kalman import ExtendedKalmanFilter
from math import *
from numpy import eye, array, asarray
from numpy.random import randn

import numpy as np

import time
import os
import subprocess


class MobileSim(object):
    def __init__(self, delta, omega, omega_hat):
        self.delta = delta
        self.omega = omega
        self.omega_hat = omega_hat
        self.i = 0

    def get_x_pos(self):
        self.omega_hat = self.omega_hat + .00001 * randn()

        # if(self.omega < 50):
        self.omega = (self.omega + self.omega_hat * self.delta)
        # else:
        #	self.omega = self.omega - self.omega_hat*self.delta
        # self.omega = self.omega % (2 * np.pi)
        self.i = (self.i + 1) % 115
        return camData[self.i]
    # err = 0.001*randn()
    # x_pos =  p * cos(self.omega) * sin(alpha)
    # return x_pos + err


camData = [110,
           121,
           126,
           130,
           139,
           148,
           154,
           158,
           163,
           162,
           162,
           157,
           151,
           146,
           137,
           131,
           116,
           103,
           89,
           58,
           24,
           -1,
           -26,
           -26,
           -26,
           -26,
           -26,
           -54,
           -155,
           -166,
           -179,
           -183,
           -183,
           -183,
           -180,
           -174,
           -168,
           -161,
           -161,
           -161,
           -161,
           -161,
           -161,
           -161,
           -161,
           -161,
           -161,
           -161,
           -161,
           -161,
           -161,
           -161,
           -161,
           -161,
           -161,
           -161,
           -151,
           105,
           117,
           125,
           128,
           137,
           145,
           151,
           159,
           159,
           162,
           161,
           160,
           153,
           147,
           138,
           133,
           117,
           104,
           60,
           24,
           -1,
           -1,
           -1,
           -1,
           -1,
           -1,
           -27,
           -156,
           -167,
           -175,
           -179,
           -183,
           -183,
           -181,
           -180,
           -174,
           -169,
           -161,
           -161,
           -161,
           -161,
           -161,
           -151,
           -151,
           -151,
           -151,
           -151,
           -151,
           -151,
           -151,
           -151,
           -151,
           -151,
           -151,
           -151,
           -151,
           -81,
           108]

def merge_estimates(w_sensor1, w_hat_sensor1, w_var_sensor1, w_hat_var_sensor1,
                    w_sensor2, w_hat_sensor2, w_var_sensor2, w_hat_var_sensor2):
    # compute merged estimate for w
    a_w = (w_var_sensor1 / (w_var_sensor1 + w_var_sensor2))
    merged_w = (1 - a_w) * w_sensor1 + a_w * w_sensor2

    # compute merged estimate for w_hat
    a_w_hat = (w_var_sensor1 / (w_var_sensor1 + w_var_sensor2))
    merged_w_hat = (1 - a_w_hat) * w_hat_sensor1 + a_w_hat * w_hat_sensor2

    return merged_w, merged_w_hat



def HJacobian_at_test(x):
    """ compute Jacobian of H matrix at x """

    horiz_dist = x[0]
    altitude = x[2]
    denom = sqrt(horiz_dist ** 2 + altitude ** 2)
    return array([[horiz_dist / denom, 0., altitude / denom]])


def hx(x):
    """ compute measurement for slant range that
    would correspond to state x.
    """

    return (x[0] ** 2 + x[2] ** 2) ** 0.5


def HJacobian_at(x, p):
    angular_vel = x[1]
    angular_pos = x[0]
    return array([[(-1.0) * sin(angular_pos) * p, 0.]])


def get_pixel_between_sun_and_planet(x, p):
    # print(np.abs(p * cos(x[0])))
    return p * cos(x[0])


class EKF_class:
    def __init__(self, planetDetector, FIFO_FILENAME, OTHER_FIFO):
        # Haar classifier
        self.detector = planetDetector
        # Number of pixels that represents distance d0
        self.p = 185
        # physical distance between Earth and Sun in a callibrated image
        self.d0 = 10.
        # angle of elevation from camera to plane of mobile
        self.alpha = np.pi/2
        # sampling rate for images
        self.dt = 0.05
        # length of time to analyze for
        self.testPeriod = 20
        # EKF model
        self.rk = ExtendedKalmanFilter(dim_x=2, dim_z=1)
        self.initializeMatrix()
        # FIFO
        self.writeFIFO = os.open(FIFO_FILENAME, os.O_WRONLY)
        self.readFIFO = os.open(OTHER_FIFO, os.O_RDONLY)

    def initialize_rk(self):
        # make an imperfect starting guess
        self.rk.x = array([np.pi / 2, 2 * np.pi / 6.55])

        # state transition matrix
        self.rk.F = np.asarray([[1, self.dt], [0, 1]])

        # measurement noise matrix
        # self.rk.R = np.diag([((d0/p) ** 2) / 8])
        self.rk.R = np.diag([50])

        # process noise -- basically, how close our process (i.e kinematics eqns)
        omega_noise = np.random.normal(0, np.pi / 2)
        self.rk.Q[0:2, 0:2] = np.array([[omega_noise, 0], [0, 0.01]])

        # covariance matrix -- set initial apriori values for "uncertainty"
        self.rk.P *= 0.01

    def run_EKF(self):

        # Init mobile simulator
        mobile = MobileSim(0.05, np.pi / 2, 2 * np.pi / 6.55)

        mobOmega, modOmega, mobOmegaHat, modOmegaHat = [], [], [], []
        deltaOmega, deltaOmegaHat = [], []
        uncertainty, uncertainty2 = [], []

        prevX = 0
        prevOmega = 0
        prevOmegaHat = 0

        for a in range(int(self.testPeriod / self.dt)):
            # detector.runCascadeClassifier()
            z = mobile.get_x_pos()  # SIMULATION
            # z = radar.get_range()
            # rk.x[0] = rk.x[0] % (2 * np.pi)
            # rk.update(array([z]), HJacobian_at_test, hx)
            self.rk.update(array([z]), HJacobian_at, get_pixel_between_sun_and_planet)
            self.rk.predict()

            # mobOmega.append(int(np.degrees(radar.pos)))
            mobOmega.append(mobile.omega)
            modOmega.append(self.rk.x[0])

            scale = 1 / (1.2 * HJacobian_at(self.rk.x)[0][0])

            # deltaOmega.append(mobile.omega - rk.x[0])
            deltaOmega.append(0.2 * scale * self.rk.y)

            # mobOmegaHat.append(int(np.degrees(radar.vel)))
            mobOmegaHat.append(mobile.omega_hat)
            modOmegaHat.append(self.rk.x[1])

            # deltaOmegaHat.append(mobile.omega_hat - rk.x[1])
            deltaOmegaHat.append((self.rk.x[0] - prevOmega) * 1.2 * scale / self.rk.y)

            uncertainty.append(self.rk.P[0, 0])
            # uncertainty2.append(rk.P[1,1])
            uncertainty2.append((self.rk.x[1] - prevOmegaHat) * 1.2 * scale / self.rk.y)

            # TODO: Send Values to write FiFo
            write_msg = str(
                [np.round(self.rk.x[0], 3), np.round(self.rk.x[1], 3), np.round(self.rk.P[0][0], 3), np.round(self.rk.P[1][1], 3)]) + ";"
            numBytes = os.write(self.writeFiFo, write_msg)
            # TODO: Get Values from read FiFO

            write_msg = str(
                [np.round(self.rk.x[0], 3), np.round(self.rk.x[1], 3), np.round(self.rk.P[0][0], 3), np.round(self.rk.P[1][1], 3)]) + ";"
            numBytes = os.write(self.writeFiFo, write_msg)
            otherX = os.read(self.readFiFo, 128)
            otherX = otherX.split(";")[0]
            otherX = otherX[1:-1]
            values = otherX.split(',')
            try:
                w_sensor2 = float(values[0])
                w_hat_sensor2 = float(values[1])
                w_var_sensor2 = float(values[2])
                w_hat_var_sensor2 = float(values[3])
                w_merge, w_hat_merge = merge_estimates(np.round(self.rk.x[0], 3), np.round(self.rk.x[1], 3),
                                                       np.round(self.rk.P[0][0], 3),
                                                       np.round(self.rk.P[1][1], 3), w_sensor2, w_hat_sensor2, w_var_sensor2,
                                                       w_hat_var_sensor2)

            # print(np.round(w_merge,3), np.round(w_hat_merge,3))
            except:
                pass
            # prevX = z
            # if(prevX != z):
            # print(i)
            # rk.predict()
            prevX = z
            prevOmega = self.rk.x[0]
            prevOmegaHat = self.rk.x[1]

        import matplotlib.pyplot as plt

        t = np.arange(0, self.testPeriod, self.dt)
        plt.subplot(3, 2, 1)
        plt.ylabel('Omega')
        plt.plot(t, mobOmega, 'r--', t, modOmega, 'b-')
        plt.subplot(3, 2, 2)
        plt.ylabel('Actual - Expected: Omega')
        plt.plot(t, deltaOmega, 'g.')
        plt.subplot(3, 2, 3)
        plt.ylabel('Omega Hat')
        plt.plot(t, mobOmegaHat, 'r--', t, modOmegaHat, 'b-')
        plt.subplot(3, 2, 4)
        plt.ylabel('Actual - Expected: Omega Hat')
        plt.plot(t, deltaOmegaHat, 'g.')

        plt.subplot(3, 2, 5)
        plt.ylabel('Uncertainty Omega')
        plt.plot(t, uncertainty, 'b-')
        plt.subplot(3, 2, 6)
        plt.ylabel('Uncertainty Omega^')
        plt.plot(t, uncertainty2, 'b-')
        plt.show()






