from math import *
from filterpy.common import Q_discrete_white_noise
from filterpy.kalman import ExtendedKalmanFilter
from numpy import eye, array, asarray
from numpy.random import randn
import numpy as np
import time
# from src.planetDetector import *


class MobileSim(object):
	def __init__(self, delta, omega, omega_hat):
		self.delta = delta
		self.omega = omega
		self.omega_hat = omega_hat
	
	def get_x_pos(self):
		self.omega_hat = self.omega_hat + .001*randn()
		self.omega = self.omega + self.omega_hat*self.delta
		self.omega = self.omega % (2 * np.pi)
		
		err = 0.05*randn()
		x_pos = d0 / p * cos(self.omega) * sin(alpha)
		return x_pos + err
		
		

def HJacobian_at(x):
	angular_vel = x[1]
	angular_pos = x[0]
	return array([[(-1)* sin(alpha) * sin(angular_pos)*d0/p, 0.]])

def get_pixel_between_sun_and_planet(x):
	return d0/p * cos(x[0]) * sin(alpha)

#Number of pixels that represents distance d0
p = 200

# physical distance between Earth and Sun in a callibrated image
d0 = 10

# angle of elevation from camera to plane of mobile
alpha = np.pi/2

# sampling rate for images
dt = .05

#Init mobile simulator
mobile = MobileSim(dt, 0., 2*np.pi/6.55)

#Init extended kalman filter
rk = ExtendedKalmanFilter(dim_x=2, dim_z=1)

#detector = PlanetDetector('../old_models/model_4/cascade.xml', False, False)

# make an imperfect starting guess
rk.x = array([0, np.pi/11])  

# state transition matrix 
rk.F = np.asarray([[1, dt], [0, 1]])

# measurement noise matrix
rk.R = np.diag([np.random.normal(loc=0, scale=((dt ** 2) / 8))])

# process noise -- basically, how close our process (i.e kinematics eqns) 
# model true system behavior
#--
rk.Q = Q_discrete_white_noise(dim=2, dt=dt, var = .1)
rk.Q = np.diag(np.diag(rk.Q)) # Zero out non-diagonal elements
print("Process noise matrix" , rk.Q)
#--rk.Q = 0

# covariance matrix -- set initial apriori values for "uncertainty"
#--rk.P = np.asarray([[0.1, 0], [0, 0.1]])
#--
rk.P *= 50

for i in range(int(20/dt)):
	time.sleep(1)
	z = mobile.get_x_pos()
	print(str(i*0.05)+"\tseconds: ")
	print("\tOmega:   "
		+str(mobile.omega * 180 / np.pi)
		+"\tdegrees\n\tOmega^: "
		+str(mobile.omega_hat * 180 / np.pi)
		+"\tdegrees per second")
	rk.update(array([z]), HJacobian_at, get_pixel_between_sun_and_planet)
	rk.predict()

