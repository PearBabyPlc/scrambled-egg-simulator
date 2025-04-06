import math
import itertools
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
import formulaegg as egg
import buzzerrookie_isa as isa
import solvers as solve
import scipy as sp
import time
import statistics as stat

totalStart = time.time()

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
Mhi = 15
Mstep = 0.05
Q = 45000
expansionRatio = 15
tempLimit = 3800
lengthLimit = 210
angles1 = (4, 5, 6)
angles2 = (3, 3, 3)
angles3 = (5, 5, 5)

#estAlt = egg.Palt(1.4, M, Q)

ambientRange = solve.initAmbient(1.4, Mlo, Mhi, Mstep, Q)
configs = list(itertools.product(angles1, angles2, angles3))
configsLen = len(configs)
print("configsLen =", configsLen)
Machlen = abs(Mlo - Mhi) / Mstep
print("MachLen =", Machlen)
totalTests = configsLen * Machlen
print("Total tests =", totalTests)

Mplot = []
thrustPlot = []
IspPlot = []
IspHeatmap = []
configList = []
qList = []
fuelList = []
timeSuccessList = []

def solveConfig(testConfig, cond0):
    start = time.time()
    print("M =", cond0[0], "| config =", testConfig)
    intakePass, conds, thetas, deltas = solve.solveIntake(cond0, testConfig, perfTup)
    print("Ambient P =", cond0[1])
    cond1 = conds[0]
    cond2 = conds[1]
    cond3 = conds[2]
    cond4 = conds[3]
    fail = (0, 0, 0, 0, 0)
    failB = (0, 0, 0, 0, 0)
    try:
        if intakePass == True:
            cond5, q = solve.basicHeating(cond4, perfTup, tempLimit)
            print("Combustor temp:", cond5[2])
            cond6, actualArea = solve.shitQuasiDivNozzle(cond5, perfTup, expansionRatio)
            allConds = (cond0, cond1, cond2, cond3, cond4, cond5, cond6)
            thrust, fuelFlow, Isp, drag, length, height = solve.performance(allConds, actualArea, deltas, thetas, LHV, q)
            print("Fuel flow:", fuelFlow)
            print("Drag:", drag)
            performance = (thrust, fuelFlow, Isp, drag)
            dimensions = (length, height)
            if (length <= 160) and (Isp <= 11000) and (Isp >= 0) and (thrust >= 0) and (q <= qLimit):
                Mplot.append(cond0[0])
                thrustKN = thrust / 1000
                thrustPlot.append(thrustKN)
                IspPlot.append(Isp)
                IspF = float(Isp)
                IspHeatmap.append(IspF)
                configList.append(testConfig)
                qList.append(q)
                fuelList.append(fuelFlow)
                end = time.time()
                timeSuccess = end - start
                timeSuccessList.append(timeSuccess)
                return performance, dimensions
            else:
                print("Fail (too long)")
                return fail, failB
        else:
            return fail, failB
    except:
        print("something fucked up lol")
        fail = str("Fail")
        failB = str("FAIL")
        return fail, failB

for x in configs:
    testConfig = x
    for y in ambientRange:
        print()
        print("==================================================")
        M0 = y[0]
        amb = y[2]
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
        performance, dimensions = solveConfig(testConfig, cond0)
        print("Thrust:", performance[0])
        print("Fuel flow:", performance[1])
        print("Isp:", performance[2])
        print("Length:", dimensions[0])
        print("==================================================")

totalEnd = time.time()
totalTime = totalEnd - totalStart
print("Total time:", totalTime)
averageMean = stat.mean(timeSuccessList)
averageMedian = stat.median(timeSuccessList)
print("Mean time:", averageMean)
print("Median time:", averageMedian)

heatmapLength = len(IspHeatmap)
ispLength = len(IspPlot)
print("Isp length =", ispLength)
print("Hmap length=", heatmapLength)

iteration = int(-1)
for x in thrustPlot:
    print()
    iteration += 1
    printIt = iteration +1
    print("Iteration num =", printIt)
    print("thrustPlot[]:", x)
    print("iteration   :", thrustPlot[iteration])
    print("Isp Plot:   :", IspPlot[iteration])
    print("Heatmap:    :", IspHeatmap[iteration])

iteration = int(-1)
IspDebug = []
for x in IspPlot:
    iteration += 1
    debugConfig = configList[iteration]
    debugMach = Mplot[iteration]
    debugThrust = thrustPlot[iteration]
    fuelD = fuelList[iteration]
    qD = qList[iteration]
    ispDebugTup = (x, iteration, debugConfig, debugMach, fuelD, qD)
    IspDebug.append(ispDebugTup)

debug_sortedByIsp = sorted(IspDebug, key=lambda spimp : spimp[0])
debug_sortedByMach = sorted(IspDebug, key=lambda smch : smch[3])
print()
print("SORTED BY ISP:")
for x in debug_sortedByIsp:
    printX = float(x[0])
    print("Isp =", printX, "| iteration =", x[1], "| Config =", x[2], "| Mach =", x[3], "| Fuel =", x[4], "| q =", x[5])

print()
print("SORTED BY MACH:")
for x in debug_sortedByMach:
    printX = float(x[0])
    print("Isp =", printX, "| iteration =", x[1], "| Config =", x[2], "| Mach =", x[3], "| Fuel =", x[4], "| q =", x[5])

fig, (ax1, ax2) = plt.subplots(2, 1)
im = ax1.scatter(Mplot, thrustPlot, cmap='plasma', c=IspPlot)
cax = fig.add_axes([0.27, 0.85, 0.5, 0.02])
fig.colorbar(im, cax=cax, orientation='horizontal')
ax1.grid()
ax1.set_title("Thrust (kN), specific impulse heatmap (s)")
bm = ax2.scatter(Mplot, IspPlot, cmap='inferno', c=thrustPlot)
cbx = fig.add_axes([0.27, 0.05, 0.5, 0.02])
fig.colorbar(bm, cax=cbx, orientation='horizontal')
ax2.grid()
ax2.set_title("Specific impulse (s), thrust heatmap (kN)")
plt.savefig("runModelRange.pdf")
plt.show()
    
