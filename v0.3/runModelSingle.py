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
maxTemp = 4000
expansionRatio = 20

config = (angle1, angle2, angle3)

def Palt(gamma, M, Q):
    P = (1 / ((gamma / 2) * M**2)) * Q
    altRange = np.linspace(0, 47000, num=47000)
    Prange = [isa.Pisa(x) for x in altRange]
    PaltDict = dict(zip(altRange, Prange))
    estAlt, estP = min(PaltDict.items(), key=lambda x: abs(P - x[1]))
    return estAlt

estAlt = Palt(gammaAir, M0, Q0)
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
intakePass, conds, thetas = solve.solveIntake(cond0, config, perfTup)
cond1 = conds[0]
cond2 = conds[1]
cond3 = conds[2]
cond4 = conds[3]

#Rayleigh flow combustion
print()
cond5, q = solve.basicHeating(cond4, perfTup, maxTemp)
print("Heat addition (J/kg):", q)
solve.printCond("Post-combustion (5):", cond5)

#Diverging nozzle
print()
cond6 = solve.shitQuasiDivNozzle(cond5, perfTup, expansionRatio)
solve.printCond("Nozzle exit (6):", cond6)

#TODO Performance (thrust, Isp, drag, yada)
