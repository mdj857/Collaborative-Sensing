from filterpy.common import Q_discrete_white_noise
from filterpy.kalman import ExtendedKalmanFilter
from math import *
from numpy import eye, array, asarray
from numpy.random import randn

import numpy as np

import time

class RadarSim(object):
    """ Simulates the radar signal returns from an object
    flying at a constant altityude and velocity in 1D. 
    """
    
    def __init__(self, dt, pos, vel, alt):
        self.pos = pos
        self.vel = vel
        self.alt = alt
        self.dt = dt
        
    def get_range(self):
        """ Returns slant range to the object. Call once 
        for each new measurement at dt time from last call.
        """
        
        # add some process noise to the system
        self.vel = self.vel  + .1*randn()
        self.alt = self.alt + .1*randn()
        if(self.pos > 500):
        	self.pos = 0
        self.pos = self.pos + self.vel*self.dt
    
        # add measurement noise
        err = self.pos * 0.05*randn()
        slant_dist = sqrt(self.pos**2 + self.alt**2)
        
        return slant_dist + err

camData = [268.7824399,
		279.4655614,
		284.4292531,
		285.7271426,
		282.1435805,
		277.61304,
		269.031596,
		259.6247292,
		247.370168,
		234.1324412,
		223.8950647,
		209.954757,
		209.954757,
		209.954757,
		209.954757,
		209.954757,
		209.954757,
		209.954757,
		209.954757,
		209.954757,
		209.954757,
		209.954757,
		209.954757,
		209.954757,
		196.7358635,
		103.0970417,
		120.0708124,
		130.9809146,
		154.3016526,
		169.5670959,
		184.8377667,
		201.1019642,
		215.5411794,
		215.5411794,
		215.5411794,
		215.5411794,
		226.0486673,
		218.3048327,
		182.1482912,
		171.8167629,
		213.3775996,
		136.4734406,
		178.9413312,
		178.9413312,
		178.9413312,
		178.9413312,
		178.9413312,
		178.9413312,
		178.9413312,
		157.8131807,
		157.8131807,
		197.2536438,
		200.9601951,
		228.659135,
		251.5432368,
		266.8332813,
		277.7048793,
		283.8045102,
		285.8898389,
		285.259531,
		279.594349,
		271.1401851,
		261.7250466,
		250.4595776,
		237.118114,
		221.9954954,
		210.857772,
		210.857772,
		210.857772,
		210.857772,
		210.857772,
		210.857772,
		210.857772,
		210.857772,
		210.857772,
		210.857772,
		210.857772,
		210.857772,
		210.857772,
		200.6389793,
		101.9656805,
		119.0798052,
		130.9809146,
		154.175225,
		170.425937,
		185.6906029,
		201.1019642,
		215.5411794,
		215.5411794,
		215.5411794]

i=-1

class MobileSim(object):
	def __init__(self, delta, omega, omega_hat):
		self.delta = delta
		self.omega = omega
		self.omega_hat = omega_hat
		self.i = 0

	def get_x_pos(self):
		
		self.omega_hat = self.omega_hat + .00001*randn()
		
		#if(self.omega < 50):
		self.omega = self.omega + self.omega_hat*self.delta
		#else:
		#	self.omega = self.omega - self.omega_hat*self.delta
		#self.omega = self.omega % (2 * np.pi)
		self.i+=1
		if(self.i == 90):
			self.i = 0
		return camData[self.i]
		err = 0.001*randn()
		x_pos = d0 / p * cos(self.omega) * sin(alpha)
		return x_pos + err

def HJacobian_at_test(x):
    """ compute Jacobian of H matrix at x """

    horiz_dist = x[0]
    altitude   = x[2]
    denom = sqrt(horiz_dist**2 + altitude**2)
    return array ([[horiz_dist/denom, 0., altitude/denom]])
   
def hx(x):
    """ compute measurement for slant range that
    would correspond to state x.
    """
    
    return (x[0]**2 + x[2]**2) ** 0.5

def HJacobian_at(x):
	angular_vel = x[1]
	angular_pos = x[0]
	return array([[(-1)* sin(alpha) * sin(angular_pos)*p, 0.]])

def get_pixel_between_sun_and_planet(x):
	print(np.abs(p * cos(x[0]) * sin(alpha)))
	return p * cos(x[0]) * sin(alpha)

#Number of pixels that represents distance d0
p = 285

# physical distance between Earth and Sun in a callibrated image
d0 = 10

# angle of elevation from camera to plane of mobile
alpha = np.pi/2

# sampling rate for images
dt = 0.05

#length of time to analyze for
testPeriod = 20

#Init mobile simulator
mobile = MobileSim(dt, np.pi/2, 2*np.pi/6.55)
radar = RadarSim(dt, pos=0., vel=100., alt=1000.)

#Init extended kalman filter
rk = ExtendedKalmanFilter(dim_x=2, dim_z=1)

# make an imperfect starting guess
rk.x = array([np.pi/2, 2*np.pi/6.55])
#rk.x = array([radar.pos-100, radar.vel+100, radar.alt+1000])

# state transition matrix
rk.F = np.asarray([[1, dt], [0, 1]])
#rk.F = eye(3) + array([[0, 1, 0],
#                       [0, 0, 0],
#                       [0, 0, 0]]) * dt

# measurement noise matrix
#rk.R = np.diag([(2 * np.pi / 6.55) ** 2])
rk.R = np.diag([0.1])
#rk.R = np.diag([(dt ** 2) / 8])
#rk.R = np.diag([0.01])

# process noise -- basically, how close our process (i.e kinematics eqns)
# model true system behavior
#--
#rk.Q = Q_discrete_white_noise(dim=2, dt=dt, var = .1)
omega_noise = np.pi/2
rk.Q[0:2, 0:2] = np.array([[omega_noise,0],[0,0.001]])
#rk.Q[0:2, 0:2] = np.array([[0,0],[0,0]])
#rk.Q[0:2, 0:2] = Q_discrete_white_noise(2, dt=dt, var=0)
#rk.Q = np.diag(np.diag(rk.Q)) # Zero out non-diagonal elements

print("Process noise matrix" , rk.Q)
#--rk.Q = 0

# covariance matrix -- set initial apriori values for "uncertainty"
#--
rk.P *= 0.1
#rk.P *= 2

mobOmega, modOmega, mobOmegaHat , modOmegaHat = [],[],[],[]
deltaOmega, deltaOmegaHat = [],[]
uncertainty,uncertainty2 = [],[]

prevX = 0

for i in range(int(testPeriod/dt)):
	#detector.runCascadeClassifier()
	z = mobile.get_x_pos() #SIMULATION
	#z = radar.get_range()
	#rk.x[0] = rk.x[0] % (2 * np.pi)
	#rk.update(array([z]), HJacobian_at_test, hx)
	rk.update(array([z]), HJacobian_at, get_pixel_between_sun_and_planet)
	#mobOmega.append(int(np.degrees(radar.pos)))
	mobOmega.append(mobile.omega% (2 * np.pi))
	modOmega.append(rk.x[0]% (2 * np.pi))

	deltaOmega.append(mobile.omega - rk.x[0])

	#mobOmegaHat.append(int(np.degrees(radar.vel)))
	mobOmegaHat.append(mobile.omega_hat)
	modOmegaHat.append(rk.x[1])

	deltaOmegaHat.append(mobile.omega_hat - rk.x[1])
	
	uncertainty.append(rk.P[0,0])
	uncertainty2.append(rk.P[1,1])
	if(prevX != z):
		print(i)
		rk.predict()
	prevX = z


import matplotlib.pyplot as plt

t = np.arange(0, testPeriod, dt)
plt.subplot(3, 2, 1)
plt.ylabel('Omega')
plt.plot(t, mobOmega, 'r--', t, modOmega, 'b-')
plt.subplot(3, 2, 2)
plt.ylabel('Actual - Expected: Omega')
plt.plot(t, deltaOmega, 'g-')
plt.subplot(3, 2, 3)
plt.ylabel('Omega Hat')
plt.plot(t, mobOmegaHat, 'r--', t, modOmegaHat, 'b-')
plt.subplot(3, 2, 4)
plt.ylabel('Actual - Expected: Omega Hat')
plt.plot(t, deltaOmegaHat, 'g-')

plt.subplot(3, 2, 5)
plt.ylabel('Uncertainty Omega')
plt.plot(t, uncertainty, 'b-')
plt.subplot(3, 2, 6)
plt.ylabel('Uncertainty Omega^')
plt.plot(t, uncertainty2, 'b-')
plt.show()
