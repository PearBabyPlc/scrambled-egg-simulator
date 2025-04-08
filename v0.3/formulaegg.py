import math
import numpy as np
import buzzerrookie_isa as isa

def Palt(gamma, M, Q):
    P = (1 / ((gamma / 2) * M**2)) * Q
    altRange = np.linspace(0, 47000, num=47000)
    Prange = [isa.Pisa(x) for x in altRange]
    PaltDict = dict(zip(altRange, Prange))
    estAlt, estP = min(PaltDict.items(), key=lambda x: abs(P - x[1]))
    return estAlt

def idealPfromMQ(gamma, M, Q):
    P = (1 / ((gamma / 2) * M**2)) * Q
    return P

Theta = 3055 + (5 / 9)

def realGamma(idealGamma, T):
    a = (idealGamma - 1)
    b = math.e**(Theta / T)
    c = 1 + a * ((Theta / T)**2 * (b / (b - 1)**2))
    realGamma = 1 + (a / c)
    return realGamma

def realCp(idealGamma, idealCp, T):
    a = (idealGamma - 1)
    b = math.e**(Theta / T)
    c = (Theta / T)**2 * (b / (b - 1)**2)
    realCp = idealCp * (1 + (a / idealGamma) * c)
    return realCp

def idealSoS(gamma, Rs, T):
    SoS = math.sqrt(gamma * Rs * T)
    return SoS

def idealRayleighFunc(gamma, M):
    a = 1 + ((gamma - 1) / 2) * M**2
    rayleigh = (a * M**2) / (1 + gamma * M**2)**2
    return rayleigh

def idealP_Pch(gamma, M):
    P_Pch = (gamma + 1) / (1 + gamma * M**2)
    return P_Pch

def idealT_Tch(gamma, M):
    T_Tch = (((gamma + 1) * M) / (1 + gamma * M**2))**2
    return T_Tch

def idealD_Dch(gamma, M):
    D_Dch = (1 + gamma * M**2) / ((gamma + 1) * M**2)
    return D_Dch

def idealSP_SPch(gamma, M):
    a = 2 / (gamma + 1)
    b = 1 + ((gamma - 1) / 2) * M**2
    c = gamma / (gamma - 1)
    d = idealP_Pch(gamma, M)
    SP_SPch = d * (a * b)**c
    return SP_SPch

def idealST_STch(gamma, M):
    ST_STch = idealRayleighFunc(gamma, M) / idealRayleighFunc(gamma, 1)
    return ST_STch

def quasiRayleighGamma(gamma, idealGamma, M, maxT):
    T = maxT * idealT_Tch(gamma, M)
    qRgamma = realGamma(idealGamma, T)
    return qRgamma

def idealA_Ach(gamma, M):
    a = 2 / (gamma + 1)
    b = 1 + ((gamma - 1) / 2) * M**2
    c = ((gamma + 1) / (gamma - 1)) / 2
    A_Ach = (1 / M) * a**c * b**c
    return A_Ach

def idealP_SP(gamma, M):
    a = 1 + ((gamma - 1) / 2) * M**2
    P_SP = a**((-gamma) / (gamma - 1))
    return P_SP

def idealT_ST(gamma, M):
    T_ST = (1 + ((gamma - 1) / 2) * M**2)**(-1)
    return T_ST

def idealD_SD(gamma, M):
    a = 1 + ((gamma - 1) / 2) * M**2
    D_SD = a**((-1) / (gamma - 1))
    return D_SD

def quasiNozzleGamma(gamma, idealGamma, M, maxST):
    T = maxST * idealT_ST(gamma, M)
    qNgamma = realGamma(idealGamma, T)
    return qNgamma

def realStagTempRelation(T, ST, idealGamma, realGamma):
    a = (idealGamma / (idealGamma - 1)) * (1 - (T / ST))
    c = 1 / (math.e**(Theta / ST) - 1)
    d = 1 / (math.e**(Theta / T) - 1)
    b = (Theta / ST) * (c - d)
    Msquared = ((2 * ST) / (realGamma * T)) * (a + b)
    return Msquared

def realT_ST(idealGamma, M, T):
    #print("realIsentropic T_ST starting...")
    STmin = (1 / (idealT_ST(idealGamma, M))) * T * 0.4
    STmax = STmin * 2.75
    STrange = np.round(np.arange(STmin,STmax,1), 1)
    realGam = realGamma(idealGamma, T)
    STrelation = [realStagTempRelation(T, x, idealGamma, realGam) for x in STrange]
    ST_Mach = dict(zip(STrange, STrelation))
    Msquared = M**2
    approxST, approxM = min(ST_Mach.items(), key=lambda x:abs(Msquared - x[1]))
    #Merror = abs(Msquared - approxM)
    #error = (Merror / Msquared) * 100
    #errorPercent = str(str(round(error, 6)) + "%")
    T_ST = T / approxST
    #print("realIsentropic T_ST done! Error:", errorPercent)
    return T_ST

def realP_SP(idealGamma, T_ST, T):
    ST = (1 / T_ST) * T
    a = ((math.e**(Theta / ST) - 1) / (math.e**(Theta / T) - 1)) * T_ST**(idealGamma / (idealGamma - 1))
    b = (Theta / T) * ((math.e**(Theta / T)) / (math.e**(Theta / T) - 1)) - (Theta / ST) * ((math.e**(Theta / ST)) / (math.e**(Theta / ST) - 1))
    P_SP = a * math.exp(b)
    return P_SP

def realD_SD(idealGamma, T_ST, T):
    ST = (1 / T_ST) * T
    a = ((math.e**(Theta / ST) - 1) / (math.e**(Theta / T) - 1)) * T_ST**(1 / (idealGamma - 1))
    b = (Theta / T) * ((math.e**(Theta / T)) / (math.e**(Theta / T) - 1)) - (Theta / ST) * ((math.e**(Theta / ST)) / (math.e**(Theta / ST) - 1))
    D_SD = a * math.exp(b)
    return D_SD

def realQ_P(idealGamma, T_ST, T):
    ST = (1 / T_ST) * T
    a = (idealGamma / (idealGamma - 1)) * ((ST / T) - 1)
    b = (Theta / T) * ((1 / (math.e**(Theta / ST) - 1)) - ((1 / (math.e**(Theta / T) - 1))))
    Q_P = a + b
    return Q_P

def kineticQ(D, V):
    Q = (1 / 2) * D * V**2
    return Q

def idealQ(gamma, M, P):
    Q = (gamma / 2) * P * M**2
    return Q

#all shock stuff uses ideal, but can accept any gam

def oPout_Pin(gamma, M, theta):
    Pout_Pin = (2 * gamma * M**2 * math.sin(theta)**2 - (gamma - 1)) / (gamma + 1)
    return Pout_Pin

def oTout_Tin(gamma, M, theta):
    a = 2 * gamma * M**2 * math.sin(theta)**2 - (gamma - 1)
    b = (gamma - 1) * M**2 * math.sin(theta)**2 + 2
    c = (gamma + 1)**2 * M**2 * math.sin(theta)**2
    Tout_Tin = (a * b) / c
    return Tout_Tin

def oSPout_SPin(gamma, M, theta):
    a = ((gamma + 1) * M**2 * math.sin(theta)**2) / ((gamma - 1) * M**2 * math.sin(theta)**2 + 2)
    b = gamma / (gamma - 1)
    c = (gamma + 1) / (2 * gamma * M**2 * math.sin(theta)**2 - (gamma - 1))
    d = 1 / (gamma - 1)
    SPout_SPin = a**b * c**d
    return SPout_SPin

def oDout_Din(gamma, M, theta):
    Dout_Din = ((gamma + 1) * M**2 * math.sin(theta)**2) / ((gamma - 1) * M**2 * math.sin(theta)**2 + 2)
    return Dout_Din

def nPout_Pin(gamma, M):
    a = 2 * gamma * M**2 - (gamma - 1)
    Pout_Pin = a / (gamma + 1)
    return Pout_Pin

def nSPout_SPin(gamma, M):
    a = ((gamma + 1) * M**2) / ((gamma - 1) * M**2 + 2)
    b = (gamma + 1) / (2 * gamma * M**2 - (gamma - 1))
    SPout_SPin = a**(gamma / (gamma - 1)) * b**(1 / (gamma - 1))
    return SPout_SPin

def nTout_Tin(gamma, M):
    a = 2 * gamma * M**2 - (gamma - 1)
    b = (gamma - 1) * M**2 + 2
    c = (gamma + 1)**2 * M**2
    Tout_Tin = (a * b) / c
    return Tout_Tin

def nDout_Din(gamma, M):
    a = (gamma + 1) * M**2
    b = (gamma - 1) * M**2 + 2
    Dout_Din = a / b
    return Dout_Din

def detachmentRad(gamma, M):
    a = 4 / (3 * math.sqrt(3) * (gamma + 1))
    b = (M**2 - 1)**(3 / 2) / M**2
    detachmentRad = a * b
    return detachmentRad

#credit to Kyle Niemeyer's Gas Dynamics
def obliqueTheta(gamma, M, delta):
    A = M**2 - 1
    B = (1 / 2) * (gamma + 1) * M**4 * math.tan(delta)
    C = (1 + (1 / 2) * (gamma + 1) * M**2) * math.tan(delta)
    coeffs = [1, C, -A, (B - A*C)]
    roots = np.array([r for r in np.roots(coeffs) if r > 0])
    thetas = np.arctan(1 / roots)
    weakTheta = np.min(thetas)
    strongTheta = np.max(thetas)
    return weakTheta, strongTheta

def nMout(gamma, M):
    MM = ((gamma - 1) * M**2 + 2) / (2 * gamma * M**2 - (gamma - 1))
    Mout = math.sqrt(MM)
    return Mout

def oMout(gamma, M, delta, theta):
    MnIn = M * math.sin(theta)
    MnOut = nMout(gamma, MnIn)
    Mout = MnOut / math.sin(theta - delta)
    return Mout




