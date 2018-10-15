from math import *
from filterpy.common import Q_discrete_white_noise
from filterpy.kalman import ExtendedKalmanFilter
from numpy import eye, array, asarray
import numpy as np
from src.planetDetector import *


constant = 1
class EKF:

    def __init__(self, path):
        dt = 0.05
        self.rk = ExtendedKalmanFilter(dim_x=2, dim_z=1)
        # radar = RadarSim(dt, pos=0., vel=100., alt=1000.)
        #self.detector = PlanetDetector('C:\\Users\\Phuc Dang\\Desktop\\Developer\\Collaborative-Sensing\\model\\cascade.xml')
        self.detector = PlanetDetector(path)
        # make an imperfect starting guess
        # rk.x = array([radar.pos - 100, radar.vel + 100, radar.alt + 1000])
        self.rk.x = array([0, .273])  # need better initial location
        self.rk.F = eye(2) + array([[0, 0],
                               [1, 0]]) * dt

        range_std = 5.  # meters
        self.rk.R = np.diag([range_std ** 2])
        self.rk.Q[0:2, 0:2] = Q_discrete_white_noise(2, dt=dt, var=0.1)
        self.rk.Q[1, 1] = 0.1
        self.rk.P *= 50


    def HJacobian_at(x):
        """ compute Jacobian of H matrix at x """

        angular_vel = x[1]
        angular_pos = x[0]
        return array([[0., (-1) * np.sin(angular_pos) * constant]])

    def hx(x):
        """ compute measurement for slant range that
        would correspond to state x.
        """

        return constant * cos(x[0])


    def run_filter(self):
        while 1:
            self.detector.runCascadeClassifier()
            z = self.detector.get_last_measurement()
            self.rk.update(array([z]), self.HJacobian_at, self.hx)
            self.rk.predict()
            print(self.rk.x)





def get_uncertainty(P):
    sum = 0
    for row in range(len(P)):
        sum += P[row][row]
    return sum / len(P)
