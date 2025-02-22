import math
import numpy as np
from matplotlib import pyplot as plt
from scipy.optimize import root_scalar
from pint import UnitRegistry
ureg = UnitRegistry()
Q_ = ureg.Quantity

import buzzerrookieisa as isa #isa(altitude)
import inputhelper as iohelper
import kylesObliqueShocks as oblique
import rayleigh

print()
print("====================CONDITIONS====================")

bEarth = 6356752.3141
geomAlt = iohelper.restrictedInput("Enter altitude (0-47350m): ", 0, True, 47350, True)
print()
altitude = (bEarth * geomAlt) / (geomAlt + bEarth)
print("Geopotential altitude (m):", round(altitude, 1))
ambientT, ambientP, ambientD, ambientM = isa.geomISA(geomAlt)
print("Ambient temp (K):", round(ambientT, 1))
print("Ambient pres (Pa):", round(ambientP, 1))
print("Ambient dens (kgm/3):", round(ambientD, 5))
print("Ambient Mach (m/s):", round(ambientM, 1))
print()
Mtest = iohelper.restrictedInput("Enter Mach (1-100): ", 1, False, 100, True)
Vtest = Mtest * ambientM
print("Velocity (m/s):", round(Vtest, 1))
Qtest = (ambientD * Vtest**2) / 2
print("Dynamic pressure (Pa):", round(Qtest, 1))

gamma = 1.4
gasConstant = 287

def SPR(Mach, gamma):
    output = ((1 + ((gamma - 1) / 2) * Mach**2)**(-gamma / (gamma - 1)))**(-1)
    return output

def obliqueShockTheta(mach1, gamma, delta):
    root = root_scalar(
    oblique.oblique_shock_theta, x0=50*np.pi/180, x1=30*np.pi/180,
    args=(gamma, delta, mach1)
    )
    theta = root.root
    return theta

def obliqueDens(gamma, inputM, theta, inputD):
    return (
        inputD * (((gamma + 1) * inputM**2 * (math.sin(theta))**2) / ((gamma - 1) * inputM**2 * (math.sin(theta))**2 + 2))
        )

def obliquePres(gamma, inputM, theta, inputP):
    return (
        inputP * (2 * gamma * inputM**2 * (math.sin(theta))**2 - (gamma - 1)) / (gamma + 1)
        )

def obliqueTemp(gamma, inputM, theta, inputT):
    oblta = 2 * gamma * inputM**2 * (math.sin(theta))**2 - (gamma - 1)
    obltb = (gamma - 1) * inputM**2 * (math.sin(theta))**2 + 2
    obltc = (gamma + 1)**2 * inputM**2 * (math.sin(theta))**2
    return (
        inputT * ((oblta * obltb) / obltc)
        )

def obliqueMach(gamma, inputM, theta, delta):
    mach_1n = inputM * np.sin(theta)
    mach_2n = oblique.get_mach_normal(gamma, mach_1n)
    return (
        mach_2n / np.sin(theta - delta)
        )

print()
print("====================INTAKE====================")

D1deg = iohelper.safeInput("Enter deflection angle 1: ")
D2deg = iohelper.safeInput("Enter deflection angle 2: ")
D3deg = iohelper.safeInput("Enter deflection angle 3: ")
D4deg = D1deg + D2deg + D3deg
print("Deflection angle 4 must equal the sum of the other angles:", D4deg)

#shock 1 - ambient+test in, 

def intakeSolver(ambientD, ambientP, ambientT, Minit, D1deg, D2deg, D3deg, D4deg):
    delta1 = D1deg * np.pi/180
    delta2 = D2deg * np.pi/180
    delta3 = D3deg * np.pi/180
    delta4 = D4deg * np.pi/180
    theta1 = obliqueShockTheta(Minit, gamma, delta1)
    theta1deg = theta1*180/np.pi
    d1 = obliqueDens(gamma, Minit, theta1, ambientD)
    p1 = obliquePres(gamma, Minit, theta1, ambientP)
    t1 = obliqueTemp(gamma, Minit, theta1, ambientT)
    M1 = obliqueMach(gamma, Minit, theta1, delta1)
    print("Shock angle 1:", theta1deg)
    print("Density:", d1)
    print("Pressure:", p1)
    print("Temperature:", t1)
    print("Mach", M1)
    print()

    theta2 = obliqueShockTheta(M1, gamma, delta2)
    theta2deg = theta2*180/np.pi
    d2 = obliqueDens(gamma, M1, theta2, d1)
    p2 = obliquePres(gamma, M1, theta2, p1)
    t2 = obliqueTemp(gamma, M1, theta2, t1)
    M2 = obliqueMach(gamma, M1, theta2, delta2)
    print("Shock angle 2:", theta2deg)
    print("Density:", d2)
    print("Pressure:", p2)
    print("Temperature:", t2)
    print("Mach", M2)
    print()

    theta3 = obliqueShockTheta(M2, gamma, delta3)
    theta3deg = theta3*180/np.pi
    d3 = obliqueDens(gamma, M2, theta3, d2)
    p3 = obliquePres(gamma, M2, theta3, p2)
    t3 = obliqueTemp(gamma, M2, theta3, t2)
    M3 = obliqueMach(gamma, M2, theta3, delta3)
    print("Shock angle 3:", theta3deg)
    print("Density:", d3)
    print("Pressure:", p3)
    print("Temperature:", t3)
    print("Mach", M3)
    print()

    theta4 = obliqueShockTheta(M3, gamma, delta4)
    theta4deg = theta4*180/np.pi
    d4 = obliqueDens(gamma, M3, theta4, d3)
    p4 = obliquePres(gamma, M3, theta4, p3)
    t4 = obliqueTemp(gamma, M3, theta4, t3)
    M4 = obliqueMach(gamma, M3, theta4, delta4)
    print("Shock angle 4:", theta4deg)
    print("Density:", d4)
    print("Pressure:", p4)
    print("Temperature:", t4)
    print("Mach", M4)
    print()
    return d4, p4, t4, M4
    
inletD, inletP, inletT, inletM = intakeSolver(ambientD, ambientP, ambientT, Mtest, D1deg, D2deg, D3deg, D4deg)

normalShockQuery = None

def ramjetNormalShock(inletD, inletP, inletT, inletM):
    combustorM = np.sqrt(
        (inletM**2 + 2/(gamma - 1))/(2 * gamma * inletM**2/(gamma - 1) - 1)
    )
    combustorD = ((gamma + 1) * inletM**2) / ((gamma - 1) * inletM**2 + 2) * inletD
    combustorP = ((2 * gamma * inletM**2 - (gamma - 1)) / (gamma + 1)) * inletP
    combustorT = (((2 * gamma * inletM**2 - (gamma - 1)) * ((gamma - 1) * inletM**2 + 2)) / ((gamma + 1)**2 * inletM**2)) * inletT
    return combustorD, combustorP, combustorT, combustorM

combustorD = None
combustorP = None
combustorT = None
combustorM = None

Cp = 1005

def getMaxHeating(inletM, inletT):
    inletT_ST = (1 + ((gamma - 1) / 2) * inletM**2)**(-1)
    inletST = inletT / inletT_ST
    chokedRayleighFactor = rayleigh.rayleighFunc(1, gamma)
    inletST_chokedST = rayleigh.rayleighFunc(inletM, gamma) / chokedRayleighFactor
    chokedST = (1 / inletST_chokedST) * inletST
    maxHeating = (chokedST - inletST) * Cp
    return chokedST, maxHeating
    #get maximum heat addition before choking

def SP_chokedSP(M, gamma):
    return ((gamma + 1) / (1 + gamma * M**2)) * ((2 / (gamma + 1)) * (1 + ((gamma - 1) / 2) * M**2))**(gamma / (gamma - 1))

#subsonic, mach increases with heating, choked at throat, accelerates out exhaust
def ramjetCombustion(inletM, inletT, inletP, inletD, q):
    inletT_ST = (1 + ((gamma - 1) / 2) * inletM**2)**(-1)
    inletST = inletT / inletT_ST
    exitST = (q / Cp) + inletST
    chokedRayleighFactor = rayleigh.rayleighFunc(1, gamma)
    inletST_chokedST = rayleigh.rayleighFunc(inletM, gamma) / chokedRayleighFactor
    exitST_chokedST = (exitST / inletST) * inletST_chokedST
    chokedST = (1 / exitST_chokedST) * exitST
    exitRF = exitST_chokedST * chokedRayleighFactor
    exitM_subsonic = int()
    exitM_supersonic = int()
    lookupRF_subsonic = int()
    lookupRF_supersonic = int()
    exitM_subsonic, lookupRF_subsonic, exitM_supersonic, lookupRF_supersonic = rayleigh.getMachFromRF(exitRF, gamma)
    subsonicError = abs(exitRF - lookupRF_subsonic)
    supersonicError = abs(exitRF - lookupRF_supersonic)
    print("Subsonic Rayleigh factor (M, RF, error):", exitM_subsonic, lookupRF_subsonic, subsonicError)
    print("Supersonic Rayleigh factor (M, RF, error):", exitM_supersonic, lookupRF_supersonic, supersonicError)
    exitM = exitM_subsonic 
    exitT_ST = (1 + ((gamma - 1) / 2) * exitM**2)**(-1)
    exitT = exitST * exitT_ST
    exitSP_inletSP = SP_chokedSP(exitM, gamma) * (1 / (SP_chokedSP(inletM, gamma)))
    exitSOS = math.sqrt(287 * gamma * exitT)
    exitV = exitSOS * exitM
    chokedP = inletP * ((1 + gamma * inletM**2) / (gamma + 1))
    chokedD = inletD * ((((gamma + 1) * inletM**2)) / (1 + gamma * inletM**2))
    chokedT = exitT * ((((gamma + 1) * exitM)/(1 + gamma * exitM**2))**(-2))
    exitP = chokedP * ((gamma + 1) / (1 + gamma * exitM**2))
    exitD = chokedD * ((1 + gamma * exitM**2) / ((gamma + 1) * exitM**2))
    #chokedT 
    return exitM, exitT, exitSP_inletSP, exitP, exitD, exitSOS, exitV, chokedST, chokedT, chokedP, chokedD
    
#supersonic, mach decreases with heating, choked at throat, accelerates out exhaust
def scramjetCombustion(inletM, inletT, inletP, inletD, q):
    inletT_ST = (1 + ((gamma - 1) / 2) * inletM**2)**(-1)
    inletST = inletT / inletT_ST
    exitST = (q / Cp) + inletST
    chokedRayleighFactor = rayleigh.rayleighFunc(1, gamma)
    inletST_chokedST = rayleigh.rayleighFunc(inletM, gamma) / chokedRayleighFactor
    exitST_chokedST = (exitST / inletST) * inletST_chokedST
    chokedST = (1 / exitST_chokedST) * exitST
    exitRF = exitST_chokedST * chokedRayleighFactor
    exitM_subsonic = int()
    exitM_supersonic = int()
    lookupRF_subsonic = int()
    lookupRF_supersonic = int()
    exitM_subsonic, lookupRF_subsonic, exitM_supersonic, lookupRF_supersonic = rayleigh.getMachFromRF(exitRF, gamma)
    subsonicError = abs(exitRF - lookupRF_subsonic)
    supersonicError = abs(exitRF - lookupRF_supersonic)
    print("Subsonic Rayleigh factor (M, RF, error):", exitM_subsonic, lookupRF_subsonic, subsonicError)
    print("Supersonic Rayleigh factor (M, RF, error):", exitM_supersonic, lookupRF_supersonic, supersonicError)
    exitM = exitM_supersonic 
    exitT_ST = (1 + ((gamma - 1) / 2) * exitM**2)**(-1)
    exitT = exitST * exitT_ST
    exitSP_inletSP = SP_chokedSP(exitM, gamma) * (1 / (SP_chokedSP(inletM, gamma)))
    exitSOS = math.sqrt(287 * gamma * exitT)
    exitV = exitSOS * exitM
    chokedP = inletP * ((1 + gamma * inletM**2) / (gamma + 1))
    chokedD = inletD * ((((gamma + 1) * inletM**2)) / (1 + gamma * inletM**2))
    chokedT = exitT * ((((gamma + 1) * exitM)/(1 + gamma * exitM**2))**(-2))
    exitP = chokedP * ((gamma + 1) / (1 + gamma * exitM**2))
    exitD = chokedD * ((1 + gamma * exitM**2) / ((gamma + 1) * exitM**2))
    return exitM, exitT, exitSP_inletSP, exitP, exitD, exitSOS, exitV, chokedST, chokedT, chokedP, chokedD

while True:
    normalShockQuery = input("Ramjet or scramjet (R or S): ")
    if normalShockQuery == "S":
        print("Scramjet selected, combustor conditions = inlet conditions")
        combustorD = inletD
        combustorP = inletP
        combustorT = inletT
        combustorM = inletM
        combustorSOS = math.sqrt(287 * gamma * combustorT)
        combustorV = combustorM * combustorSOS
        break
    elif normalShockQuery == "R":
        print("Ramjet selected, combustor conditions are after a normal shock")
        combustorD, combustorP, combustorT, combustorM = ramjetNormalShock(inletD, inletP, inletT, inletM)
        combustorSOS = math.sqrt(287 * gamma * combustorT)
        combustorV = combustorM * combustorSOS
        break
    else:
        print("R or S only.")
        continue
        
print()
print("====================COMBUSTOR====================")
print("Pre-combustion conditions:")
print("Mach", combustorM)
print("Temperature (K):", combustorT)
print("Pressure (Pa):", combustorP)
print("Density (kg/m3):", combustorD)
print("Speed of sound (m/s):", combustorSOS)
print("Velocity (m/s):", combustorV)

chokedST, maxHeating = getMaxHeating(combustorM, combustorT)
qString = str("Input heat addition (max before choking = " + str(round(maxHeating, 1)) + "J/kg, up to a stagnation temp of " + str(round(chokedST, 1)) + "K): ")
q = iohelper.restrictedInput(qString, 0, True, maxHeating, True)

if normalShockQuery == "S":
    exitM, exitT, exitSP_inletSP, exitP, exitD, exitSOS, exitV, chokedST, chokedT, chokedP, chokedD = scramjetCombustion(combustorM, combustorT, combustorP, combustorD, q)
elif normalShockQuery == "R":
    exitM, exitT, exitSP_inletSP, exitP, exitD, exitSOS, exitV, chokedST, chokedT, chokedP, chokedD = ramjetCombustion(combustorM, combustorT, combustorP, combustorD, q)

print("Post-combustion conditions:")
print("Mach", exitM)
print("Temperature (K):", exitT)
print("Pressure (Pa):", exitP)
print("Density (kg/m3):", exitD)
print("Speed of sound (m/s):", exitSOS)
print("Velocity (m/s):", exitV)
exitSP_percentage = exitSP_inletSP * 100
print("Exit stagnation pressure (% of inlet SP):", round(exitSP_percentage, 1))

#define the throat
chokedM = 1
print(chokedST)
print(chokedT)
print(chokedP)
print(chokedD)

#define de Laval nozzle


#heat addition brings flow closer to choking, scramjet lowers mach closer to 1, ramjet raises it closer to 1
#then the flow has to be choked in the 

