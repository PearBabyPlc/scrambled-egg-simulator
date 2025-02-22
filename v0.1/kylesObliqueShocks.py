from matplotlib import pyplot as plt

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

def get_max_shock_angle(gamma, mach):
    '''Calculate shock angle for maximum deflection angle given Mach number.'''
    return np.arcsin(np.sqrt(
        (1.0/(gamma*mach**2))*(
            (gamma+1)*mach**2/4 - 1 +
            np.sqrt((gamma+1)*((gamma+1)*mach**4/16.0 + (gamma-1)*mach**2/2.0 + 1.0))
            )
        ))

machs = np.linspace(1, 15, num=10001, endpoint=True)
deltas = np.arange(0, 40, 5) * np.pi / 180
gamma = 1.4

# solve for weak shock solution
thetas_weak_all = []
thetas_strong_all = []
for delta in deltas:
    thetas_weak = np.zeros_like(machs)
    thetas_strong = np.zeros_like(machs)
    
    for idx, mach in enumerate(machs):
        theta_max = get_max_shock_angle(gamma, mach)
        delta_max = oblique_shock_delta(theta_max, gamma, mach)
        
        if delta >= delta_max:
            thetas_weak[idx] = np.nan
            thetas_strong[idx] = np.nan
        else:
            A = mach**2 - 1
            B = 0.5*(gamma+1) * mach**4 * np.tan(delta)
            C = (1 + 0.5*(gamma+1)*mach**2)*np.tan(delta)
            coeffs = [1, C, -A, (B - A*C)]
            # roots of a cubic equation, two positive solutions
            # (disregard the negative)
            roots = np.array([r for r in np.roots(coeffs) if r > 0])
            
            thetas = np.arctan(1 / roots)
            thetas_weak[idx] = np.min(thetas)
            thetas_strong[idx] = np.max(thetas)
    thetas_weak_all.append(thetas_weak)
    thetas_strong_all.append(thetas_strong)

for thetas_weak, thetas_strong in zip(thetas_weak_all, thetas_strong_all):
    p = plt.plot(machs, thetas_weak*180/np.pi)
    color = p[0].get_color()
    plt.plot(machs, thetas_strong*180/np.pi, c=color)
    
thetas_max = get_max_shock_angle(gamma, machs)
deltas_max = oblique_shock_delta(thetas_max, gamma, machs)
plt.plot(machs, thetas_max*180/np.pi, '--', c='k')
plt.text(
    15.15, thetas_max[-1]*180/np.pi, r'$\delta_{\max}$',
    horizontalalignment='center', verticalalignment='center'
    )

# put labels for degrees
for thetas_weak, delta in zip(thetas_weak_all, deltas):
    theta = np.nanmin(thetas_weak)
    plt.text(
        15.1, theta*180/np.pi, f'{delta*180/np.pi: .0f}',
        horizontalalignment='center', verticalalignment='center'
        )

plt.text(
    15.12, 10, r'$\delta$',
    horizontalalignment='center', verticalalignment='center'
    )

plt.grid(True)
plt.title('Oblique shock wave angle for different deflection angles')
plt.xlabel(r'Upstream Mach number, $M_1$')
plt.ylabel(r'Shock angle, $\theta$')
plt.xlim([0.9, 15.3])
plt.ylim([5, 95])
plt.tight_layout()
#plt.show()
