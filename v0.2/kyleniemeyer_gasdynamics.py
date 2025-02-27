import numpy as np
from scipy.optimize import root_scalar

# Pint gives us some helpful unit conversion
from pint import UnitRegistry
ureg = UnitRegistry()
Q_ = ureg.Quantity # We will use this to construct quantities (value + unit)

def oblique_shock_delta(theta, gamma, mach):
    '''Calculate oblique shock deflection from shock angle and Mach'''
    return (
        np.arctan((2.0/np.tan(theta)) * (
            (mach**2 * np.sin(theta)**2 - 1) /
            (2 + mach**2 * (gamma + np.cos(2*theta)))
            ))
        )

def get_mach_normal(gamma, mach1):
    '''Calculate Mach number after a normal shock'''
    return np.sqrt(
        (mach1**2 + 2/(gamma - 1))/(2 * gamma * mach1**2/(gamma - 1) - 1)
        )

def oblique_shock_theta(theta, gamma, delta, mach):
    '''Use for theta as unknown variable'''
    return (
        np.tan(delta) - oblique_shock_delta(theta, gamma, mach)
        )

def obliqueShockTheta(mach1, gamma, delta):
    root = root_scalar(
    oblique_shock_theta, x0=50*np.pi/180, x1=30*np.pi/180,
    args=(gamma, delta, mach1)
    )
    theta = root.root
    return theta

def obliqueMach(gamma, inputM, theta, delta):
    mach_1n = inputM * np.sin(theta)
    mach_2n = get_mach_normal(gamma, mach_1n)
    return (
        mach_2n / np.sin(theta - delta)
        )

