import math
import numpy as np
import formulaegg as egg

R = 8.314463
gamiH2 = 1.41
gamiO2 = 1.40
gamiH2O = 1.33
molH2 = 0.002
molO2 = 0.032
molH2O = 0.018
RsH2 = R / molH2
RsO2 = R / molO2
RsH2O = R / molH2O
CpiH2 = (RsH2 / (gamiH2 - 1)) + RsH2
CpiO2 = (RsO2 / (gamiO2 - 1)) + RsO2
CpiH2O = (RsH2O / (gamiH2O - 1)) + RsH2O
LHV = 119960000
stoich = 8
mixture = 4.5
Rs0 = (RsH2 + (RsO2 * mixture)) / (mixture + 1)
deltaST = 5
tempLimit = 4000
combustionEfficiency = 0.75


def solveIteration(condIn, deltaST):
    itIn = condIn[0]
    Min = condIn[1]
    Pin = condIn[2]
    Tin = condIn[3]
    Din = condIn[4]
    SPin = condIn[5]
    STin = condIn[6]
    SDin = condIn[7]
    nH2in = condIn[8]
    nO2in = condIn[9]
    nH2Oin = condIn[10]
    gamH2in = egg.gamT(gamiH2, Tin)
    gamO2in = egg.gamT(gamiO2, Tin)
    gamH2Oin = egg.gamT(gamiH2O, Tin)
    gamIn = ((gamH2in*nH2in)+(gamO2in*nO2in)+(gamH2Oin*nH2Oin)) / (nH2in+nO2in+nH2Oin)
    print("Iteration =", itIn)
    print("gamma =", gamIn)
    CpH2in = egg.CpT(gamiH2, CpiH2, Tin)
    CpO2in = egg.CpT(gamiO2, CpiO2, Tin)
    CpH2Oin = egg.CpT(gamiH2O, CpiH2O, Tin)
    CpIn = ((CpH2in*nH2in)+(CpO2in*nO2in)+(CpH2Oin*nH2Oin)) / (nH2in+nO2in+nH2Oin)
    print("Cp =", CpIn)
    STout = STin + deltaST
    H2burn = ((deltaST * CpIn) / LHV) * combustionEfficiency
    nH2out = nH2in - H2burn
    nO2out = nO2in - (stoich * H2burn)
    nH2Oout = nH2Oin + (H2burn * (stoich + 1))
    print("H2, O2, H2O =", nH2out, nO2out, nH2Oout)
    ST_STchin = egg.idealST_STch(gamIn, Min)
    print("ST_STchin =", ST_STchin)
    STchin = (1 / ST_STchin) * STin
    print("ST in, out, choked =", STin, STout, STchin)
    if STout > STchin:
        condOut = (itIn, Min, Pin, Tin, Din, SPin, STin, SDin, nH2in, nO2in, nH2Oin, False)
        print("Flow is choked")
    else:
        ST_STchout = STout / STchin
        Mmmx = Min * 2
        if Mmmx <= 1:
            Mmax = Mmmx
        else:
            Mmax = 1
        Mrange = np.linspace(Min, Mmax, num=1000)
        STratio = [egg.idealST_STch(gamIn, x) for x in Mrange]
        MSTdict = dict(zip(Mrange, STratio))
        Mout, unused = min(MSTdict.items(), key=lambda x:abs(ST_STchout - x[1]))
        print("Mout, STratio =", Mout, unused)
        SP_SPchin = egg.idealSP_SPch(gamIn, Min)
        P_Pchin = egg.idealP_Pch(gamIn, Min)
        D_Dchin = egg.idealD_Dch(gamIn, Min)
        T_Tchin = egg.idealT_Tch(gamIn, Min)
        SPchin = (1 / SP_SPchin) * SPin
        Pchin = (1 / P_Pchin) * Pin
        Dchin = (1 / D_Dchin) * Din
        Tchin = (1 / T_Tchin) * Tin
        SPout = egg.idealSP_SPch(gamIn, Mout) * SPchin
        Pout = egg.idealP_Pch(gamIn, Mout) * Pchin
        Dout = egg.idealD_Dch(gamIn, Mout) * Dchin
        Tout = egg.idealT_Tch(gamIn, Mout) * Tchin
        SDout = egg.idealSD_D(gamIn, Mout) * Din
        itOut = itIn + 1
        if (nH2out >= 0) and (nO2out >= 0):
            condOut = (itOut, Mout, Pout, Tout, Dout, SPout, STout, SDout, nH2out, nO2out, nH2Oout, True)
            print("Flow is NOT choked")
        else:
            condOut = (itOut, Min, Pin, Tin, Din, SPin, STin, SDin, nH2in, nO2in, nH2Oin, False)
            print("Combustion complete")
    print("Mout =", condOut[1])
    return condOut

M0 = 0.15
P0 = 101325 * 100
T0 = 500
D0 = P0 / (Rs0 * T0)
gamH2in = egg.gamT(gamiH2, T0)
gamO2in = egg.gamT(gamiO2, T0)
gam0 = (gamH2in + (gamO2in * mixture)) / (mixture + 1)
SP0 = egg.idealSP_P(gam0, M0) * P0
ST0 = egg.idealST_T(gam0, M0) * T0
SD0 = egg.idealSD_D(gam0, M0) * D0
fuel = 1 / (mixture + 1)
oxy = mixture / (mixture + 1)
cond0 = (0, M0, P0, T0, D0, SP0, ST0, SD0, fuel, oxy, 0, True)
condIn = cond0
condMid = condIn
conds = []

while True:
    print()
    condMid = solveIteration(condIn, deltaST)
    print("Temp =", condMid[3])
    if condMid[11] == True:
        condIn = condMid
        conds.append(condMid)
    elif condMid[11] == False:
        conds.append(condIn)
        break

print()
condsLimited = []
for cond in conds:
    if cond[3] <= tempLimit:
        print("It, temp, pass =", cond[3], cond[0])
        condsLimited.append(cond)
    else:
        print("It, temp, fail =", cond[3], cond[0])

condOut = condsLimited[-1]
    
print()
print("FINAL CONDITION")
print("It =", condOut[0])
print("Mout =", condOut[1])
print("Pout =", float(condOut[2] / 101325), "atm")
print("Tout =", condOut[3])
print("Dout =", condOut[4])
print("SPout =", condOut[5])
print("STout =", condOut[6])
print("SDout =", condOut[7])
print("H2, O2, H2O =", condOut[8], condOut[9], condOut[10])
gamH2out = egg.gamT(gamiH2, condOut[3])
gamO2out = egg.gamT(gamiO2, condOut[3])
gamH2Oout = egg.gamT(gamiH2O, condOut[3])
gamOut = ((gamH2out*condOut[8])+(gamO2out*condOut[9])+(gamH2Oout*condOut[10])) / (condOut[8] + condOut[9] + condOut[10])
print("gamma =", gamOut)
RsOut = ((RsH2*condOut[8])+(RsO2*condOut[9])+(RsH2O*condOut[10])) / (condOut[8] + condOut[9] + condOut[10])
print("Rs =", RsOut)
SoSout = math.sqrt(RsOut * condOut[3] * gamOut)
print("SoS =", SoSout)
Vout = condOut[1] * SoSout
print("Vout =", Vout)
Cpout = (RsOut / (gamOut - 1)) + RsOut
print("Cpout =", Cpout)
Vmax = math.sqrt(2 * Cpout * condOut[6])
print("Vmax =", Vmax)

print()
print("DE LAVAL NOZZLE")
expansionRatio = 100



    
    
