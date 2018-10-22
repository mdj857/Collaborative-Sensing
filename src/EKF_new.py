from math import *
from filterpy.common import Q_discrete_white_noise
from filterpy.kalman import ExtendedKalmanFilter
from numpy import eye, array, asarray
import numpy as np
import time
# from src.planetDetector import *
PI = 3.14159265358979323846264979

#Physical distance between Earth and Sun in a callibrated image
d0 = 10

# angle of elevation from camera to plane of mobile
alpha = PI/2

# sampling rate for images
dt = .05

def f1(x):
	return x ** 2

def HJacobian_at(x):
	angular_vel = x[1]
	angular_pos = x[0]
	return array([[0., (-1)*np.sin(angular_pos)*d0]])

def get_pixel_between_sun_and_planet(x):
	return d0 * cos(x[0]) * sin(alpha)

rk = ExtendedKalmanFilter(dim_x=2, dim_z=1)

#detector = PlanetDetector('../old_models/model_4/cascade.xml', False, False)

# make an imperfect starting guess -- make 
rk.x = array([PI/2, 2*PI/22])    

# state transition matrix 
rk.F = np.asarray([[1, dt], [0, 1]])

# measurement noise matrix 
#---
rk.R = np.diag([np.random.normal(loc=0, scale=((dt ** 2) / 8))])
#---rk.R = np.asarray([[0]])
print("Measurement noise matrix: " , (rk.R))

# process noise -- basically, how close our process (i.e kinematics eqns) model true system behavior
#--
rk.Q = Q_discrete_white_noise(dim=2, dt=dt, var = .1)
#--rk.Q = 0

# covariance matrix -- set initial apriori values for "uncertainty"
rk.P = np.asarray([[0.1, 0.1], [0.1, 0.1]])

i = 0
di = 1
while 1:
	time.sleep(0.05)
	#detector.runCascadeClassifier()
	#z = detector.get_last_measurement()
	i += di
	#if(i == 10):
	#	di = -1
	#if(i == -10):
	#	di = 1
	z = i

	rk.update(z, HJacobian_at, get_pixel_between_sun_and_planet)
	rk.predict()
	out_x = rk.x
	#out_x[0] = (out_x[0])  * 180/PI
	print str(i) + ": \n\t" + str(out_x[0] * 180/PI) + '\n\t' + str(out_x[1] * 180/PI)

