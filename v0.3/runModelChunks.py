import math
import itertools
import numpy as np
import matplotlib.pyplot as plt
import formulaegg as egg
import buzzerrookie_isa as isa
import solvers as solve

#constants
RsAir = 287
molAir = 28.97
gammaAir = 1.4
CpAir = 1005
RsSteam = 462
molSteam = 18
gammaSteam = 1.33
CpSteam = 1996
RsH = None
molH = None
gammaH = None
CpH = None
LHV = 120 * 1000000
qLimit = LHV / 34
perfTup = (gammaAir, CpAir, RsAir, molAir)
steamTUp = (gammaSteam, CpSteam, RsSteam, molSteam)
fuelTup = (gammaH, CpH, RsH, molH)

#test variables
Mlo = 4
Mhi = 16
Mstep = 0.05
Q = 45000
expansionRatio = 15
tempLimit = 3800
lengthLimit = 210
angles1 = (2, 3, 4, 5, 6)
angles2 = (4, 6, 8, 10, 12)
angles3 = (6, 9, 12, 15, 18)

#setup ranges
ambientRange = solve.initAmbient(perfTup[0], Mlo, Mhi, Mstep, Q)
configs = list(itertools.product(angles1, angles2, angles3))
configsLen = len(configs)
print("configsLen =", configsLen)
Machlen = abs(Mlo - Mhi) / Mstep
print("MachLen =", Machlen)
totalTests = configsLen * Machlen
print("Total tests =", totalTests)

arrayMach = []
arrayConfig = []
arrayThrust = []
arrayIsp = []
arrayLength = []

def solveConfig(testConfig, cond0):
    print("M =", cond0[0], "| config =", testConfig)
    intakePass, conds, thetas, deltas = solve.solveIntake(cond0, testConfig, perfTup)
    cond1 = conds[0]
    cond2 = conds[1]
    cond3 = conds[2]
    cond4 = conds[3]
    failConfig = (0, 0, 0)
    try:
        if intakePass == True:
            cond5, q = solve.basicHeating(cond4, perfTup, tempLimit)
            cond6, actualArea = solve.shitQuasiDivNozzle(cond5, perfTup, expansionRatio)
            allConds = (cond0, cond1, cond2, cond3, cond4, cond5, cond6)
            thrust, fuelFlow, Isp, drag, length, height = solve.performance(allConds, actualArea, deltas, thetas, LHV, q)
            if (length <= lengthLimit) and (Isp <= 11000) and (Isp >= 0) and (thrust >= 0) and (q <= qLimit):
                passMach = cond0[0]
                passConfig = testConfig
                passThrust = thrust / 1000
                passIsp = Isp
                passLength = length
                arrayMach.append(passMach)
                arrayConfig.append(passConfig)
                arrayThrust.append(passThrust)
                arrayIsp.append(passIsp)
                arrayLength.append(passLength)
                print("CONFIG PASS! (intake pass, performance pass)")
                return passMach, passConfig, passThrust, passIsp, passLength
            else:
                print("CONFIG FAIL! (intake pass, performance fail)")
                return 0, failConfig, 0, 0, 0
        else:
            print("CONFIG FAIL! (intake fail, performance fail)")
            return 0, failConfig, 0, 0, 0
    except:
        print("CONFIG ERROR!")
        return 0, failConfig, 0, 0, 0

maxThrustConfig_atM = []
for x in ambientRange:
    print()
    print("====================MACH====================")
    testM = x
    configThrIspLen = []
    configThrIspLen.clear()
    for y in configs:
        print("--------------------Config--------------------")
        testConfig = y
        M0 = x[0]
        amb = x[2]
        P0 = amb[1]
        T0 = amb[0]
        D0 = amb[2]
        T_ST0 = egg.realT_ST(gammaAir, M0, T0)
        ST0 = T0 / T_ST0
        SP0 = P0 / egg.realP_SP(gammaAir, T_ST0, T0)
        gam0 = egg.realGamma(gammaAir, T0)
        Cp0 = egg.realCp(gammaAir, CpAir, T0)
        Rs0 = RsAir
        mol0 = molAir
        SoS0 = egg.idealSoS(gam0, Rs0, T0)
        Vel0 = M0 * SoS0
        cond0 = (M0, P0, T0, D0, SP0, ST0, SoS0, Vel0, gam0, Cp0, Rs0, mol0)
        passMach, passConfig, passThrust, passIsp, passLength = solveConfig(testConfig, cond0)
        passThrIspLen = (passConfig, passThrust, passIsp, passLength, passMach)
        configThrIspLen.append(passThrIspLen)
        print("--------------------------------------------------")
    sortedByThrust = sorted(configThrIspLen, key=lambda z : z[1])
    maxThrustConfig = sortedByThrust[-1]
    maxThrustConfig_atM.append(maxThrustConfig)
    print("==================================================")

plotM = []
plotThrust = []
plotIsp = []
print()
for x in maxThrustConfig_atM:
    plotTup = (x[4], x[1], x[2])
    print()
    print("Mach:", x[4], "| Config:", x[0], "| Thrust:", x[1], "| Isp:", x[2], "| Length:", x[3])
    if (plotTup[0] != 0) and (plotTup[1] != 0) and (plotTup[2] != 0):
        plotM.append(x[4])
        plotThrust.append(x[1])
        plotIsp.append(x[2])
        print("Added to plot")
    else:
        print("Excluded from plot")
    
fig, (ax1, ax2) = plt.subplots(2, 1)
ax1.plot(plotM, plotThrust)
ax1.set_title("Thrust (kN)")
ax2.plot(plotM, plotIsp)
ax2.set_title("Specific impulse (s)")
plt.savefig("chunks.pdf")
plt.show()
                
                
