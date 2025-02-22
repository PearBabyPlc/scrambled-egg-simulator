import math
import numpy as np
import inputhelper as io

#Prandlt-Meyer expansion fans are isentropic, get all other flow parameters from that shit

def prandltMeyerAngle(gamma, M):
    PM = math.sqrt((gamma + 1) / (gamma - 1)) * math.atan(math.sqrt(((gamma - 1) / (gamma + 1)) * (M**2 - 1))) - math.atan(math.sqrt(M**2 - 1))
    return PM

def prandltMeyerMach(PM, gamma):
    rangeM = list(np.linspace(1.1, 30.0, num=10000))
    rangeNP = [prandltMeyerAngle(gamma, x) for x in rangeM]
    prandly = dict(zip(rangeM, rangeNP))
    approxM, approxPM = min(prandly.items(), key=lambda x: abs(PM - x[1]))
    error = abs(approxPM - PM)
    return approxM, approxPM, error

def getPrandltMeyerMach(gamma, preMach, degE):
    radE = math.radians(degE)
    prePMrad = prandltMeyerAngle(gamma, preMach)
    prePMdeg = math.degrees(prePMrad)
    postPMrad = prePMrad + radE
    postPMdeg = math.degrees(postPMrad)
    postMach, approxPM, error = prandltMeyerMach(postPMrad, gamma)
    return prePMdeg, postPMdeg, postMach, approxPM, error
    
def test():
    gamma = io.restrictedInput("Enter gamma: ", 0, True, 10, False)
    preMach = io.restrictedInput("Enter initial Mach: ", 1, True, 30, True)
    degE = io.restrictedInput("Enter expansion angle (deg): ", 0, True, 90, True)
    radE = math.radians(degE)
    prePMrad = prandltMeyerAngle(gamma, preMach)
    prePMdeg = math.degrees(prePMrad)
    postPMrad = prePMrad + radE
    postPMdeg = math.degrees(postPMrad)
    postMach, approxPM, error = prandltMeyerMach(postPMrad, gamma)
    print("Initial Prandlt-Meyer angle (deg):", prePMdeg)
    print("Final Prandlt-Meyer angle (deg):", postPMdeg)
    print("Final Mach:", postMach)
    print("Lookup table PM error:", error)

#test()
