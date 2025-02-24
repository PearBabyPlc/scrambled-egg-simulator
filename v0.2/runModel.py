#this version currently generates a constant dynamic pressure altitude path, a big array of ramp angles, and can solve shocks
#the next steps are to add the rest of the model (combustion, expansion, geometry, drag, performance)
#most importantly, also adding an iterator to apply the angles to the whole model
#difficult bit is going to be visualising the outputs - as each set of angles will have a Mach that it performs best at
#intake performance can be quantified by stagnation pressure ratio, overall performance by thrust and specific impulse
#probably going to be some sort of dot plot of the best performance values per Mach number
#then print the 10 best configurations per whole Mach number, find the ones that are closest, and arrange from Mach 4 to 16 probably
#this will be fun bleh

import math
import numpy as np
import buzzerrookie_isa as isa
import kyleniemeyer_gasdynamics as kyle
import matplotlib.pyplot as plt
import formulaegg as egg
import itertools

### DEFINE TEST CONDITIONS ###
Mlo = 1.0
Mhi = 17.0
Q = 30000
gamma = 1.4
R = 287
### 

def P_from_MQ(M, Q, gamma):
    P = (Q / M**2) / (gamma / 2)
    return P

def alt_from_P(P):
    rangeAlt = np.linspace(0, 47000, num=3000)
    rangeP = [isa.Pisa(x) for x in rangeAlt]
    dictAlt = dict(zip(rangeAlt, rangeP))
    estAlt, estP = min(dictAlt.items(), key=lambda x: abs(P - x[1]))
    return estAlt
    
def initialAlt(Mlo, Mhi, Q, gamma):
    Mrange = np.round(np.arange(Mlo,Mhi,0.1), 2)
    Prange = [P_from_MQ(x, Q, gamma) for x in Mrange]
    altRange = [alt_from_P(x) for x in Prange]
    return altRange, Mrange

def initialConditions(altRange):
    Prange = [isa.Pisa(x) for x in altRange]
    Trange = [isa.Tisa(x) for x in altRange]
    Drange = [isa.Disa(x) for x in altRange]
    return Prange, Trange, Drange

altRange, Mrange = initialAlt(Mlo, Mhi, Q, gamma)
Prange, Trange, Drange = initialConditions(altRange)

def ambient_from_MQ(M, Q, gamma):
    isenP = P_from_MQ(M, Q, gamma)
    alt = alt_from_P(isenP)
    ambT, ambP, ambD = isa.isa(alt)
    ambSoS = egg.SoS(gamma, R, ambT)
    ambV = ambSoS * M
    ambST = (1 / (egg.T_sT(gamma, M))) * ambT
    ambSP = (1 / (egg.P_sP(gamma, M))) * ambP
    return alt, ambT, ambP, ambD, ambSoS, ambV, ambST, ambSP

alt, ambT, ambP, ambD, ambSoS, ambV, ambST, ambSP = ambient_from_MQ(10, Q, 1.4)
print(alt)
print(ambT)
print(ambP)
print(ambD)
print(ambSoS)
print(ambV)
print(ambST)
print(ambSP)

### DEF TEST GEOMETRY ###
# something something detachment angle

def detachmentAngle(M, gamma):
    degDetachment = math.degrees(egg.radDetachment(M, gamma))
    return degDetachment

degDetachmentRange = [detachmentAngle(x, gamma) for x in Mrange]

#simple for now
ramp1range = (2, 3, 4, 5)
ramp2range = (4, 6, 8, 10)
ramp3range = (10, 14, 18, 22)
rampCount = 3
ramp123range = list(itertools.product(ramp1range, ramp2range, ramp3range))
temporary = list((int(j) for i in ramp123range for j in i))
resultemp = len(temporary)
rampnum = resultemp / rampCount
print("Number of ramp configurations to be tested: " + str(rampnum))

#delta = math.radians(deflectionAngleDegrees)
#STin = STout, stagnation temp remains constant

def solveObliqueShock(gamma, delta, Min, Tin, Pin, Din, SPin):
    theta = kyle.obliqueShockTheta(Min, gamma, delta)
    Mout = egg.obliqueMout(gamma, Min, theta, delta)
    Tout = Tin * egg.obliqueTout_Tin(gamma, Min, theta)
    Pout = Pin * egg.obliquePout_Pin(gamma, Min, theta)
    Dout = Din * egg.obliqueDout_Din(gamma, Min, theta)
    SPout = SPin * egg.obliqueSPout_SPin(gamma, Min, theta)
    return theta, Mout, Tout, Pout, Dout, SPout

def solveNormalShock(gamma, Min, Tin, Pin, Din, SPin):
    Mout = egg.normalMout(gamma, Min)
    Tout = Tin * egg.normalTout_Tin(gamma, Min)
    Pout = Pin * egg.normalPout_Pin(gamma, Min)
    Dout = Din * egg.normalDout_Din(gamma, Min)
    SPout = SPin * egg.normalSPout_SPin(gamma, Min)
    return Mout, Tout, Pout, Dout, SPout

def solveShock(gamma, delta, Min, Tin, Pin, Din, SPin):
    detached = egg.radDetachment(Min, gamma)
    if detached > delta:
        theta, Mout, Tout, Pout, Dout, SPout = solveObliqueShock(gamma, delta, Min, Tin, Pin, Din, SPin)
        proceed = True
        return proceed, theta, Mout, Tout, Pout, Dout, SPout
    elif detached < delta:
        theta = math.radians(90)
        Mout, Tout, Pout, Dout, SPout = solveNormalShock(gamma, Min, Tin, Pin, Din, SPin)
        proceed = False
        return proceed, theta, Mout, Tout, Pout, Dout, SPout

def solveConfig(gamma, rampIteration, ambM, ambT, ambP, ambD, ambSP):
    deg1 = rampIteration[0]
    deg2 = rampIteration[1]
    deg3 = rampIteration[2]
    deg4 = deg1 + deg2 + deg3
    delta1 = math.radians(deg1)
    delta2 = math.radians(deg2)
    delta3 = math.radians(deg3)
    delta4 = math.radians(deg4)
    while True:
        proceed1, theta1, M1, T1, P1, D1, SP1 = solveShock(gamma, delta1, ambM, ambT, ambP, ambD, ambSP)
        if proceed1 == False:
            rampNum = 1
            return theta1, M1, T1, P1, D1, SP1, rampNum
            break
        elif proceed1 == True:
            proceed2, theta2, M2, T2, P2, D2, SP2 = solveShock(gamma, delta2, M1, T1, P1, D1, SP1)
            if proceed2 == False:
                rampNum = 2
                return theta2, M2, T2, P2, D2, SP2, rampNum
                break
            elif proceed2 == True:
                proceed3, theta3, M3, T3, P3, D3, SP3 = solveShock(gamma, delta3, M2, T2, P2, D2, SP2)
                if proceed3 == False:
                    rampNum = 3
                    return theta3, M3, T3, P3, D3, SP3, rampNum
                    break
                elif proceed3 == True:
                    proceed4, theta4, M4, T4, P4, D4, SP4 = solveShock(gamma, delta4, M3, T3, P3, D3, SP3)
                    if proceed4 == False:
                        rampNum = 4
                        return theta4, M4, T4, P4, D4, SP4, rampNum
                        break
                    elif proceed4 == True:
                        rampNum = 5
                        return theta4, M4, T4, P4, D4, SP4, rampNum

### PLOT AT THE END
fig, (ax1, ax2, ax3) = plt.subplots(3)
ax1.plot(Mrange, altRange, color='k')
ax1.plot(Mrange, Prange, color='b')
ax2.plot(Mrange, Trange, color='r')
ax2.plot(Mrange, Drange, color='y')
ax3.plot(Mrange, degDetachmentRange)
plt.savefig("machQ_conditions.pdf")
plt.show()
