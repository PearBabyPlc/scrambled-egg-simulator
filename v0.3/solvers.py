import math
import numpy as np
import buzzerrookie_isa as isa
import formulaegg as egg
import geometryDrag as geom

g = 9.81

def printCond(condString, cond):
    print(condString)
    Mstr = str("Mach: " + str(round(cond[0], 3)))
    Pstr = str("Pressure: " + str(round(cond[1], 1)) + " Pa")
    Tstr = str("Temperature: " + str(round(cond[2], 1)) + " K")
    Dstr = str("Density: " + str(round(cond[3], 4)) + " kg/m3")
    SPstr = str("Stagnation P: " + str(round(cond[4], 1)) + " Pa")
    STstr = str("Stagnation T: " + str(round(cond[5], 1)) + " K")
    SoSstr = str("Speed of sound: " + str(round(cond[6], 1)) + " m/s")
    Vstr = str("Velocity: " + str(round(cond[7], 1)) + " m/s")
    gamStr = str("gamma = " + str(round(cond[8], 6)))
    CpStr = str("Cp = " + str(round(cond[9], 6)))
    RsStr = str("Rs = " + str(cond[10]))
    molStr = str("mol = " + str(cond[11]))
    print(Mstr)
    print(Pstr)
    print(Tstr)
    print(Dstr)
    print(SPstr)
    print(STstr)
    print(SoSstr)
    print(Vstr)
    print(gamStr)
    print(CpStr)
    print(RsStr)
    print(molStr)

def printAngle(angleString, radians):
    angle = math.degrees(radians)
    print(angleString, angle)

def obliqueShock(condIn, delta, perfTup):
    Min = condIn[0]
    gammaIn = condIn[8]
    theta, strongTheta = egg.obliqueTheta(gammaIn, Min, delta)
    Mout = egg.oMout(gammaIn, Min, delta, theta)
    Prout = egg.oPout_Pin(gammaIn, Min, theta)
    Trout = egg.oTout_Tin(gammaIn, Min, theta)
    Drout = egg.oDout_Din(gammaIn, Min, theta)
    SProut = egg.oSPout_SPin(gammaIn, Min, theta)
    Pout = Prout * condIn[1]
    Tout = Trout * condIn[2]
    Dout = Drout * condIn[3]
    SPout = SProut * condIn[4]
    STout = condIn[5]
    gammaOut = egg.realGamma(perfTup[0], Tout)
    CpOut = egg.realCp(perfTup[0], perfTup[1], Tout)
    SoSout = egg.idealSoS(gammaOut, condIn[10], Tout)
    Vout = Mout * SoSout
    RsOut = condIn[10]
    molOut = condIn[11]
    condOut = (Mout, Pout, Tout, Dout, SPout, STout, SoSout, Vout, gammaOut, CpOut, RsOut, molOut)
    return condOut, theta

def normalShock(condIn, perfTup):
    Min = condIn[0]
    gammaIn = condIn[8]
    Mout = egg.nMout(gammaIn, Min)
    Prout = egg.nPout_Pin(gammaIn, Min)
    Trout = egg.nTout_Tin(gammaIn, Min)
    Drout = egg.nDout_Din(gammaIn, Min)
    SProut = egg.nSPout_SPin(gammaIn, Min)
    Pout = Prout * condIn[1]
    Tout = Trout * condIn[2]
    Dout = Drout * condIn[3]
    SPout = SProut * condIn[4]
    STout = condIn[5]
    gammaOut = egg.realGamma(perfTup[0], Tout)
    CpOut = egg.realCp(perfTup[0], perfTup[1], Tout)
    SoSout = egg.idealSoS(gammaOut, condIn[10], Tout)
    Vout = Mout * SoSout
    RsOut = condIn[10]
    molOut = condIn[11]
    condOut = (Mout, Pout, Tout, Dout, SPout, STout, SoSout, Vout, gammaOut, CpOut, RsOut, molOut)
    return condOut

def solveShock(condIn, delta, perfTup):
    maxDelta = egg.detachmentRad(condIn[8], condIn[0])
    if maxDelta <= delta:
        condOut = normalShock(condIn, perfTup)
        theta = math.radians(90)
        shockType = "N"
    elif maxDelta > delta:
        condOut, theta = obliqueShock(condIn, delta, perfTup)
        shockType = "O"
    else:
        condOut = None
        theta = None
        shockType = "F"
    return shockType, condOut, theta

def solveIntake(condIn, config, perfTup):
    delta1 = math.radians(config[0])
    delta2 = math.radians(config[1])
    delta3 = math.radians(config[2])
    delta4 = delta1 + delta2 + delta3
    deltas = (delta1, delta2, delta3, delta4)
    shock1, cond1, theta1 = solveShock(condIn, delta1, perfTup)
    #printAngle("Theta1:", theta1)
    #printCond("Cond1:", cond1)
    if shock1 == "O":
        shock2, cond2, theta2 = solveShock(cond1, delta2, perfTup)
        #printAngle("Theta2:", theta2)
        #printCond("Cond2:", cond2)
        if shock2 == "O":
            shock3, cond3, theta3 = solveShock(cond2, delta3, perfTup)
            #printAngle("Theta3:", theta3)
            #printCond("Cond3:", cond3)
            if shock3 == "O":
                shock4, cond4, theta4 = solveShock(cond3, delta4, perfTup)
                #printAngle("Theta4:", theta4)
                #printCond("Cond4:", cond4)
                if shock4 == "O":
                    conds = (cond1, cond2, cond3, cond4)
                    thetas = (theta1, theta2, theta3, theta4)
                    intakePass = True
                else:
                    conds = (cond1, cond2, cond3, cond4)
                    thetas = (theta1, theta2, theta3, theta4)
                    intakePass = False
                    print("Fail at shock 4")
            else:
                conds = (cond1, cond2, cond3)
                thetas = (theta1, theta2, theta3)
                intakePass = False
                print("Fail at shock 3")
        else:
            conds = (cond1, cond2)
            thetas = (theta1, theta2)
            intakePass = False
            print("Fail at shock 2")
    else:
        conds = (cond1)
        thetas = (theta1)
        intakePass = False
        print("Fail at shock 1")
    return intakePass, conds, thetas, deltas

#condOut = (Mout, Pout, Tout, Dout, SPout, STout, SoSout, Vout, gammaOut, CpOut, RsOut, molOut)

def quasiHeating(condIn, perfTup, steamTup, fuelTup, LHV, maxT):
    return 0

def rayleighRelations(perfTup, M, gam):
    P_Pch = egg.idealP_Pch(gam, M)
    T_Tch = egg.idealT_Tch(gam, M)
    D_Dch = egg.idealD_Dch(gam, M)
    SP_SPch = egg.idealSP_SPch(gam, M)
    ST_STch = egg.idealST_STch(gam, M)
    return P_Pch, T_Tch, D_Dch, SP_SPch, ST_STch

def basicHeating(condIn, perfTup, maxT):
    Min = condIn[0]
    Tin = condIn[2]
    print("Min =", Min)
    MarangeReversed = np.round(np.arange(1.001,Min,0.001), 6)
    Marange = MarangeReversed[::-1]
    Trange = []
    MgamRange = []
    gamA = egg.realGamma(perfTup[0], Tin)
    T_TchA = egg.idealT_Tch(gamA, Min)
    TchA = Tin / T_TchA
    for x in Marange:
        T_TchB = egg.idealT_Tch(gamA, x)
        TB = T_TchB * TchA
        TchB = TB / T_TchB
        gamB = egg.realGamma(perfTup[0], TB)
        Mgam = (x, gamB)
        MgamRange.append(Mgam)
        #debugV = x * egg.idealSoS(gamB, perfTup[2], TB)
        #debugD = condIn[3] / egg.idealD_Dch(gamB, x)
        #debugFlow = debugV * debugD
        #print("M =", x, "| gam =", gamB, "| T =", TB, "| massFlow =", debugFlow)
        Trange.append(TB)
    Tdict = dict(zip(MgamRange, Trange))
    MgamOut, Tout = min(Tdict.items(), key=lambda x:abs(maxT - x[1]))
    print("Mout =", MgamOut)
    Mout = MgamOut[0]
    gamOut = MgamOut[1]
    rayleighTupIn = rayleighRelations(perfTup, Min, gamA)
    rayleighTupOut = rayleighRelations(perfTup, Mout, gamOut)
    inPr, inTr, inDr, inSPr, inSTr = rayleighRelations(perfTup, Min, gamA)
    ouPr, ouTr, ouDr, ouSPr, ouSTr = rayleighRelations(perfTup, Mout, gamOut)
    Pout = (condIn[1] / inPr) * ouPr
    Dout = (condIn[3] / inDr) * ouDr
    SPout = (condIn[4] / inSPr) * ouSPr
    STout = (condIn[5] / inSTr) * ouSTr
    print("Tout =", Tout)
    print("STout =", STout)
    SoSout = egg.idealSoS(gamOut, perfTup[2], Tout)
    Vout = Mout * SoSout
    CpOut = egg.realCp(perfTup[0], perfTup[1], Tout)
    RsOut = condIn[10]
    molOut = condIn[11]
    condOut = (Mout, Pout, Tout, Dout, SPout, STout, SoSout, Vout, gamOut, CpOut, RsOut, molOut)
    qOut = CpOut * (STout - condIn[5])
    print(CpOut, "x (", STout, "-", condIn[5], ") =", qOut)
    return condOut, qOut

def shitQuasiDivNozzle(condIn, perfTup, expansionRatio):
    Min = condIn[0]
    gamIn = condIn[8]
    STin = condIn[5]
    T_STin = condIn[2] / STin
    SDin = condIn[3] / egg.realD_SD(perfTup[0], T_STin, condIn[2])
    Marange = np.round(np.arange(Min,6.,0.001), 6)
    Mrange = []
    Arange = []
    condRange = []
    aGam = egg.quasiNozzleGamma(gamIn, perfTup[0], Min, STin)
    aAch = egg.idealA_Ach(aGam, Min)
    aSP = egg.idealP_SP(aGam, Min)
    aST = egg.idealT_ST(aGam, Min)
    aSD = egg.idealD_SD(aGam, Min)
    aP = condIn[1] / (aSP * condIn[4])
    aT = condIn[2] / (aST * STin)
    aD = condIn[3] / (aSD * SDin)
    #print("Inlet A/Ach:", aAch)
    for x in Marange:
        testGam = egg.quasiNozzleGamma(gamIn, perfTup[0], x, STin)
        testA_Ach = egg.idealA_Ach(testGam, x)
        testP_SP = egg.idealP_SP(testGam, x)
        testT_ST = egg.idealT_ST(testGam, x)
        testD_SD = egg.idealD_SD(testGam, x)
        testP = testP_SP * condIn[4] * aP
        testT = testT_ST * STin * aT
        testD = testD_SD * SDin * aD
        testSoS = egg.idealSoS(testGam, perfTup[2], testT)
        testV = testSoS * x
        testCp = egg.realCp(perfTup[0], perfTup[1], testT)
        testCond = (x, testP, testT, testD, condIn[4], condIn[5], testSoS, testV, testGam, testCp, perfTup[2], perfTup[3])
        Mrange.append(x)
        Arange.append(testA_Ach)
        condRange.append(testCond)
        expRbtio = testA_Ach / aAch
        #print("M:", x, "| ExpR:", expRbtio, "| V:", testV, "| P:", testP, "| T:", testT, "| D:", testD, "| gam:", testGam)
    Adict = dict(zip(Arange, Mrange))
    condDict = dict(zip(condRange, Arange))
    proxA, proxM = min(Adict.items(), key=lambda x:abs(Min - x[1]))
    Aratio = proxA * expansionRatio
    condOut, Aout = min(condDict.items(), key=lambda x:abs(Aratio - x[1]))
    actualAratio = Aout / proxA
    #print("Actual area ratio:", actualAratio)
    return condOut, actualAratio

def performance(conds, areaOut, deltas, thetas, LHV, q):
    print("q =", q)
    condAmb = conds[0]
    cond1 = conds[1]
    cond2 = conds[2]
    cond3 = conds[3]
    condInlet = conds[4]
    condOut = conds[6]
    ambientP = condAmb[1]
    Din = condInlet[3]
    Vin = condInlet[7]
    Ain = 1
    massIn = Din * Vin * Ain
    condMid = conds[5]
    massMid = condMid[3] * condMid[7] * Ain
    #print(Din, Vin, massIn)
    #print(condMid[3], condMid[7], massMid)
    Dout = condOut[3]
    Vout = condOut[7]
    massOut = Dout * Vout * areaOut
    #print(Dout, Vout, massOut)
    newtonianThrust = (massIn * condOut[7]) - (massIn * condInlet[7])
    pressureThrust = (condOut[1] - ambientP) * areaOut
    totalThrust = newtonianThrust + pressureThrust
    fuelFlow = (q / LHV) * massOut
    pressures = (cond1[1], cond2[1], cond3[1])
    lift, drag, length, height = geom.solveDrag(deltas, thetas, pressures)
    #print("drag", drag)
    excessThrust = totalThrust - drag
    Isp = (1 / (g * fuelFlow)) * excessThrust
    print("Mass in:", massIn)
    print("Mass mid:", massMid)
    print("Mass out:", massOut)
    burger = (1.4, 1005, 287, 28.97)
    print("CondInlet:", condInlet)
    zeroFuelThrust(condInlet, burger, 15, drag, ambientP)
    return excessThrust, fuelFlow, Isp, drag, length, height

def zeroFuelThrust(condInlet, perfTup, expansionRatio, drag, ambientP):
    condOut, areaOut = shitQuasiDivNozzle(condInlet, perfTup, expansionRatio)
    massIn = condInlet[3] * condInlet[7] * 1
    newtonianThrust = (massIn * condOut[7]) - (massIn * condInlet[7])
    pressureThrust = (condOut[1] - ambientP)
    zeroFuelThrust = (newtonianThrust + pressureThrust) - drag
    print("Zero fuel Vin:", condInlet[7])
    print("Zero fuel Vout:", condOut[7])
    print("Zero fuel mflow:", massIn)
    print("Zero fuel thrust:", zeroFuelThrust)
    return None

def initAmbient(gamma, Mlo, Mhi, Mstep, Q):
    Mrange = np.round(np.arange(Mlo,Mhi,Mstep), 6)
    altRange = np.linspace(0, 47000, num=47000)
    Prange = [isa.Pisa(x) for x in altRange]
    PaltDict = dict(zip(altRange, Prange))
    ambientRange = []
    for m in Mrange:
        P = egg.idealPfromMQ(gamma, m, Q)
        estAlt, estP = min(PaltDict.items(), key=lambda x: abs(P - x[1]))
        temp, pres, dens = isa.isa(estAlt)
        condAmb = (temp, pres, dens)
        dynamicP = egg.idealQ(gamma, m, pres)
        ambientTup = (m, estAlt, condAmb, dynamicP)
        ambientRange.append(ambientTup)
    return ambientRange
    
        
