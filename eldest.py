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

import scipy
import scipy.integrate as integrate
import numpy as np
import sciconv
import complex_integration as ci
import in_out

#-------------------------------------------------------------------------
# Input parameters

rdg_au        = 0.5           # transition dipole moment into the resonant state
cdg           = 0.5           # transition dipole moment into any continuum state

# parameters of the investigated system
# the ground state energy is being defined as Eg = 0
Er_eV         = 14.0          # resonance energy in eV
E_kin_eV      = 2.0           # kinetic energy of secondary electron
E_fin_eV      = 12.0          # final state energy in eV

Gamma_eV      = 5.0           # electronic decay width of the resonant state

# laser parameters
Omega_min_eV  = 12.0          # scanning XUV pulse from Omega_min-eV to
Omega_max_eV  = 16.0          #
TX_s          = 100E-18       # duration of the XUV pulse in seconds
A0X           = 1.0           # amplitude of the XUV pulse

omega_eV      = 1.0           # IR pulse
TL_s          = 1.0E-11       # duration of the IR streaking pulse
A0L           = 1.0           # amplitude of the IR pulse
delta_t_s     = 5.0E-13       # time difference between the maxima of the two pulses

# parameters of the simulation
tmax_s        = 3.0E-16       # simulate until time tmax in seconds
timestep_s    = 50E-18        # evaluate expression every timestep_s seconds 
Omega_step_eV = 0.2           # energy difference between different evaluated Omegas
#-------------------------------------------------------------------------

print 'Hello World'

in_out.check_input(Er_eV, E_kin_eV, E_fin_eV, Gamma_eV,
                   Omega_min_eV, Omega_max_eV, TX_s, A0X,
                   omega_eV, TL_s, A0L, delta_t_s,
                   tmax_s, timestep_s, Omega_step_eV)

Omega= 13.5
Omega_au = sciconv.ev_to_hartree(Omega)

#-------------------------------------------------------------------------
# Definitions of reusable functions
#-------------------------------------------------------------------------

#-------------------------------------------------------------------------
# Convert input parameters to atomic units
#-------------------------------------------------------------------------
Er_au          = sciconv.ev_to_hartree(Er_eV)
E_kin_au       = sciconv.ev_to_hartree(E_kin_eV)
E_fin_au       = sciconv.ev_to_hartree(E_fin_eV)

Gamma_au       = sciconv.ev_to_hartree(Gamma_eV)

# laser parameters
Omega_min_au  = sciconv.ev_to_hartree(Omega_min_eV)
Omega_max_au  = sciconv.ev_to_hartree(Omega_max_eV)
TX_au         = sciconv.second_to_atu(TX_s)

omega_au      = sciconv.ev_to_hartree(omega_eV)
TL_au         = sciconv.second_to_atu(TL_s)
delta_t_au    = sciconv.second_to_atu(delta_t_s)

# parameters of the simulation
tmax_au       = sciconv.second_to_atu(tmax_s)
timestep_au   = sciconv.second_to_atu(timestep_s)
Omega_step_au = sciconv.ev_to_hartree(Omega_step_eV)

VEr_au        = np.sqrt(Gamma_au/ (2*np.pi))

#-------------------------------------------------------------------------
# physical defintions of functions
# XUV pulse
f  = lambda t1: 1./4 * ( np.exp(2j * np.pi * t1 / TX_au)
                      + 2
                      + np.exp(-2j * np.pi * t1 /TX_au) )

fp = lambda t1: np.pi/(2j*TX_au) * ( - np.exp(2j*np.pi*t1/TX_au)
                                     + np.exp(-2j*np.pi*t1/TX_au) )

FX = lambda t1: - A0X * np.cos(Omega_au * t1) * fp(t1) + A0X * Omega_au * np.sin(Omega_au * t1) * f(t1)

# IR pulse
A_IR = lambda t3: A0L * np.sin(np.pi * (t3 - delta_t_au + TL_au/2) / TL_au)**2

# functions
fun_inf_TX2_1 = lambda t1: np.exp(t1 * complex(Gamma_au/2,Er_au)) * FX(t1)
fun_inf_TX2_2 = lambda t2: np.exp(t2 * complex(Gamma_au/2, Er_au + E_kin_au))

fun_TX2_delta_1 = lambda t1: np.exp(t1 * complex(Gamma_au/2,Er_au))
fun_TX2_delta_2 = lambda t2: np.exp(t2 * complex(Gamma_au/2, Er_au + E_kin_au))

#-------------------------------------------------------------------------
# very important: The first Variable in the definition of the function marks the inner
# integral, while the second marks the outer integral.
# If any limit is replaced by the integration variable of the outer integral,
# this is always specified as x, never as the actual name of the variable.
#

t_au = -TX_au/2


#-------------------------------------------------------------------------
while ((t_au <= TX_au/2) and (t_au <= tmax_au)):
#-------------------------------------------------------------------------
#    fun1 = lambda t1: np.exp(t1 * complex(Gamma_au/2,Er_au)) * FX(t1)
#    fun2 = lambda t2: np.exp(t2 * complex(Gamma_au/2, Er_au + E_kin_au))

    Omega_au = Omega_min_au
    outlines = []
    
    while (Omega_au < Omega_max_au):
        I = ci.complex_double_quadrature(fun_inf_TX2_1,fun_inf_TX2_2,
                                         -TX_au/2, t_au,
                                         lambda x: x, lambda x: t_au)
       

        J = I[0] * np.exp(1j * E_kin_au * t_au) * rdg_au * VEr_au

        string = in_out.prep_output(J, Omega_au)
        outlines.append(string)
        
        Omega_au = Omega_au + Omega_step_au
    
    
    in_out.doout(t_au,outlines)

    t_au = t_au + timestep_au


print 't                    = ', sciconv.atu_to_second(t_au)
print 'TX/2                 = ', sciconv.atu_to_second(TX_au/2)
print 'delta_t_au - TL_au/2 = ', sciconv.atu_to_second(delta_t_au - TL_au/2)
print 'tmax                 = ', sciconv.atu_to_second(tmax_au)


#-------------------------------------------------------------------------
while (t_au >= TX_au/2 and t_au <= (delta_t_au - TL_au/2) and (t_au <= tmax_au)):
#-------------------------------------------------------------------------
    print 'in while loop 2'
    #fun1 = lambda t1: np.exp(t1 * complex(Gamma_au/2,Er_au))
    #fun2 = lambda t2: np.exp(t2 * complex(Gamma_au/2, Er_au + E_kin_au))

    Omega_au = Omega_min_au
    outlines = []
    
    while (Omega_au < Omega_max_au):
        # Integral 2
        I = ci.complex_double_quadrature(fun_inf_TX2_1,fun_inf_TX2_2,
                                         -TX_au/2, TX_au/2,
                                         lambda x: x, lambda x: TX_au/2)
        I_inf_TX2 = I[0] * np.exp(1j * E_kin_au * TX_au/2) * rdg_au * VEr_au
        #
        # Integral 3
        I = ci.complex_double_quadrature(fun_TX2_delta_1,fun_TX2_delta_2,
                                         TX_au/2, t_au,
                                         lambda x: x, lambda x: TX_au/2)
        I_TX2_t_t1 = I[0] * np.exp(1j * E_kin_au * TX_au/2) * rdg_au * VEr_au
        #
        # Integral 4
        I = ci.complex_double_quadrature(fun_TX2_delta_1,fun_TX2_delta_2,
                                         TX_au/2, t_au,
                                         lambda x: TX_au/2, lambda x: t_au)
        I_TX2_t_TX2 = I[0] * np.exp(1j * E_kin_au * t_au) * rdg_au * VEr_au
       

        J = I_inf_TX2 + I_TX2_t_t1 + I_TX2_t_TX2

        string = in_out.prep_output(J, Omega_au)
        outlines.append(string)
        
        Omega_au = Omega_au + Omega_step_au
    
    
    in_out.doout(t_au,outlines)

    t_au = t_au + timestep_au
