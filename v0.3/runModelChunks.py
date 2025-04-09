import math
import itertools
import numpy as np
import matplotlib.pyplot as plt
import geometryDrag as geom
import formulaegg as egg
import buzzerrookie_isa as isa
import solvers as solve
import time
import statistics as stat
import csv

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
outputName = "AoA=7deg"
Mlo = 4
Mhi = 16
Mstep = 1
Qdyn = 40000
expansionRatio = 30
tempLimit = 3800
lengthLimit = 310
IspLimit = 11000
angles1 = (7, 7, 7, 7)
angles2 = (5, 6, 7, 8)
angles3 = (6, 8, 10, 12)

###LEAVE EVERYTHING BELOW THIS ALONE###
print()
scrambledEggString = R""".  /$$$$$$                                                       .
. /$$__  $$                                                      .
.| $$  \__/  /$$$$$$$  /$$$$$$  /$$$$$$  /$$$$$$/$$$$            .
.|  $$$$$$  /$$_____/ /$$__  $$|____  $$| $$_  $$_  $$           .
. \____  $$| $$      | $$  \__/ /$$$$$$$| $$ \ $$ \ $$           .
. /$$  \ $$| $$      | $$      /$$__  $$| $$ | $$ | $$           .
.|  $$$$$$/|  $$$$$$$| $$     |  $$$$$$$| $$ | $$ | $$           .
. \______/  \_______/|__/      \_______/|__/ |__/ |__/           .
. /$$       /$$                 /$$ /$$$$$$$$                    .
.| $$      | $$                | $$| $$_____/                    .
.| $$$$$$$ | $$  /$$$$$$   /$$$$$$$| $$        /$$$$$$   /$$$$$$ .
.| $$__  $$| $$ /$$__  $$ /$$__  $$| $$$$$    /$$__  $$ /$$__  $$.
.| $$  \ $$| $$| $$$$$$$$| $$  | $$| $$__/   | $$  \ $$| $$  \ $$.
.| $$  | $$| $$| $$_____/| $$  | $$| $$      | $$  | $$| $$  | $$.
.| $$$$$$$/| $$|  $$$$$$$|  $$$$$$$| $$$$$$$$|  $$$$$$$|  $$$$$$$.
.|_______/ |__/ \_______/ \_______/|________/ \____  $$ \____  $$.
.                                             /$$  \ $$ /$$  \ $$.
. v0.3 Alpha (Pear Baby Hyperaeronautics)    |  $$$$$$/|  $$$$$$/.
.                                             \______/  \______/ .
"""
print(scrambledEggString)
print()
#setup ranges
ambientRange = solve.initAmbient(perfTup[0], Mlo, Mhi, Mstep, Qdyn)
configL = list(itertools.product(angles1, angles2, angles3))
configS = set(configL)
configs = list(configS)
configsLen = len(configs)
print("Test configs:", configsLen)
Machlen = abs(Mlo - Mhi) / Mstep
print("Test Machs:", Machlen)
totalTests = configsLen * Machlen
print("Total tests:", totalTests)
estimateTotal = totalTests * 0.031
print("Estimated time (s):", estimateTotal)

arrayMach = []
arrayConfig = []
arrayThrust = []
arrayIsp = []
arrayLength = []

tryRamjet = []
exceptionList = []

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
            zP = (cond1[1], cond2[1], cond3[1])
            zL, zD, zL, zH, zR = geom.solveDrag(deltas, thetas, zP)
            testExpansionRatio = expansionRatio
            print("Expansion ratio:", testExpansionRatio)
            cond5, q = solve.betterHeating(cond4, perfTup, tempLimit, qLimit)
            cond6, actualArea = solve.shitQuasiDivNozzle(cond5, perfTup, testExpansionRatio)
            allConds = (cond0, cond1, cond2, cond3, cond4, cond5, cond6)
            thrust, fuelFlow, Isp, lift, drag, length, height, passRamp = solve.performance(allConds, actualArea, deltas, thetas, LHV, q)
            printKNThrust = thrust / 1000
            print("Thrust:", printKNThrust)
            print("Specific impulse:", Isp)
            print("Length:", length)
            if (length <= lengthLimit) and (Isp <= IspLimit) and (Isp >= 0) and (thrust >= 0) and (q <= qLimit):
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
                passSPR = cond4[4] / cond0[4]
                passTmax = cond5[2]
                dynP = Qdyn
                return passMach, dynP, passConfig, passLength, passRamp, passSPR, passTmax, testExpansionRatio, passThrust, passIsp
                #######
            else:
                print("CONFIG FAIL! (intake pass, performance fail)")
                if length > lengthLimit:
                    print("Intake too long")
                elif Isp > IspLimit:
                    print("Suspicious Isp")
                elif thrust < 0:
                    print("No thrust produced")
                elif q > qLimit:
                    print("Heat addition exceeds stoichiometric limit")
                return 0, failConfig, 0, 0, 0, 0, 0, 0, 0, 0
        else:
            print("CONFIG FAIL! (intake fail, performance fail)")
            print("Inlet Mach:", cond5[0])
            tryAsRamjet = (testConfig, cond0[0])
            tryRamjet.append(tryAsRamjet)
            print("Config and M added to ramjet list")
            return 0, failConfig, 0, 0, 0, 0, 0, 0, 0, 0
    except:
        print("CONFIG ERROR!")
        exceptionConfigM = (testConfig, cond0[0])
        exceptionList.append(exceptionConfigM)
        print("Config and M added to exception list")
        return 0, failConfig, 0, 0, 0, 0, 0, 0, 0, 0

totalStart = time.time()
machTimes = []
configTimes = []
maxThrustConfig_atM = []
iterationConfig = int(0)
for x in ambientRange:
    machStart = time.time()
    print()
    print("====================MACH====================")
    testM = x
    configThrIspLen = []
    configThrIspLen.clear()
    for y in configs:
        configStart = time.time()
        print("--------------------Config--------------------")
        iterationConfig += 1
        print("Iteration #", iterationConfig)
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
        passMach, Q, passConfig, passLength, passRamp, passSPR, passTmax, passExpR, passThrust, passIsp = solveConfig(testConfig, cond0)
        passThrIspLen = (passMach, Q, passConfig, passLength, passRamp, passSPR, passTmax, passExpR, passThrust, passIsp)
        configThrIspLen.append(passThrIspLen)
        print("--------------------------------------------------")
        print()
        configEnd = time.time()
        configTime = configEnd - configStart
        configTimes.append(configTime)
    sortedByThrust = sorted(configThrIspLen, key=lambda z : z[8])
    maxThrustConfig = sortedByThrust[-1]
    maxThrustConfig_atM.append(maxThrustConfig)
    print("==================================================")
    machEnd = time.time()
    machTime = machEnd - machStart
    machTimes.append(machTime)

totalEnd = time.time()

saveCSVStr = str(outputName + ".csv")
with open(saveCSVStr, 'w', newline='') as csvfile:
    writer = csv.writer(csvfile, delimiter=' ', quotechar='|', quoting=csv.QUOTE_MINIMAL)
    writer.writerow(['M', 'Q', 'config', 'intakeLen', 'rampLen', 'intakeSPR', 'maxT', 'expansionR', 'thrust', 'Isp'])
    for x in maxThrustConfig_atM:
        configQuote = str("|" + str(x[2]) + "|")
        writer.writerow([x[0], x[1], configQuote, x[3], x[4], x[5], x[6], x[7], x[8], x[9]])

plotM = []
plotThrust = []
plotIsp = []
plotExpR = []
print()
print("====================PLOT====================")
for x in maxThrustConfig_atM:
    plotTup = (x[0], x[8], x[9])
    print()
    print("Mach:", x[0], "| Config:", x[2], "| Thrust:", x[8], "| Isp:", x[9])
    print("Ramp length:", x[5])
    if (plotTup[0] != 0) and (plotTup[1] != 0) and (plotTup[2] != 0):
        plotM.append(x[0])
        plotThrust.append(x[8])
        plotIsp.append(x[9])
        plotExpR.append(x[7])
        print("Added to plot")
    else:
        print("Excluded from plot")
print("==================================================")

print()
print("====================TIMES====================")
totalTime = totalEnd - totalStart
print("Total time:", totalTime)
meanMach = stat.mean(machTimes)
medMach = stat.median(machTimes)
meanConfig = stat.mean(configTimes)
medConfig = stat.median(configTimes)
print("Mach mean:", meanMach)
print("Mach median:", medMach)
print("Config mean:", meanConfig)
print("Config median:", medConfig)
maxMach = max(machTimes)
minMach = min(machTimes)
maxConf = max(configTimes)
minConf = min(configTimes)
print("Mach max min:", maxMach, minMach)
print("Config max min:", maxConf, minConf)
successes = len(configThrIspLen)
print("Config passes:", successes)
successPercent = (successes / totalTests) * 100
print(successPercent, "% passed")

fig, (ax1, ax2, ax3) = plt.subplots(3, 1)
ax1.plot(plotM, plotThrust)
#ax1.plot(np.unique(plotM), np.poly1d(np.polyfit(plotM, plotThrust, 1))(np.unique(plotM))) line of best fit not working
ax1.set_title("Thrust (kN)")
ax1.grid()
ax2.plot(plotM, plotIsp)
#ax2.plot(np.unique(plotM), np.poly1d(np.ployfit(plotM, plotIsp, 1))(np.unique(plotM))) line of best fit not working
ax2.set_title("Specific impulse (s)")
ax2.grid()
ax3.plot(plotM, plotExpR)
ax3.set_title("Expansion ratio")
ax3.grid()
saveFigStr = str(outputName + ".pdf")
plt.savefig("chunks.pdf")
plt.show()
                
                
