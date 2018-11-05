from filterpy.common import Q_discrete_white_noise
from filterpy.kalman import ExtendedKalmanFilter
from math import *
from numpy import eye, array, asarray
from numpy.random import randn

import numpy as np

import time
import os
import subprocess

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

def merge_estimates(w_sensor1, w_hat_sensor1, w_var_sensor1, w_hat_var_sensor1,
					w_sensor2, w_hat_sensor2, w_var_sensor2, w_hat_var_sensor2):
	# compute merged estimate for w
	a_w = (w_var_sensor1 / (w_var_sensor1 + w_var_sensor2))
	merged_w = (1 - a_w) * w_sensor1 + a_w * w_sensor2

	# compute merged estimate for w_hat
	a_w_hat = (w_var_sensor1 / (w_var_sensor1 + w_var_sensor2))
	merged_w_hat = (1 - a_w_hat) * w_hat_sensor1 + a_w_hat * w_hat_sensor2

	return (merged_w, merged_w_hat)

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
		self.omega = (self.omega + self.omega_hat*self.delta)
		#else:
		#	self.omega = self.omega - self.omega_hat*self.delta
		#self.omega = self.omega % (2 * np.pi)
		self.i = (self.i + 1)%115
		return camData[self.i]
		#err = 0.001*randn()
		#x_pos =  p * cos(self.omega) * sin(alpha)
		#return x_pos + err

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
	return array([[(-1.0)* sin(angular_pos)*p, 0.]])

def get_pixel_between_sun_and_planet(x):
	#print(np.abs(p * cos(x[0])))
	return p * cos(x[0])


#Number of pixels that represents distance d0
p = 185

# physical distance between Earth and Sun in a callibrated image
d0 = 10.

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
#rk.R = np.diag([3.33 ** 2])
#rk.R = np.diag([0.1])

#rk.R = np.diag([((d0/p) ** 2) / 8])
rk.R = np.diag([50])

# process noise -- basically, how close our process (i.e kinematics eqns)
# model true system behavior
#--
#rk.Q = Q_discrete_white_noise(dim=2, dt=dt, var = .1)
omega_noise = np.random.normal(0, np.pi/2)
#omega_noise =np.random.normal(0, 0.0001)
rk.Q[0:2, 0:2] = np.array([[omega_noise,0],[0,0.01]])
#rk.Q[0:2, 0:2] = np.array([[0,0],[0,0]])
#rk.Q[0:2, 0:2] = Q_discrete_white_noise(2, dt=dt, var=0)
#rk.Q = np.diag(np.diag(rk.Q)) # Zero out non-diagonal elements

print("Process noise matrix" , rk.Q)
#--rk.Q = 0

# covariance matrix -- set initial apriori values for "uncertainty"
#--
#rk.P *= 0.01
rk.P *= 0
#rk.P *= 2

mobOmega, modOmega, mobOmegaHat , modOmegaHat = [],[],[],[]
deltaOmega, deltaOmegaHat = [],[]
uncertainty,uncertainty2 = [],[]

prevX = 0
prevOmega = 0
prevOmegaHat = 0


FIFO_FILENAME = "cli_transmit"
OTHER_FIFO = "cli_recieve"

writeFiFo = os.open(FIFO_FILENAME, os.O_WRONLY)
print("Open Write Fifo")
readFiFo = os.open(OTHER_FIFO, os.O_RDONLY)
print("Opened Read Fifo")


for a in range(int(testPeriod/dt)):
	#detector.runCascadeClassifier()
	z = mobile.get_x_pos() #SIMULATION
	#z = radar.get_range()
	#rk.x[0] = rk.x[0] % (2 * np.pi)
	#rk.update(array([z]), HJacobian_at_test, hx)
	rk.update(array([z]), HJacobian_at, get_pixel_between_sun_and_planet)
	rk.predict()

	#mobOmega.append(int(np.degrees(radar.pos)))
	mobOmega.append(mobile.omega)
	modOmega.append(rk.x[0])
	
	scale = 1 / (1.2 * HJacobian_at(rk.x)[0][0])
	
	#deltaOmega.append(mobile.omega - rk.x[0])
	deltaOmega.append(0.2 * scale * rk.y)

	#mobOmegaHat.append(int(np.degrees(radar.vel)))
	mobOmegaHat.append(mobile.omega_hat)
	modOmegaHat.append(rk.x[1])

	#deltaOmegaHat.append(mobile.omega_hat - rk.x[1])
	deltaOmegaHat.append((rk.x[0] - prevOmega) * 1.2 * scale / rk.y)
	
	uncertainty.append(rk.P[0,0])
	#uncertainty2.append(rk.P[1,1])
	uncertainty2.append((rk.x[1] - prevOmegaHat) * 1.2 * scale / rk.y)

	# TODO: Send Values to write FiFo
	write_msg = str([np.round(rk.x[0], 3), np.round(rk.x[1], 3), np.round(rk.P[0][0], 3), np.round(rk.P[1][1], 3)])+";"
	print("Wrote: ", write_msg)
	numBytes = os.write(writeFiFo, write_msg)
	print(numBytes)
	# TODO: Get Values from read FiFO
	otherX =  os.read(readFiFo, 32)
	otherX = otherX.split(";")[0]
	print("Read From FiFO", otherX)
	otherX = otherX[1:-1]
	values = otherX.split(',')
	w_sensor2 = float(values[0])
	w_hat_sensor2 = float(values[1])
	w_var_sensor2 = float(values[2])
	w_hat_var_sensor2 = float(values[3])
	print("Parsed vals: ", w_sensor2, w_hat_sensor2, w_var_sensor2, w_hat_var_sensor2)
	w_merge, w_hat_merge = merge_estimates(np.round(rk.x[0], 3), np.round(rk.x[1], 3), np.round(rk.P[0][0], 3),
										   np.round(rk.P[1][1], 3), w_sensor2, w_hat_sensor2, w_var_sensor2, w_hat_var_sensor2)

	print("Merged Pos & Vel: ", w_merge, w_hat_merge)
	#prevX = z
	#if(prevX != z):
		#print(i)
		#rk.predict()
	prevX = z
	prevOmega = rk.x[0]
	prevOmegaHat = rk.x[1]


import matplotlib.pyplot as plt

t = np.arange(0, testPeriod, dt)
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
