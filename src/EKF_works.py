from filterpy.common import Q_discrete_white_noise
from filterpy.kalman import ExtendedKalmanFilter
from math import *
from planetDetector import *
from numpy import eye, array, asarray
from numpy.random import randn

import numpy as np

import time


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
	#return math.acos(x[0]) * p / d0 / sin(alpha)

#Number of pixels that represents distance d0
p = 200

# physical distance between Earth and Sun in a callibrated image
d0 = 10

# angle of elevation from camera to plane of mobile
alpha = np.pi/2

# sampling rate for images
dt = 0.25

#length of time to analyze for
testPeriod = 50

#Init mobile simulator
mobile = MobileSim(dt, 0., 2*np.pi/6.55)

#Init extended kalman filter
rk = ExtendedKalmanFilter(dim_x=2, dim_z=1)

#Haar Cascade Planet Detector
detector = PlanetDetector('../old_models/model_4/cascade.xml', False, False)

# make an imperfect starting guess
rk.x = array([0, 2*np.pi/6.55])  

# state transition matrix 
rk.F = np.asarray([[1, dt], [0, 1]])

# measurement noise matrix
#rk.R = (dt ** 2) / 8
rk.R = np.diag([(2 * np.pi / 6.55) ** 2])
#rk.R = np.diag([(dt ** 2) / 8])

# process noise -- basically, how close our process (i.e kinematics eqns) 
# model true system behavior
#--
rk.Q = Q_discrete_white_noise(dim=2, dt=dt, var = .1)
rk.Q = np.diag(np.diag(rk.Q)) # Zero out non-diagonal elements

print("Process noise matrix" , rk.Q)
#--rk.Q = 0

# covariance matrix -- set initial apriori values for "uncertainty"
#--
rk.P *= 0.01

mobOmega, modOmega, mobOmegaHat , modOmegaHat = [],[],[],[]
deltaOmega, deltaOmegaHat = [],[]

i = 0
k = 0
while(k != 27):
	
	#Function will run until spacebar is pressed. At this point, all samples will be
	#displayed with matplotlib.pyplot to show the measurement of the ekf vs the ex-
	#pected movement of a constantly revolving Earth.

	k = (cv2.waitKey(30) & 0xff)

#for i in range(int(testPeriod/dt)):
	#time.sleep(1)
	time.sleep(0.05)
	i += 0.05
	detector.runCascadeClassifier()
	z = detector.get_last_measurement() #EVALUATION
	#z = mobile.get_x_pos() #SIMULATION
	rk.x[0] = rk.x[0] % (2 * np.pi)
		#print(str(i*0.05)+"\tseconds: ")
		#print("\tMobile Omega:   "
		#	+str(int(mobile.omega * 180 / np.pi))
		#	+"\tdegrees\n\tModel Omega: "
		#	+str(int(rk.x[0] * 180 / np.pi))
		#	+"\tdegrees\n\tMobile Omega^: "
		#	+str(int(mobile.omega_hat * 180 / np.pi))
		#	+"\tdegrees per second\n\tModel Omega^: "
		#	+str(int(rk.x[1] * 180 / np.pi))
		#	+"\tdegrees per second")
	mobOmega.append(int(np.degrees(mobile.omega)))
	modOmega.append(int(np.degrees(rk.x[0])))
	
	deltaOmega.append(int(np.degrees(mobile.omega - rk.x[0])))
	
	mobOmegaHat.append(int(np.degrees(mobile.omega_hat)))
	modOmegaHat.append(int(np.degrees(rk.x[1])))
	
	deltaOmegaHat.append(int(np.degrees(mobile.omega_hat - rk.x[1])))
	
	rk.update(array([z]), HJacobian_at, get_pixel_between_sun_and_planet)
	rk.predict()
	

import matplotlib.pyplot as plt
"""
#t = np.arange(0, testPeriod, dt)
t = np.arange(0, i, dt)
plt.subplot(2, 2, 1)
plt.plot(t, mobOmega, 'r--', t, modOmega, 'bo')
plt.subplot(2, 2, 2)
plt.plot(t, deltaOmega, 'g*')
plt.subplot(2, 2, 3)
plt.plot(t, mobOmegaHat, 'r--', t, modOmegaHat, 'bo')
plt.subplot(2, 2, 4)
plt.plot(t, deltaOmegaHat, 'g*')
plt.show()
"""
