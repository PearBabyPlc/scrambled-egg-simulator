import math
import numpy as np

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
    print("realIsentropic T_ST starting...")
    STmin = (1 / (idealT_ST(idealGamma, M))) * T * 0.4
    STmax = STmin * 2.75
    STrange = np.round(np.arange(STmin,STmax,1), 1)
    realGam = realGamma(idealGamma, T)
    STrelation = [realStagTempRelation(T, x, idealGamma, realGam) for x in STrange]
    ST_Mach = dict(zip(STrange, STrelation))
    Msquared = M**2
    approxST, approxM = min(ST_Mach.items(), key=lambda x:abs(Msquared - x[1]))
    Merror = abs(Msquared - approxM)
    error = (Merror / Msquared) * 100
    errorPercent = str(str(round(error, 6)) + "%")
    T_ST = T / approxST
    print("realIsentropic T_ST done! Error:", errorPercent)
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




