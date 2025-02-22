#todo: proper error values, readouts for all areas at selected points (chamber, throat, nozzle)

import math
import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import fsolve
import rayleigh

#IN ALL FUTURE SOLVERS THE FOLLOWING PARAMS MUST BE CALCULATED FOR EVERY STEP
#Mach number
#Pressure
#Density
#Temperature
#Speed of Sound math.sqrt(287 * gamma * Temperature)
#Velocity M*SoS
#Stagnation pressure (isentropic)
#Stagnation temperature (flow)
#Stagnation density (relations)

#chamber
#throat (real or theoretical, choked values need to be stored somewhere)
#exhaust

#define a few spare inputs
def getSP(P, M, gamma):
    P_SP = (1 + ((gamma - 1) / 2) * M**2)**(-gamma / (gamma - 1))
    SP_P = 1 / P_SP
    SP = SP_P * P
    return SP

def getST(T, M, gamma):
    T_ST = (1 + ((gamma - 1) / 2) * M**2)**(-1)
    ST_T = 1 / T_ST
    ST = ST_T * T
    return ST

def getSD(D, M, gamma):
    D_SD = (1 + ((gamma - 1) / 2) * M**2)**(-1 / (gamma - 1))
    SD_D = 1 / D_SD
    SD = SD_D * D
    return SD

def getSoS(gamma, Rs, T):
    return math.sqrt(Rs * gamma * T)

def estD(P, M, R, T):
    return (P * M) / (R * T)

gamma = 1.33
Rs = 287
R = 8314.5 #unsure if this is correct, but 8.3145 seems to give bunk values for D
airM = 28.97
steamM = 18.015
expansionRatio = 75
#for subsonic flow, expansionRatio is applied from the throat to the outlet
#for supersonic flow, expansionRatio is applied from the chamber to the outlet
#expansion ratio is effectively the widest point of the nozzle divided by the narrowest point in the engine (either chamber or throat)
#solver only goes up to an exitM of 10, or an expansion ratio at most of 1426:1, 0.00001 steps

chamberM = 0.25
chamberP = 20001555
chamberT = 3580
chamberD = estD(chamberP, steamM, R, chamberT)
chamberSoS = getSoS(gamma, Rs, chamberT)
chamberV = chamberM * chamberSoS
chamberSP = getSP(chamberP, chamberM, gamma)
chamberST = getST(chamberT, chamberM, gamma)
chamberSD = getSD(chamberD, chamberM, gamma)
chamberA = 1 #by definition the cross sectional "area" of the combustion chamber is set to 1


print("=====COMBUSTION CHAMBER CONDITIONS=====")
print("Mach:", chamberM)
print("Pressure (Pa):", chamberP)
print("Density (kg/m3):", chamberD)
print("Temperature (K):", chamberT)
print("Speed of sound (m/s):", chamberSoS)
print("Velocity (m/s):", chamberV)
print("Stagnation pressure (Pa):", chamberSP)
print("Stagnation temperature (K):", chamberST)
print("Stagnation density (kg/m3):", chamberSD)
print()

#choked conditions

def getChokedST(ST, M, gamma):
    ST_chokedST = (rayleigh.rayleighFunc(M, gamma)) / (rayleigh.rayleighFunc(1, gamma))
    chokedST_ST = 1 / ST_chokedST
    chokedST = chokedST_ST * ST
    return chokedST

def getChokedT(T, M, gamma):
    T_chokedT = (((gamma + 1) * M) / (1 + gamma * M**2))**2
    chokedT_T = 1 / T_chokedT
    chokedT = chokedT_T * T
    return chokedT

def getChokedP(P, M, gamma):
    P_chokedP = (gamma + 1) / (1 + gamma * M**2)
    chokedP_P = 1 / P_chokedP
    chokedP = chokedP_P * P
    return chokedP

def getChokedSP(SP, M, gamma):
    SP_chokedSP = ((gamma + 1) / (1 + gamma * M**2)) * ((2 / (gamma + 1)) * (1 + ((gamma - 1) / 2) * M**2))**(gamma / (gamma - 1))
    chokedSP_SP = 1 / SP_chokedSP
    chokedSP = chokedSP_SP * SP
    return chokedSP

def getChokedD(D, M, gamma):
    D_chokedD = (1 + gamma * M**2) / ((gamma + 1) * M**2)
    chokedD_D = 1 / D_chokedD
    chokedD = chokedD_D * D
    return chokedD

throatM = 1 #by definition
throatP = getChokedP(chamberP, chamberM, gamma)
throatD = getChokedD(chamberD, chamberM, gamma)
throatT = getChokedT(chamberT, chamberM, gamma)
throatSoS = getSoS(gamma, Rs, throatT)
throatV = throatM * throatSoS
throatSP = getChokedSP(chamberSP, chamberM, gamma)
throatST = getChokedST(chamberST, chamberM, gamma)
throatSD = getSD(throatD, throatM, gamma)

def getA_Achoked(M):
    partA = ((gamma + 1) / 2)**((-(gamma + 1)) / (2 * (gamma - 1)))
    partB = (1 + ((gamma - 1) / 2) * M**2)**((gamma + 1) / (2 * (gamma - 1)))
    return partA * (partB / M)

def solveDivOnly(chamberM, chamberA, expansionRatio):
    supM = list(np.round(np.arange(1.,10.,0.00001), 6))
    supAR = [getA_Achoked(x) for x in supM]
    supAreaRatio = dict(zip(supM, supAR))
    chokedAR = getA_Achoked(chamberM)
    finalA_chokedA = chokedAR * expansionRatio
    finalM, approxA_chokedA = min(supAreaRatio.items(), key=lambda x: abs(finalA_chokedA - x[1]))
    exitA = chamberA * expansionRatio
    exitM = finalM
    error = abs(finalA_chokedA - approxA_chokedA)
    return exitA, exitM, error #this might be correct, you need to fix when not drunk. for div only, choked area > chamber area (i think)

def solveConDiv(chamberM, chamberA, expansionRatio):
    supM = list(np.round(np.arange(1.,10.,0.00001), 6))
    supAR = [getA_Achoked(x) for x in supM]
    supAreaRatio = dict(zip(supM, supAR))
    #subM = list(np.round(np.arange(0.,1.,0.00001), 6))
    #subAR = [getA_Achoked(x) for x in subM]
    #subAreaRatio = dict(zip(subM, subAR))
    #2 dicts of values ready to go, for now the subsonic values are unneeded
    chamberA_throatA = getA_Achoked(chamberM)
    throatA = chamberA / chamberA_throatA
    finalM, approxA_chokedA = min(supAreaRatio.items(), key=lambda x:abs(expansionRatio - x[1]))
    exitA = expansionRatio * throatA
    error = 0 #fix this for now
    return throatA, exitA, finalM, error

if chamberM > 1:
    print("(Note: choked throat conditions are entirely theoretical")
    print("       As the flow through the combustor is entirely supersonic,")
    print("       there's no need to choke the flow with a de Laval nozzle")
    print("       throat, as the flow can just be expanded and accelerated")
    print("       isentropically. Theoretical choked throat conditions are")
    print("       necessary to calculate the influence of the area ratio,")
    print("       as the relevant isentropic flow relations only provide for")
    print("       the ratio of A/Achoked (the max nozzle area divided by the")
    print("       the area of the choked throat, derived from gamma and exit")
    print("       Mach number). See the NASA Isentropic Flow for a Calorically")
    print("       Perfect Gas, equation (9).)")
    exitA, exitM, error = solveDivOnly(chamberM, chamberA, expansionRatio)
    print("Exit area (m2):", exitA)
    print("Exit Mach:", exitM)
    print("Area ratio error (m2):", error)
elif chamberM < 1:
    print("(Note: choked throat conditions are both practically and theoretically")
    print("       relevant in this case where the combustor flow is subsonic.")
    print("       The outlet from the combustion chamber needs to be accelerated")
    print("       through a de Laval nozzle to accelerate up to a useful velocity")
    print("       for thrust. See the NASA Isentropic Flow for a Calorically")
    print("       Perfect Gas, equation (9).)")
    throatA, exitA, exitM, error = solveConDiv(chamberM, chamberA, expansionRatio)
print()
print("=====CHOKED THROAT CONDITIONS=====")
print("Mach:", throatM)
print("Pressure (Pa):", throatP)
print("Density (kg/m3):", throatD)
print("Temperature (K):", throatT)
print("Speed of sound (m/s):", throatSoS)
print("Velocity (m/s):", throatV)
print("Stagnation pressure (Pa):", throatSP)
print("Stagnation temperature (K):", throatST)
print("Stagnation density (kg/m3):", throatSD)
print()

#throatA = 1.61167
#exitM = 4.24982
#exitA = 18

def getExitP(chokedP, M, gamma):
    P_chokedP = (gamma + 1) / (1 + gamma * M**2)
    P = P_chokedP * chokedP
    return P

def getExitD(chokedD, M, gamma):
    D_chokedD = (1 + gamma * M**2) / ((gamma + 1) * M**2)
    D = D_chokedD * chokedD
    return D

def getExitT(chokedT, M, gamma):
    T_chokedT = (((gamma + 1) * M) / (1 + gamma * M**2))**2
    T = T_chokedT * chokedT
    return T

def getExitSP(chokedSP, M, gamma):
    SP_chokedSP = ((gamma + 1) / (1 + gamma * M**2)) * ((2 / (gamma + 1)) * (1 + ((gamma - 1) / 2) * M**2))**(gamma / (gamma - 1))
    SP = SP_chokedSP * chokedSP
    return SP

def getExitST(chokedST, M, gamma):
    ST_chokedST = (rayleigh.rayleighFunc(M, gamma)) / (rayleigh.rayleighFunc(1, gamma))
    ST = ST_chokedST * chokedST
    return ST

exitP = getExitP(throatP, exitM, gamma)
exitD = getExitD(throatD, exitM, gamma)
exitT = getExitT(throatT, exitM, gamma)
exitSoS = getSoS(gamma, Rs, exitT)
exitV = exitM * exitSoS
exitSP = getExitSP(throatSP, exitM, gamma)
exitST = getExitST(throatST, exitM, gamma)
exitSD = getSD(exitD, exitM, gamma)

print("=====NOZZLE OUTLET CONDITIONS=====")
print("Mach:", exitM)
print("Pressure (Pa):", exitP)
print("Density (kg/m3):", exitD)
print("Temperature (K):", exitT)
print("Speed of sound (m/s):", exitSoS)
print("Velocity (m/s):", exitV)
print("Stagnation pressure (Pa):", exitSP)
print("Stagnation temperature (K):", exitST)
print("Stagnation density (kg/m3):", exitSD)
print()
Isp = exitV / 9.81
print("Specific impulse (s):", Isp)
