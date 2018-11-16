from filterpy.common import Q_discrete_white_noise
from filterpy.kalman import ExtendedKalmanFilter
from math import *
from numpy import eye, array, asarray
from numpy.random import randn

import numpy as np

import time

camData = [163,
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
	-26,
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
	-161,
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
	160]

i=-1

class MobileSim(object):
	def __init__(self, delta, omega, omega_hat):
		self.delta = delta
		self.omega = omega
		self.omega_hat = omega_hat
		self.i = 0

	def get_x_pos(self):
		
		self.omega_hat = self.omega_hat + .01*randn()
		
		#if(self.omega < 50):
		self.omega = (self.omega + self.omega_hat*self.delta)
		#else:
		#	self.omega = self.omega - self.omega_hat*self.delta
		self.omega = self.omega % (2 * np.pi)
		self.i = (self.i + 1)%len(camData)
		return camData[self.i] +10
		#err = 0.001*randn()
		#x_pos =  p * cos(self.omega) * sin(alpha)
		#return x_pos + err

def omegaDiff(sim, exp):
	'''
	if((-1 * np.pi) < np.abs(sim - exp)):
		return sim-exp
	if((-2*np.pi) < sim-exp and sim-exp < np.pi):
		return (sim + (2*np.pi)) - exp
	if((-1*np.pi) < sim-exp and sim-exp < (2*np.pi)):
		return np.abs(sim - (2*np.pi) - exp)
	return -100000
	'''
	diff = (sim - exp + np.pi) % (2*np.pi) - np.pi
	if(diff < (-1 * np.pi)):
	  return diff + (2*np.pi)
	else:
	  return diff

def HJacobian_at(x):
	angular_vel = x[1]
	angular_pos = x[0]
	return array([[(-1.0)* sin(angular_pos)*p, 0.]])

def get_pixel_between_sun_and_planet(x):
	#print(np.abs(p * cos(x[0])))
	return p * cos(x[0])

#Number of pixels that represents distance d0
p = 175

# sampling rate for images
dt = 0.2

#length of time to analyze for
testPeriod = 60

#Init mobile simulator
mobile = MobileSim(dt,0, 2*np.pi/10)
#radar = RadarSim(dt, pos=0., vel=100., alt=1000.)

#Init extended kalman filter
rk = ExtendedKalmanFilter(dim_x=2, dim_z=1)

# make an imperfect starting guess
rk.x = array([-55, 0])
#rk.x = array([radar.pos-100, radar.vel+100, radar.alt+1000])

# state transition matrix
rk.F = np.asarray([[1, dt], [0, 1]])
#rk.F = eye(3) + array([[0, 1, 0],
#                       [0, 0, 0],
#                       [0, 0, 0]]) * dt

# measurement noise matrix
#rk.R = np.diag([0])
rk.R = np.diag([(p ** 2)/8])

# process noise -- basically, how close our process (i.e kinematics eqns)
# model true system behavior
omega_noise = np.pi/8
rk.Q[0:2, 0:2] = np.array([[omega_noise,0],[0,0.01]])

print("Process noise matrix" , rk.Q)
#--rk.Q = 0

# covariance matrix -- set initial apriori values for "uncertainty"
#--
rk.P *= 0.1
#rk.P *= 0
#rk.P *= 2

mobOmega, modOmega, mobOmegaHat , modOmegaHat = [],[],[],[]
measureDist, simDist, ekfDist = [],[],[]
uncertainty,uncertainty2 = [],[]

prevX = 0
prevOmega = 0

prevOmegaHat = 0
for a in range(int(testPeriod/dt)):
	#detector.runCascadeClassifier()
	z = mobile.get_x_pos() #SIMULATION
	#z = radar.get_range()
	#rk.x[0] = rk.x[0] % (2 * np.pi)
	#rk.update(array([z]), HJacobian_at_test, hx)
	rk.predict()
	
	rk.x[0] = rk.x[0] % (2*np.pi)
	
	#mobOmega.append(int(np.degrees(radar.pos)))
	#mobOmega.append(z)
	mobOmega.append((mobile.omega % (2*np.pi)) )
	#modOmega.append(get_pixel_between_sun_and_planet(rk.x))
	modOmega.append((rk.x[0] % (2*np.pi)) )
	
	#deltaOmega.append(mobile.omega - rk.x[0])
	simDist.append(get_pixel_between_sun_and_planet([mobile.omega]))
	
	measureDist.append(z)

	#mobOmegaHat.append(int(np.degrees(radar.vel)))
	mobOmegaHat.append(mobile.omega_hat)
	modOmegaHat.append(rk.x[1])

	#deltaOmegaHat.append(mobile.omega_hat - rk.x[1])
	ekfDist.append(get_pixel_between_sun_and_planet(rk.x))
	
	uncertainty.append(omegaDiff(mobile.omega, rk.x[0]))
	#prevX = z
	if(prevX != z):
		#print(i)
		#uncertainty2.append(get_pixel_between_sun_and_planet(rk.x) - get_pixel_between_sun_and_planet([mobile.omega]))
		uncertainty2.append(get_pixel_between_sun_and_planet(rk.x) - z)
		rk.update(array([z]), HJacobian_at, get_pixel_between_sun_and_planet)
	else:
		uncertainty2.append(0)
	prevX = z
	prevOmega = rk.x[0]
	prevOmegaHat = rk.x[1]


import matplotlib.pyplot as plt


t = np.arange(0, testPeriod, dt)
plt.subplot(2, 1, 1)
plt.title('Expected Omega')
plt.xlabel('Time(s)')
plt.ylabel('Omega(rad)')
plt.axhline(y=175)
plt.axhline(y=-175)
plt.plot(t, ekfDist, 'r.',t, measureDist, 'b.', t, uncertainty2, 'g--')
plt.subplot(2, 1, 2)
plt.ylabel('Actual - Expected: Omega Hat')
plt.axhline(y=np.pi)
plt.axhline(y=-np.pi)
plt.plot(t, modOmega, 'r--')
'''
plt.subplot(2, 1, 2)
plt.ylabel('Actual - Expected: Omega Hat')
plt.axhline(y=np.pi)
plt.axhline(y=-np.pi)
plt.plot(t, modOmegaHat, 'r--', t, mobOmegaHat, 'b--')
'''
plt.show()
