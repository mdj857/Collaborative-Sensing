from filterpy.common import Q_discrete_white_noise
from filterpy.kalman import ExtendedKalmanFilter
from math import *
from numpy import eye, array, asarray
from numpy.random import randn

import numpy as np

import time
camData3 = [163,
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
	160]
	
camData2 = [163,
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

camData = [109,
109,
130,
138,
144,
150,
155,
158,
156,
155,
151,
145,
136,
130,
121,
105,
105,
97,
55,
26,
3,
-20,
-20,
-20,
-20,
-20,
-46,
-138,
-151,
-161,
-167,
-174,
-176,
-175,
-174,
-170,
-164,
-158,
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
-151,
-151,
-151,
-151,
-151,
-151,
-143,
110,
119,
125,
126,
131,
138,
145,
153,
154,
157,
156,
155,
151,
145,
136,
130,
121,
106,
106,
96,
57,
31,
9,
-12,
-36,
-36,
-36,
-36,
-36,
-60,
-143,
-155,
-163,
-170,
-174,
-176,
-175,
-174,
-170,
-165,
-158,
-152,
-152,
-152,
-152,
-152,
-152,
-152,
-152,
-152,
-152,
-152,
-152,
-152,
-152,
-152,
-152,
-152,
-152,
-152,
-152,
-145,
106,
114,
124,
125,
128,
136,
142,
149,
155,
156,
157,
157,
152,
149,
139,
133,
125,
110,
110,
99,
60,
33,
10,
-13,
-13,
-13,
-13,
-13,
-38,
-132,
-146,
-157,
-165,
-172,
-175,
-176,
-174,
-173,
-168,
-161,
-155,
-155,
-155,
-155,
-155,
-155,
-155,
-155,
-155,
-155,
-155,
-155,
-155,
-155,
-155,
-155,
-155,
-155,
-155,
-155,
-147,
106,
114,
123,
124,
128,
136,
142,
148,
152,
156,
157,
157,
154,
151,
142,
133,
130,
115,
101,
101,
95,
49,
24,
3,
-19,
-19,
-19,
-19,
-19,
-44,
-133,
-147,
-157,
-165,
-172,
-176,
-176,
-175,
-173,
-169,
-164,
-157,
-149,
-149,
-149,
-149,
-149,
-149,
-149,
-149,
-149,
-149,
-149,
-149,
-149,
-149,
-149,
-149,
-149,
-149,
-149,
-149,
-141,
108,
117,
125,
126,
130,
138,
144,
150,
154,
157,
157,
155,
151,
145,
135,
131,
120,
103,
103,
98,
51,
23,
0,
-22,
-22,
-22,
-22,
-22,
-49,
-138,
-150,
-160,
-168,
-174,
-176,
-175,
-174,
-171,
-166,
-160,
-153,
-153,
-153,
-153,
-153,
-153,
-153,
-153,
-153,
-153,
-153,
-153,
-153,
-153,
-153,
-153,
-153,
-153,
-153,
-153,
-145,
107,
116,
125,
125,
130,
136,
143,
149,
154,
158,
159,
156,
152,
148,
140,
132,
127,
113,
113,
113,
100,
45,
21,
-1,
-23,
-23,
-23,
-23,
-23,
-47,
-135,
-148,
-158,
-166,
-172,
-176,
-176,
-175,
-173,
-168,
-162,
-157,
-149,
-149,
-149,
-149,
-149,
-149,
-149,
-149,
-149,
-149,
-149,
-149,
-149,
-149,
-149,
-149,
-149,
-149,
-149,
-149,
-141,
110,
120,
125,
126,
132,
140,
147,
151,
154,
157,
156,
153,
150,
142,
134,
130,
115,
100,
100,
92,
42,
18,
-5,
-27,
-27,
-27,
-27,
-27,
-54,
-140,
-153,
-161,
-169,
-173,
-176,
-175,
-174,
-170,
-165,
-158,
-152,
-152,
-152,
-152,
-152,
-152,
-152,
-152,
-152,
-152,
-152,
-152,
-152,
-152,
-152,
-152,
-152,
-152,
-152,
-152,
-144]

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
		self.i = (self.i + 1)%len(camData3)
		return camData3[self.i] +10
		#err = 0.001*randn()
		#x_pos =  p * cos(self.omega) * sin(alpha)
		#return x_pos + err

def omegaDiff(sim, exp):
	diff = (sim - exp + np.pi) % (2*np.pi) - np.pi
	if(diff < (-1 * np.pi)):
	  return diff + (2*np.pi)
	else:
	  return diff

def HJacobian_at(x):
	return array([[(-1.0)* sin(x[0])*p, 0.]])

def get_pixel_between_sun_and_planet(x):
	return p * cos(x[0])

#Number of pixels that represents distance d0
p = 175

# sampling rate for images
dt = 0.2

#length of time to analyze for
testPeriod = 500

#Init mobile simulator
mobile = MobileSim(dt,0, 0)
#radar = RadarSim(dt, pos=0., vel=100., alt=1000.)

#Init extended kalman filter
rk = ExtendedKalmanFilter(dim_x=2, dim_z=1)

# make an imperfect starting guess
rk.x = array([0, 2*np.pi/6.55])
#rk.x = array([radar.pos-100, radar.vel+100, radar.alt+1000])

# state transition matrix
rk.F = np.asarray([[1, dt], [0, 1]])

# measurement noise matrix
#rk.R = np.diag([15])
rk.R = np.diag([(1/8) * dt ** 2])

# process noise -- basically, how close our process (i.e kinematics eqns)
# model true system behavior
omega_noise = np.pi/12
rk.Q[0:2, 0:2] = np.array([[omega_noise,0],[0,0.01]])

#print("Process noise matrix" , rk.Q)
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
	z = mobile.get_x_pos() #SIMULATION
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
	#np.abs(z - rk.x[0]) > 100
	zPrime = get_pixel_between_sun_and_planet(rk.x)
	#if(prevX == z or np.abs(zPrime - z) > 180):
	if(np.abs(prevX - z) == 0):
		uncertainty2.append(0)
	else:
		uncertainty2.append(get_pixel_between_sun_and_planet(rk.x) - z)
		rk.update(array([z]), HJacobian_at, get_pixel_between_sun_and_planet)
	prevX = z
	prevOmega = rk.x[0]
	prevOmegaHat = rk.x[1]


import matplotlib.pyplot as plt


t = np.arange(0, testPeriod, dt)
plt.subplot(2, 1, 1)
plt.title('Expected Omega')
plt.xlabel('Time(s)')
plt.ylabel('Earth Distance from Sun')
plt.axhline(y=175)
plt.axhline(y=-175)
plt.plot(t, ekfDist, 'r*',t, measureDist, 'b.', t, uncertainty2, 'g--')
plt.subplot(2, 1, 2)
plt.ylabel('Omega')

plt.plot(t, modOmega, 'r--')
'''
plt.subplot(2, 1, 2)
plt.ylabel('Actual - Expected: Omega Hat')
plt.axhline(y=np.pi)
plt.axhline(y=-np.pi)
plt.plot(t, modOmegaHat, 'r--', t, mobOmegaHat, 'b--')
'''
plt.show()
