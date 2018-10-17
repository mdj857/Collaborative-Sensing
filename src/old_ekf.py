from math import *
from filterpy.common import Q_discrete_white_noise
from filterpy.kalman import ExtendedKalmanFilter
from numpy import eye, array, asarray
import numpy as np
from src.planetDetector import *

constant = 0

def HJacobian_at(x):

    angular_vel = x[1]
    angular_pos = x[0]
    return array([[0., (-1)*np.sin(angular_pos)*constant]])


def get_pixel_between_sun_and_planet(x):

    return constant * cos(x[0])


dt = 0.05
rk = ExtendedKalmanFilter(dim_x=2, dim_z=1)

#radar = RadarSim(dt, pos=0., vel=100., alt=1000.)
detector = PlanetDetector('../old_models/model_4/cascade.xml', False, False)

# make an imperfect starting guess
#rk.x = array([radar.pos - 100, radar.vel + 100, radar.alt + 1000])
rk.x = array([0, 0.237])    #need better initial location

rk.F = eye(2) + array([[0, 0],
                       [1, 0]]) * dt

range_std = 5.  # meters
bs = np.diag([range_std ** 2])
print(bs)

t = (dt ** 2) / 8
rk.R = np.diag([np.random.normal(loc=0, scale=t)])
print(rk.R)

rk.Q[0:2, 0:2] = Q_discrete_white_noise(2, dt=dt, var=0.1)
rk.Q[1, 1] = 0.1

P = [[np.random.normal(loc=0, scale=3.14/12), 0], [0, np.random.normal(loc=0, scale=0.001)]]
rk.P = np.asarray(P)

xs, track = [], []
#for i in range(int(20 / dt)):
while 1:
    #z = radar.get_range()
    detector.runCascadeClassifier()
    z = detector.get_last_measurement()
    #track.append((radar.pos, radar.vel, radar.alt))

    rk.update(array([z]), HJacobian_at, get_pixel_between_sun_and_planet)
    #xs.append(rk.x)
    rk.predict()
    print(rk.P)
    #print(rk.P)