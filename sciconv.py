##########################################################################
#                                   SCICONV                              #
##########################################################################
# Purpose:                                                               #
#          - A python module for the conversion of numbers between       #
#            different unit systems.                                     #
#                                                                        #
##########################################################################
# written by: Elke Fasshauer May 2018                                    #
##########################################################################

import scipy.constants as constants
#-------------------------------------------------------------------------
#   unit conversion

a_0 = constants.hbar / (constants.m_e * constants.c * constants.fine_structure)
E_h = constants.fine_structure**2 * constants.m_e * constants.c**2

#-------------------------------------------------------------------------
#      Distances, Areas, Volume
def bohr_to_angstrom(d_au):
    d_AA = d_au *a_0 * 1E10
    return d_AA

def angstrom_to_bohr(d_AA):
    d_au = d_AA / a_0 * 1E-10
    return d_au

def bohr_to_meter(d_au):
    d_m = d_au * a_0
    return d_m

def meter_to_bohr(d_m):
    d_au = d_m / a_0
    return d_au

def megabarn_to_sqmeter(sigma_mb):
    sigma_m2 = sigma_mb * 1E-22
    return sigma_m2

def sqmeter_to_megabarn(sigma_m2):
    sigma_mb = sigma_m2 * 1E22

#-------------------------------------------------------------------------
#      Energies
def joule_to_ev(E_J):
    E_eV = E_J / constants.e
    return E_eV

def ev_to_joule(E_eV):
    E_J = E_eV * constants.e
    return E_J

def hartree_to_joule(E_H):
    E_J = E_H * constants.hbar * constants.c * constants.fine_structure / a_0
    return E_J

def joule_to_hartree(E_J):
    E_H = E_J * a_0 / (constants.hbar * constants.c * constants.fine_structure)
    return E_H

def hartree_to_ev(E_H):
    E_eV = joule_to_ev( hartree_to_joule(E_H) )   
    return E_eV

def ev_to_hartree(E_eV):
    E_H = joule_to_hartree( ev_to_joule(E_eV) )
    return E_H

#-------------------------------------------------------------------------
#      Time
def second_to_atu(t_s):
    t_au = t_s * E_h / constants.hbar
    return t_au

def atu_to_second(t_au):
    t_s = t_au * constants.hbar / E_h
    return t_s