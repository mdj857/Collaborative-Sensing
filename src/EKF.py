from math import *
from filterpy.common import Q_discrete_white_noise
from filterpy.kalman import ExtendedKalmanFilter
from numpy import eye, array, asarray
import numpy as np
from src.planetDetector import *

constant = 1

def HJacobian_at(x):
    """ compute Jacobian of H matrix at x """

    angular_vel = x[0]
    angular_pos = x[1]
    return array([[0., (-1)*np.sin(angular_pos)*constant]])


def hx(x):
    """ compute measurement for slant range that
    would correspond to state x.
    """

    return constant * cos(x[1])


dt = 0.05
rk = ExtendedKalmanFilter(dim_x=2, dim_z=1)

#radar = RadarSim(dt, pos=0., vel=100., alt=1000.)
detector = PlanetDetector('C:\\Users\\Phuc Dang\\Desktop\\Developer\\Collaborative-Sensing\\model\\cascade.xml')

# make an imperfect starting guess
#rk.x = array([radar.pos - 100, radar.vel + 100, radar.alt + 1000])
rk.x = array([0, 0])    #need better initial location

rk.F = eye(2) + array([[0, 0],
                       [1, 0]]) * dt

range_std = 5.  # meters
rk.R = np.diag([range_std ** 2])
rk.Q[0:2, 0:2] = Q_discrete_white_noise(2, dt=dt, var=0.1)
rk.Q[1, 1] = 0.1
rk.P *= 50

xs, track = [], []
#for i in range(int(20 / dt)):
while 1:
    #z = radar.get_range()
    detector.runCascadeClassifier()
    z = detector.get_last_measurement()
    #track.append((radar.pos, radar.vel, radar.alt))

    rk.update(array([z]), HJacobian_at, hx)
    #xs.append(rk.x)
    rk.predict()
    print(rk.x)

#xs = asarray(xs)
#track = asarray(track)
#time = np.arange(0, len(xs) * dt, dt)