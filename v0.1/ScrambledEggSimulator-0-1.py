import math
import numpy as np
from matplotlib import pyplot as plt
from scipy.optimize import root_scalar
from scipy.optimize import fsolve
from pint import UnitRegistry
ureg = UnitRegistry()
Q_ = ureg.Quantity

import buzzerrookieisa as isa
import inputhelper as iohelper
import kylesObliqueShocks as oblique
import rayleigh
import nozzleSolverModule as nozzle

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
    rampP1 = p1
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
    rampP2 = p2
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
    rampP3 = p3
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
    return d4, p4, t4, M4, theta1, theta2, theta3, theta4, delta1, delta2, delta3, delta4, rampP1, rampP2, rampP3
    
inletD, inletP, inletT, inletM, theta1, theta2, theta3, theta4, delta1, delta2, delta3, delta4, rampP1, rampP2, rampP3 = intakeSolver(ambientD, ambientP, ambientT, Mtest, D1deg, D2deg, D3deg, D4deg)

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
    exitSP = (1 / ((1 + ((gamma - 1) / 2) * exitM**2)**(-gamma / (gamma - 1)))) * exitP ###
    chokedSP = (1 / (SP_chokedSP(exitM, gamma))) * exitSP ###NEW CODE MIGHT NOT WORK
    return exitM, exitT, exitSP_inletSP, exitP, exitD, exitSOS, exitV, chokedST, chokedT, chokedP, chokedD, chokedSP
    
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
    exitSP = (1 / ((1 + ((gamma - 1) / 2) * exitM**2)**(-gamma / (gamma - 1)))) * exitP ###
    chokedSP = (1 / (SP_chokedSP(exitM, gamma))) * exitSP ###NEW CODE MIGHT NOT WORK
    return exitM, exitT, exitSP_inletSP, exitP, exitD, exitSOS, exitV, chokedST, chokedT, chokedP, chokedD, chokedSP

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
    exitM, exitT, exitSP_inletSP, exitP, exitD, exitSOS, exitV, chokedST, chokedT, chokedP, chokedD, chokedSP = scramjetCombustion(combustorM, combustorT, combustorP, combustorD, q)
elif normalShockQuery == "R":
    exitM, exitT, exitSP_inletSP, exitP, exitD, exitSOS, exitV, chokedST, chokedT, chokedP, chokedD, chokedSP = ramjetCombustion(combustorM, combustorT, combustorP, combustorD, q)

print("Post-combustion conditions:")
print("Mach", exitM)
print("Temperature (K):", exitT)
print("Pressure (Pa):", exitP)
print("Density (kg/m3):", exitD)
print("Speed of sound (m/s):", exitSOS)
print("Velocity (m/s):", exitV)
exitSP_percentage = exitSP_inletSP * 100
print("Exit stagnation pressure (% of inlet SP):", round(exitSP_percentage, 1))
print()
expansionRatio = iohelper.restrictedInput("Enter expansion ratio (chamber-exit for scram, throat-exit for ram): ", 0, True, 500, True)
chamberA = 1

#put the expansion nozzle shit here
print()
exhM, exhP, exhD, exhT, exhV, exhSP, exhST, exhSD = nozzle.runNozzleSolver(gamma, 287, 8314.5, 28.97, expansionRatio, exitM, exitP, exitT, exitD, chamberA)


print()
#after this point we now calculate drag from the intake
def shock1(x):
    return x * math.tan(-(theta1))

def shock2(x):
    return x * math.tan(-(delta1 + theta2))

def shock3(x):
    return x * math.tan(-(delta1 + delta2 + theta3))

def shock4(x):
    return x * math.tan(theta4 - (delta1 + delta2 + delta3))

s4l = 1 / (math.tan(theta4 - (delta1 + delta2 + delta3)))

def surface3(x):
    return (x - s4l) * math.tan(-(delta1 + delta2 + delta3)) + 1

def surface3end(x):
    return surface3(x) - shock3(x)

def surface2(x):
    return (x - surf3xMin) * math.tan(-(delta1 + delta2)) + surface3(surf3xMin)

def surface2end(x):
    return surface2(x) - shock2(x)

def surface1(x):
    return (x - surf2xMin) * math.tan(-(delta1)) + surface2(surf2xMin)

def surface1end(x):
    return surface1(x) - shock1(x)

xMin = -65.0
xMax = 5.0
xPos = np.arange(xMin,xMax,0.1)

surf3xMin = fsolve(surface3end, [0, 0])
surf3xMax = s4l
surf3xRange = np.linspace(surf3xMin, surf3xMax, num=100)

surf2xMin = fsolve(surface2end, [0, 0])
surf2xMax = surf3xMin
surf2xRange = np.linspace(surf2xMin, surf2xMax, num=100)

surf1xMin = fsolve(surface1end, [0, 0])
surf1xMax = surf2xMin
surf1xRange = np.linspace(surf1xMin, surf1xMax, num=100)

shock1range = np.linspace(surf1xMin, s4l, num=100)
shock2range = np.linspace(surf2xMin, s4l, num=100)
shock3range = np.linspace(surf3xMin, s4l, num=100)
shock4range = np.linspace(0., s4l, num=100)

#surface area for a 1m slice
def surfaceLength(x1, y1, x2, y2):
    sxr = abs(x1 - x2)
    syr = abs(y1 - y2)
    pythag = sxr**2 + syr**2
    return pythag**(1/2)

F1xm = surf1xMin[0]
F1ymAlmost = surface1(F1xm)
F1ym = F1ymAlmost[0]
F1xh = surf1xMax[0]
F1yhAlmost = surface1(F1xh)
F1yh = F1yhAlmost[0]
print(F1xm, F1ym)
print(F1xh, F1yh)
lengthF1 = surfaceLength(F1xm, F1ym, F1xh, F1yh)
print("Length:", lengthF1)

F2xm = surf2xMin[0]
F2ymAlmost = surface2(F2xm)
F2ym = F2ymAlmost[0]
F2xh = surf2xMax[0]
F2yhAlmost = surface2(F2xh)
F2yh = F2yhAlmost[0]
print(F2xm, F2ym)
print(F2xh, F2yh)
lengthF2 = surfaceLength(F2xm, F2ym, F2xh, F2yh)
print("Length:", lengthF2)

F3xm = surf3xMin[0]
F3ym = surface3(F3xm)
F3xh = surf3xMax
F3yh = surface3(F3xh)
print(F3xm, F3ym)
print(F3xh, F3yh)
lengthF3 = surfaceLength(F3xm, F3ym, F3xh, F3yh)
print("Length:", lengthF3)

#force calculations
print()
print("Force calculations are for a 1m wide strip of aircraft surface")
P1 = rampP1
P2 = rampP2
P3 = rampP3
F1 = (lengthF1 * P1) / 1000
print("Force 1:", F1, "kN")
angleF1 = math.radians(90) - delta1
F2 = (lengthF2 * P2) / 1000
print("Force 2:", F2, "kN")
angleF2 = math.radians(90) - (delta1 + delta2)
F3 = (lengthF3 * P3) / 1000
print("Force 3:", F3, "kN")
angleF3 = math.radians(90) - (delta1 + delta2 + delta3)
L1 = F1 * math.sin(angleF1)
L2 = F2 * math.sin(angleF2)
L3 = F3 * math.sin(angleF3)
D1 = F1 * math.cos(angleF1)
D2 = F2 * math.cos(angleF2)
D3 = F3 * math.cos(angleF3)
Ltotal = L1 + L2 + L3
Dtotal = D1 + D2 + D3
Ftotal = F1 + F2 + F3
print("Total lift:", Ltotal, "kN")
print("Total drag:", Dtotal, "kN")

def ramjetThrust(exitD, exitV, inletD, inletV, exitP, ambientP, exitArea):
    massFlow = inletD * inletV
    newtonianThrust = (massFlow * exitV) - (massFlow * inletV)
    pressureThrust = (exitP - ambientP) * exitArea
    totalThrust = newtonianThrust + pressureThrust
    return totalThrust

inletVel = nozzle.getSoS(gamma, 287, inletT)
thrustN = ramjetThrust(exhD, exhV, inletD, inletVel, exhP, ambientP, expansionRatio)
thrustBeforeDrag = thrustN / 1000
thrustAfterDrag = thrustBeforeDrag - Dtotal
print("Thrust before drag (kN per m2 of combustor cross section):", thrustBeforeDrag)
print("Thrust after drag:", thrustAfterDrag)
print("Thrust and mass flow scale proprtionally with combustor area, dimensions scale with sqrt(10).")
print("I.e. 1m2 = 1000kN, 100m long. 0.1m2 = 100kN, 31.6m long")
print("Thanks guys and please subscribe and hit like!!!")

#finally show plot
fig, ax = plt.subplots()
#ax.plot([xMin, xMax], [0, 0])
ax.plot(shock1range, shock1(shock1range))
ax.plot(shock2range, shock2(shock2range))
ax.plot(shock3range, shock3(shock3range))
ax.plot(shock4range, shock4(shock4range))
ax.plot([0, s4l], [0, 0])
ax.plot([s4l, s4l], [0, 1])
ax.plot(surf3xRange, surface3(surf3xRange))
ax.plot(surf2xRange, surface2(surf2xRange))
ax.plot(surf1xRange, surface1(surf1xRange))
ax.set_aspect('equal')
plt.savefig("intakeGeometry.pdf")
plt.show()

