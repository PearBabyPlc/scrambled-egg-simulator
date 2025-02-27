#absolute mess, horrible code efficiency, but it gets the job done

import math
import numpy as np
import buzzerrookie_isa as isa
import kyleniemeyer_gasdynamics as kyle
import matplotlib.pyplot as plt
import formulaegg as egg
import itertools
import nozzle

### DEFINE TEST CONDITIONS ###
Mlo = 4
Mhi = 15 #if step = 1, it'll only go up to Mhi-1, keep in mind
step = 1
Q = 30000
gamma = 1.4
R = 287
Cp = 1005
chamberA = 1
expansionRatio = 15
temperatureLimit = 4000
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
    Mrange = np.round(np.arange(Mlo,Mhi,step), 2)
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
    Mout = kyle.obliqueMach(gamma, Min, theta, delta)
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
    elif detached <= delta:
        #theta = math.radians(90)
        #Mout, Tout, Pout, Dout, SPout = solveNormalShock(gamma, Min, Tin, Pin, Din, SPin)
        proceed = False
        return proceed, 0, 0, 0, 0, 0, 0
    else:
        return False, 0, 0, 0, 0, 0, 0

def solveConfig(gamma, rampIteration, ambM, ambT, ambP, ambD, ambSP):
    deg1 = rampIteration[0]
    deg2 = rampIteration[1]
    deg3 = rampIteration[2]
    deg4 = deg1 + deg2 + deg3
    delta1 = math.radians(deg1)
    delta2 = math.radians(deg2)
    delta3 = math.radians(deg3)
    delta4 = math.radians(deg4)
    proceed1, theta1, M1, T1, P1, D1, SP1 = solveShock(gamma, delta1, ambM, ambT, ambP, ambD, ambSP)
    if proceed1 == True:
        proceed2, theta2, M2, T2, P2, D2, SP2 = solveShock(gamma, delta2, M1, T1, P1, D1, SP1)
        if proceed2 == True:
            proceed3, theta3, M3, T3, P3, D3, SP3 = solveShock(gamma, delta3, M2, T2, P2, D2, SP2)
            if proceed3 == True:
                proceed4, theta4, M4, T4, P4, D4, SP4 = solveShock(gamma, delta4, M3, T3, P3, D3, SP3)
                return theta4, M4, T4, P4, D4, SP4
            else:
                return (0, 0, 0, 0, 0, 0)
        else:
            return (0, 0, 0, 0, 0, 0)
    else:
        return (0, 0, 0, 0, 0, 0)

nozzle.initNozzle()
    
#for Mach in Mrange:
def getMaxHeating(inletM, inletT):
    inletT_ST = (1 + ((gamma - 1) / 2) * inletM**2)**(-1)
    inletST = inletT / inletT_ST
    chokedRayleighFactor = egg.rayleighFunc(1, gamma)
    inletST_chokedST = egg.rayleighFunc(inletM, gamma) / chokedRayleighFactor
    chokedST = (1 / inletST_chokedST) * inletST
    maxHeating = (chokedST - inletST) * Cp
    return chokedST, maxHeating
    #get maximum heat addition before choking

def SP_chokedSP(M, gamma):
    return ((gamma + 1) / (1 + gamma * M**2)) * ((2 / (gamma + 1)) * (1 + ((gamma - 1) / 2) * M**2))**(gamma / (gamma - 1))

def scramjetCombustion(inletM, inletT, inletP, inletD, q):
    inletT_ST = (1 + ((gamma - 1) / 2) * inletM**2)**(-1)
    inletST = inletT / inletT_ST
    exitST = (q / Cp) + inletST
    chokedRayleighFactor = egg.rayleighFunc(1, gamma)
    inletST_chokedST = egg.rayleighFunc(inletM, gamma) / chokedRayleighFactor
    exitST_chokedST = (exitST / inletST) * inletST_chokedST
    chokedST = (1 / exitST_chokedST) * exitST
    exitRF = exitST_chokedST * chokedRayleighFactor
    exitM_subsonic = int()
    exitM_supersonic = int()
    lookupRF_subsonic = int()
    lookupRF_supersonic = int()
    exitM_subsonic, lookupRF_subsonic, exitM_supersonic, lookupRF_supersonic = egg.getMachFromRF(exitRF, gamma)
    subsonicError = abs(exitRF - lookupRF_subsonic)
    supersonicError = abs(exitRF - lookupRF_supersonic)
    #print("Subsonic Rayleigh factor (M, RF, error):", exitM_subsonic, lookupRF_subsonic, subsonicError)
    #print("Supersonic Rayleigh factor (M, RF, error):", exitM_supersonic, lookupRF_supersonic, supersonicError)
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
    return (exitM, exitT, exitSP_inletSP, exitP, exitD, exitSOS, exitV, chokedST, chokedT, chokedP, chokedD, chokedSP)

def ramjetThrust(exitD, exitV, inletD, inletV, exitP, ambientP, exitArea):
    massFlow = inletD * inletV
    newtonianThrust = (massFlow * exitV) - (massFlow * inletV)
    pressureThrust = (exitP - ambientP) * exitArea
    totalThrust = newtonianThrust + pressureThrust
    return totalThrust

def performance(inletD, inletV, inletM, inletT, thrust):
    maxChokedST, maxHeating = getMaxHeating(inletM, inletT)
    maxHydrogenPerKgAir = maxHeating / 120000000
    massFlow = inletD * inletV
    maxHydrogen = maxHydrogenPerKgAir * massFlow
    effectiveExhaustV = thrust / maxHydrogen
    Isp = effectiveExhaustV / 9.81
    return massFlow, maxHydrogen, Isp

def solveThrust(inletM, inletT, inletP, inletD, inletSP, inletST, ambD, ambV, ambP, expansionRatio, temperatureLimit):
    maxChokedST, maxHeatingFull = getMaxHeating(inletM, inletT)
    maxHeating = maxHeatingFull * 0.99
    quarter = maxHeating * (1 / 4)
    half = maxHeating * (1 / 2)
    threeQuarter = maxHeating * (3 / 4)
    quarterOutlet = scramjetCombustion(inletM, inletT, inletP, inletD, quarter)
    halfOutlet = scramjetCombustion(inletM, inletT, inletP, inletD, half)
    threeQuOutlet = scramjetCombustion(inletM, inletT, inletP, inletD, threeQuarter)
    maxOutlet = scramjetCombustion(inletM, inletT, inletP, inletD, maxHeating)
    minOutlet = scramjetCombustion(inletM, inletT, inletP, inletD, 0)
    quarterM = float(quarterOutlet[0])
    halfM = float(halfOutlet[0])
    threeQuM = float(threeQuOutlet[0])
    maxM = float(maxOutlet[0])
    minM = float(minOutlet[0])
    quarterExhaust = nozzle.runNozzleSolver(gamma, 287, 8314.5, 28.97, expansionRatio, quarterM, quarterOutlet[3], quarterOutlet[1], quarterOutlet[4], chamberA)
    halfExhaust = nozzle.runNozzleSolver(gamma, 287, 8314.5, 28.97, expansionRatio, halfM, halfOutlet[3], halfOutlet[1], halfOutlet[4], chamberA)
    threeQuExhaust = nozzle.runNozzleSolver(gamma, 287, 8314.5, 28.97, expansionRatio, threeQuM, threeQuOutlet[3], threeQuOutlet[1], threeQuOutlet[4], chamberA)
    maxExhaust = nozzle.runNozzleSolver(gamma, 287, 8314.5, 28.97, expansionRatio, maxM, maxOutlet[3], maxOutlet[1], maxOutlet[4], chamberA)
    minExhaust = nozzle.runNozzleSolver(gamma, 287, 8314.5, 28.97, expansionRatio, minM, minOutlet[3], minOutlet[1], minOutlet[4], chamberA)
    quarterHeatingThrust = ramjetThrust(quarterExhaust[2], quarterExhaust[4], ambD, ambV, quarterExhaust[1], ambP, expansionRatio)
    halfHeatingThrust = ramjetThrust(halfExhaust[2], halfExhaust[4], ambD, ambV, halfExhaust[1], ambP, expansionRatio)
    threeQuarterHeatingThrust = ramjetThrust(threeQuExhaust[2], threeQuExhaust[4], ambD, ambV, threeQuExhaust[1], ambP, expansionRatio)
    maxHeatingThrust = ramjetThrust(maxExhaust[2], maxExhaust[4], ambD, ambV, maxExhaust[1], ambP, expansionRatio)
    minHeatingThrust = ramjetThrust(minExhaust[2], minExhaust[4], ambD, ambV, minExhaust[1], ambP, expansionRatio)
    temps = (quarterOutlet[1], halfOutlet[1], threeQuOutlet[1], maxOutlet[1], minOutlet[1])
    return (quarterHeatingThrust, halfHeatingThrust, threeQuarterHeatingThrust, maxHeatingThrust, minHeatingThrust), temps

def solvePerformance():
    return drag, thrust, excessThrust, fuelBurn, specificImpulse, exhaustV

def debugPrint(debugThis):
    print("(Intake solver output for debug)")
    debugTheta = math.degrees(debugThis[0])
    debugM = debugThis[1]
    debugT = debugThis[2]
    debugP = debugThis[3]
    debugD = debugThis[4]
    debugSP = debugThis[5]
    stringDebug = str("Theta (deg): " + str(round(debugTheta, 1)) + ", Mach: " + str(round(debugM, 3)) + ", Temp (K): " + str(round(debugT, 1)) + ", Pres (Pa): " + str(round(debugP, 1)) + ", Dens (kg/m3): " + str(round(debugD, 5)) + ", Stag P (Pa): " + str(round(debugSP, 1)))
    print(stringDebug)

configsList = []
machsList = []

def solveMachRange_forConfig(config):
    for M in Mrange:
        alt, ambT, ambP, ambD, ambSoS, ambV, ambST, ambSP = ambient_from_MQ(M, Q, gamma)
        configAtM = solveConfig(gamma, config, M, ambT, ambP, ambD, ambSP)
        print("----------------------------------------------------------------------------------------------------")
        print("Config:", config)
        print("Mach:", M)
        print("==========INTAKE==========")
        if configAtM[1] <= 1.0:
            debugPrint(configAtM)
            print("FAIL (intake subsonic at inlet)")
        elif (configAtM[1] > 1.0) and (configAtM[1] < M):
            debugPrint(configAtM)
            print("PASS (intake supersonic at inlet)")
            try: 
                inletM = float(configAtM[1])
                inletT = float(configAtM[2])
                inletP = float(configAtM[3])
                inletD = float(configAtM[4])
                inletSP = float(configAtM[5])
                inletST = float(ambST)
                thrusts, temps = solveThrust(inletM, inletT, inletP, inletD, inletSP, inletST, ambD, ambV, ambP, expansionRatio, temperatureLimit)
                quarterkN = thrusts[0] / 1000
                halfkN = thrusts[1] / 1000
                threeQuarterkN = thrusts[2] / 1000
                maximumkN = thrusts[3] / 1000
                thrustFromHeat = thrusts[3] - thrusts[4]
                thrustFromHeatkN = thrustFromHeat / 1000
                minimum = thrusts[4]
                minimumkN = minimum / 1000
                temp0 = temps[4]
                temp1 = temps[0]
                temp2 = temps[1]
                temp3 = temps[2]
                temp4 = temps[3]
                print("==========COMBUSTOR==========")
                string0 = str("0% thrust: " + str(round(minimumkN, 1)) + "kN, " + str(round(temp0, 1)) + "K combustor")
                string1 = str("25% thrust: " + str(round(quarterkN, 1)) + "kN, " + str(round(temp1, 1)) + "K combustor")
                string2 = str("50% thrust: " + str(round(halfkN, 1)) + "kN, " + str(round(temp2, 1)) + "K combustor")
                string3 = str("75% thrust: " + str(round(threeQuarterkN, 1)) + "kN, " + str(round(temp3, 1)) + "K combustor")
                string4 = str("100% thrust: " + str(round(maximumkN, 1)) + "kN, " + str(round(temp4, 1)) + "K combustor")
                print(string0)
                print(string1)
                print(string2)
                print(string3)
                print(string4)
                print("Max thrust from heat addition (kN)", round(thrustFromHeatkN, 1))
                inletV = (egg.SoS(gamma, 287, inletT)) * inletM
                massFlow, maxHydrogen, IspLo = performance(inletD, inletV, inletM, inletT, thrustFromHeat)
                unusedA, unusedB, IspHi = performance(inletD, inletV, inletM, inletT, thrusts[3])
                print("Max hydrogen flow (kg/s):", round(maxHydrogen, 3))
                print("Inlet mass flow (kg/m2/s):", round(massFlow, 3))
                print("Lower Isp (s):", round(IspLo, 1))
                print("Higher Isp (s):", round(IspHi, 1))
                if temp1 <= temperatureLimit:
                    print("PASS (combustor within temperature limit at 25%)")
                    configAnalysis = [float(M), config, float(IspLo), float(quarterkN)]
                    configsList.append(configAnalysis)
                    machAnalysis = [config, float(M), float(IspLo), float(quarterkN)]
                    machsList.append(machAnalysis)
                elif temp1 > temperatureLimit:
                    print("FAIL (combustor exceeds temperature limit even at 25%)")
                else:
                    print("ERROR (combustor temperature)")
            except:
                print("ERROR (combustor)")
            #calcualte geometry and performance
        elif configAtM[0] < 0:
            debugPrint(configAtM)
            print("ERROR (intake)")
        else:
            debugPrint(configAtM)
            print("ERROR (intake)")
        print("----------------------------------------------------------------------------------------------------")
        print()

for config in ramp123range:
    solveMachRange_forConfig(config)

configsList.sort()
print("Successful configs, listed in Mach order, with Isp and 25% thrust:")
it = 0
for x in configsList:
    it += 1
    print(it, x)

print()
print("Successful configs in order, with Mach, Isp and 25% thrust:")
it = 0
for x in machsList:
    it += 1
    print(it, x)


#i guess it works???!!

    
    

### PLOT AT THE END
fig, (ax1, ax2, ax3) = plt.subplots(3)
ax1.plot(Mrange, altRange, color='k')
ax1.plot(Mrange, Prange, color='b')
ax2.plot(Mrange, Trange, color='r')
ax2.plot(Mrange, Drange, color='y')
ax3.plot(Mrange, degDetachmentRange)
plt.savefig("machQ_conditions.pdf")
plt.show()
