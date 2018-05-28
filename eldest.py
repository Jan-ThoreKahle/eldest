#!/usr/bin/python

##########################################################################
#                                    ELDEST                              #
#        Investigating Electronic Decay Processes with Streaking         #
##########################################################################
# Purpose:                                                               #
#          - A program to simulate the streaking process of electronic   #
#            decay processes.                                            #
#                                                                        #
##########################################################################
# written by: Elke Fasshauer May 2018                                    #
##########################################################################

import scipy.integrate as integrate
from numpy import sqrt, sin, cos, pi

#-------------------------------------------------------------------------
# Input parameters

rdg           = 0.5           # transition dipole moment into the resonant state
cdg           = 0.5           # transition dipole moment into any continuum state

# parameters of the investigated system
# the ground state energy is being defined as Eg = 0
Er_eV         = 14.0          # resonance energy in eV
E_kin_eV      = 2.0           # kinetic energy of secondary electron
E_fin_eV      = 12.0          # final state energy in eV

Gamma_eV      = 0.5           # electronic decay width of the resonant state

# laser parameters
Omega_min_eV  = 10.0          # scanning XUV pulse from Omega_min-eV to
Omega_max_eV  = 18.0          #
TX_s          = 100E-18       # duration of the XUV pulse in seconds
A0X           = 1.0           # amplitude of the XUV pulse

omega_eV      = 1.0           # IR pulse
TL_s          = 1.0E-12       # duration of the IR streaking pulse
A0L           = 1.0           # amplitude of the IR pulse
delta_t_s     = 1.0E-15       # time difference between the maxima of the two pulses

# parameters of the simulation
tmax_s        = 1.0E-10       # simulate until time tmax in seconds
timestep_s    = 10E-18        # evaluate expression every timestep_s seconds 
Omega_step_eV = 0.1           # energy difference between different evaluated Omegas



print 'Hello World'
