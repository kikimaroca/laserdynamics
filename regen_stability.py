# -*- coding: utf-8 -*-
"""
Created on Mon Oct 17 23:05:19 2016

@author: cpkmanchee
"""

'''

REGEN Dynamics
Dorring, Opt Exp, 2004

Simulation broken down into pumping time (lowQ) and amplification time (highQ)

 lowQ
 -solve for gain

 highQ
 -solve for pulse amplification
 -solve for gain depletion

 HighQ phase will included many round trips of the pulse in the cavity.


LowQ:

dg/dt = (g0-g)/tau

g2 = g0 + (g1-g0)*exp(-(Td-Tg)/tau))
 

HighQ:

dg/dt = (g0-g)/tau - (g*E)/(Esat*Tr)

dE/dt = E(g-l)/Tr


g0 = small signal gain
g1 = gain at begining of low phase
g2 = gain at begining of high phase
Td = dumping time = 1/f, f is rep rate
Tg = gate time = N*Tr, N is number of round trips
Tr = roundtrip time
Esat = saturation energy = hv/(lamba*(sigma_e+sigma_a))
tau = upper state lifetime

'''


import numpy as np
import scipy as sp
import scipy.integrate as integrate
import matplotlib.pyplot as plt
import sys


def rk4(f, x, y0, const_args = [], abs_x = False):
	'''
	functional form
	y'(x) = f(x,y,constants)

	f must be function, f(x,y,const_args)
	x = array
	y0 = initial condition,
	cont_args = additional constants required for f

	returns y, integrated array
	'''

	N = np.size(x)
	y = np.zeros(np.shape(x))
	print(N,y)
	if N>1:
		y[0] = y0

	dx = np.gradient(x)

	if abs_x:
		dx = np.abs(dx)

	for i in range(N-1):
		k1 = f(x[i], y[i], *const_args)
		k2 = f(x[i] + dx[i]/2, y[i] + k1*dx[i]/2, *const_args)
		k3 = f(x[i] + dx[i]/2, y[i] + k2*dx[i]/2, *const_args)
		k4 = f(x[i] + dx[i], y[i] + k3*dx[i], *const_args)

		y[i+1] = y[i] + (k1 + 2*k2 + 2*k3 + k4)*dx[i]/6

	return y


def g2Low(g1):
    
    return (g0 - (g0-g1)*np.exp(-(Td-Tg)/tau))

def dgHigh(t, g, E):

	return ((g0-g)/tau - g*E/(Esat*Tr))

def dEHigh(t, E, g):

	return (E*(g-l)/Tr)


#constants
h = 6.62606957E-34	#J*s
c = 299792458.0		#m/s

d = 1.6         #cavity length, m
l = 0.05  		#cavity losses
g0 = 0.4        #small signal gain
E_seed = 1E-9  	#seed pulse energy in J
tau = 300E-6    #upper state lifetime, s
frep = 1E3      #rep rate
Td = 1/(frep)   #dumping time

N = 20          # number of roundtrips
Tr = 2*d/c      # round trip time
Tg = N*Tr  		#gate time, integer round trips


g_cur = 0
E_cur = E_seed


#Low-Q Phase
g_cur = g2Low(g_cur)

#High-Q Phase

for i in range(N):

	dt = Tr

	E_cur = rk4(dEHigh, Tr, E_cur, [g_cur])
	g_cur = rk4(dgHigh, Tr, g_cur, [E_cur])


print(E_cur,g_cur)


