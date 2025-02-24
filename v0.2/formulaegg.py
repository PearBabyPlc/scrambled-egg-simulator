import math
import numpy as np
import kyleniemeyer_gasdynamics as kyle

#from here: https://www.grc.nasa.gov/www/k-12/airplane/shortc.html
#degXXXX = degrees angle, radXXXX = radians angle (just needs to be specified since py is rad)
#Universal gas constant is like 8.3145 or some shit
#Air gas constant is 286/287, depending on who you ask
#SoS - gamma (generally 1.4), R (R specific, 287), T (Kelvin)
#Isentropic flow - M, SoS, R, gamma, (s)tag/(c)hoked, V, P, T, D, A, Q
### Q (D, V)
### P/sP (gamma, M)
### T/sT (gamma, M)
### D/sD (gamma, M)
### A/cD (gamma, M)
### Prandlt-Meyer (gamma, M)
### Mach angle (M)
### Mass flow rate, just set M to 1 for choked flow (A, sP, sT, gamma, R, M)
### Weight flow, all fucked up, idk just make sure mass is conserved, whatever
### P -> T (P1, P2, gamma, T1) = T2
### T -> P (T1, T2, gamma, P1) = P2 (figure out later)
### vol -> P (vol1, vol2, gamma, P1) = P2
### P -> vol (P1, P2, gamma, vol1) = vol2 (figure out later)

linsteps = 15000 #define how precise linspace is going to be, from Mach 1 to 30

###ISENTROPICS FLOWS###
def SoS(gamma, R, T):
    SoS = math.sqrt(gamma * R * T)
    return SoS

def Q(D, V):
    Q = (1 / 2) * D * V**2
    return Q

def P_sP(gamma, M):
    P_sP = (1 + ((gamma - 1) / 2) * M**2)**((-gamma) / (gamma - 1))
    return P_sP

def T_sT(gamma, M):
    T_sT = (1 + ((gamma - 1) / 2) * M**2)**(-1)
    return T_sT

def D_sD(gamma, M):
    D_sD = (1 + ((gamma - 1) / 2) * M**2)**((-1) / (gamma - 1))
    return D_sD

def A_cD(gamma, M):
    A_cD = ((gamma + 1) / 2)**((-gamma + 1) / (2 * (gamma - 1))) * (((1 + ((gamma - 1) / 2) * M**2)**((gamma + 1) / (2 * (gamma - 1)))) / M)
    return A_cD

def radPrandltMeyer(gamma, M):
    nu = math.sqrt((gamma + 1) / (gamma - 1)) * math.acot(math.sqrt(((gamma - 1) / (gamma + 1)) * (M**2 - 1))) - math.acot(math.sqrt((M**2 - 1)))
    return nu

def radMachAngle(M):
    mu = math.asin(1 / M)
    return mu

def massFlow(A, sP, sT, gamma, R, M):
    mf = ((A * sP) / (math.sqrt(sT))) * (math.sqrt((gamma / R))) * M * (1 + ((gamma - 1) / 2) * M**2)**(-((gamma + 1) / (2 * (gamma - 1))))
    return mf

def PrToTr(P2, P1, gamma):
    Tr = (P2 / P1)**(1 - 1/gamma)
    return Tr

def vrToPr(v1, v2, gamma):
    Pr = (v1 / v2)**gamma
    return P

def radPrandltMeyerToM(PM, gamma):
    rangeM = list(np.linspace(1.1, 30.0, num=linsteps))
    rangeNP = [radPrandltMeyer(gamma, x) for x in rangeM]
    prandly = dict(zip(rangeM, rangeNP))
    approxM, approxPM = min(prandly.items(), key=lambda x: abs(PM - x[1]))
    error = abs(approxPM - PM)
    return approxM, approxPM, error

#todo: incorporate shockwaves, aerodynamics, gas properties

###SHOCK WAVES (see shockwaves.py)

#radDeflection < radDetachment = oblique shock calculation
#radDeflection > radDetachment = normal shock calculation
def radDetachment(M, gamma):
    radDetachment = (4 / (3 * math.sqrt(3) * (gamma + 1))) * (((M**2 - 1)**(3 / 2)) / M**2)
    return radDetachment

#oblique - just going to use Kyle's code to get theta (shock angle)
#radShock = kyle.obliqueShockTheta(Min, gamma, radDeflection)

def obliqueMout(gamma, M, theta, delta):
    machParam = ((gamma - 1) * M**2 * math.sin(theta)**2 + 2) / (2 * gamma * M**2 * math.sin(theta)**2 - (gamma - 1))
    sinParam = math.sin(theta - delta)**2
    Mout = math.sqrt(machParam / sinParam)
    return Mout

def obliqueTout_Tin(gamma, M, theta):
    Tout_Tin = ((2 * gamma * M**2 * math.sin(theta)**2 - (gamma - 1)) * ((gamma - 1) * M**2 * math.sin(theta)**2 + 2)) / ((gamma + 1)**2 * M**2 * math.sin(theta)**2)
    return Tout_Tin

def obliquePout_Pin(gamma, M, theta):
    Pout_Pin = (2 * gamma * M**2 * math.sin(theta)**2 - (gamma - 1)) / (gamma + 1)
    return Pout_Pin

def obliqueDout_Din(gamma, M, theta):
    Dout_Din = ((gamma + 1) * M**2 * math.sin(theta)**2) / ((gamma - 1) * M**2 * math.sin(theta)**2 + 2)
    return Dout_Din

#STout / STin = 1, i.e. it stays constant

def obliqueSPout_SPin(gamma, M, theta):
    a = ((gamma + 1) * M**2 * math.sin(theta)**2) / ((gamma - 1) * M**2 * math.sin(theta)**2 + 2)
    b = gamma / (gamma - 1)
    c = (gamma + 1) / (2 * gamma * M**2 * math.sin(theta)**2 - (gamma - 1))
    d = 1 / (gamma - 1)
    SPout_SPin = a**b * c**d
    return SPout_SPin

#normal

def normalMout(gamma, M):
    machParam = ((gamma - 1) * M**2 + 2) / (2 * gamma * M**2 - (gamma - 1))
    Mout = math.sqrt(machParam)
    return Mout

def normalTout_Tin(gamma, M):
    Tout_Tin = ((2 * gamma * M**2 - (gamma - 1)) * ((gamma - 1) * M**2 + 2)) / ((gamma + 1)**2 * M**2)
    return Tout_Tin

def normalPout_Pin(gamma, M):
    Pout_Pin = (2 * gamma * M**2 - (gamma - 1)) / (gamma + 1)
    return Pout_Pin

def normalDout_Din(gamma, M):
    Dout_Din = ((gamma + 1) * M**2) / ((gamma - 1) * M**2 + 2)
    return Dout_Din

#STout / STin = 1, i.e. it stays constant

def normalSPout_SPin(gamma, M):
    a = ((gamma + 1) * M**2) / ((gamma - 1) * M**2 + 2)
    b = gamma / (gamma - 1)
    c = ((gamma + 1) / (2 * gamma * M**2 - (gamma - 1)))
    d = 1 / (gamma - 1)
    SPout_SPin = a**b * c**d
    return SPout_SPin

