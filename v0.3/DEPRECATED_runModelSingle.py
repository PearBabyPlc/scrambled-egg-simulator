import math
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

#test variables
M0 = 10
Q0 = 40000
angle1 = 3
angle2 = 6
angle3 = 10
maxTemp = 3200
expansionRatio = 15

config = (angle1, angle2, angle3)

estAlt = egg.Palt(gammaAir, M0, Q0)
T0, P0, D0 = isa.isa(estAlt)

Rs0 = RsAir
mol0 = molAir
T_ST0 = egg.realT_ST(gammaAir, M0, T0)
ST0 = T0 / T_ST0
SP0 = P0 / egg.realP_SP(gammaAir, T_ST0, T0)
gam0 = egg.realGamma(gammaAir, T0)
Cp0 = egg.realCp(gammaAir, CpAir, T0)
SoS0 = egg.idealSoS(gam0, Rs0, T0)
Vel0 = M0 * SoS0

cond0 = (M0, P0, T0, D0, SP0, ST0, SoS0, Vel0, gam0, Cp0, Rs0, mol0)
perfTup = (gammaAir, CpAir, RsAir, molAir)
steamTUp = (gammaSteam, CpSteam, RsSteam, molSteam)
fuelTup = (gammaH, CpH, RsH, molH)
solve.printCond("Ambient (0):", cond0)
print("Altitude:", estAlt, "metres")

#iIntake oblique shock cascade
print()
intakePass, conds, thetas, deltas = solve.solveIntake(cond0, config, perfTup)
cond1 = conds[0]
cond2 = conds[1]
cond3 = conds[2]
cond4 = conds[3]

qLimit = (120 * 1000000) / 34
#Rayleigh flow combustion
print()
cond5, q = solve.betterHeating(cond4, perfTup, maxTemp, qLimit)
print("Heat addition (J/kg):", q)
solve.printCond("Post-combustion (5):", cond5)

#Diverging nozzle
print()
cond6, actualArea = solve.shitQuasiDivNozzle(cond5, perfTup, expansionRatio)
solve.printCond("Nozzle exit (6):", cond6)

#Performance (thrust, drag, isp)
print()
allConds = (cond0, cond1, cond2, cond3, cond4, cond5, cond6)
thrust, fuelFlow, Isp, lift, drag, length, height, rampLength = solve.performance(allConds, actualArea, deltas, thetas, LHV, q)
print("Thrust:", thrust)
print("Fuel flow:", fuelFlow)
print("Isp:", Isp)
print("Lift:", lift)
print("Total length:", length)
print("Ramp legnth:", rampLength)
print("Intake height:", height)
