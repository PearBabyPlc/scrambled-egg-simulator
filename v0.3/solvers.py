import math
import formulaegg as egg
import buzzerrookie_isa as isa
import numpy as np

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
    shock1, cond1, theta1 = solveShock(condIn, delta1, perfTup)
    printAngle("Theta1:", theta1)
    printCond("Cond1:", cond1)
    if shock1 == "O":
        shock2, cond2, theta2 = solveShock(cond1, delta2, perfTup)
        printAngle("Theta2:", theta2)
        printCond("Cond2:", cond2)
        if shock2 == "O":
            shock3, cond3, theta3 = solveShock(cond2, delta3, perfTup)
            printAngle("Theta3:", theta3)
            printCond("Cond3:", cond3)
            if shock3 == "O":
                shock4, cond4, theta4 = solveShock(cond3, delta4, perfTup)
                printAngle("Theta4:", theta4)
                printCond("Cond4:", cond4)
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
    return intakePass, conds, thetas

#condOut = (Mout, Pout, Tout, Dout, SPout, STout, SoSout, Vout, gammaOut, CpOut, RsOut, molOut)

def quasiHeating(condIn, perfTup, steamTup, fuelTup, LHV, maxT):
    return 0

#not good, roughGam and testGam diverge with iteration
def shittyHeating(condIn, perfTup, maxT):
    Min = condIn[0]
    MarangeReversed = np.round(np.arange(1.,Min,0.01), 6)
    Marange = MarangeReversed[::-1]
    testCondRange = []
    Trange = []
    for x in Marange:
        roughGam = egg.quasiRayleighGamma(condIn[8], perfTup[0], x, maxT)
        roughT_Tch = egg.idealT_Tch(roughGam, x)
        roughT = condIn[2] / roughT_Tch
        testGam = egg.realGamma(perfTup[0], roughT)
        testT_Tch = egg.idealT_Tch(testGam, x)
        testT = condIn[2] / testT_Tch
        testP_Pch = egg.idealP_Pch(testGam, x)
        testP = condIn[1] / testP_Pch
        testD_Dch = egg.idealD_Dch(testGam, x)
        testD = condIn[3] / testD_Dch
        testSP_SPch = egg.idealSP_SPch(testGam, x)
        testSP = condIn[4] / testSP_SPch
        testST_STch = egg.idealST_STch(testGam, x)
        testST = condIn[5] / testST_STch
        Trange.append(testT)
        testCond = (x, testP, testT, testD, testSP, testST, testGam)
        testCondRange.append(testCond)
    testCondDict = dict(zip(testCondRange, Trange))
    approxCond, bpproxT = min(testCondDict.items(), key=lambda x:abs(maxT - x[1]))
    Mout = approxCond[0]
    Pout = approxCond[1]
    Tout = approxCond[2]
    Dout = approxCond[3]
    SPout = approxCond[4]
    STout = approxCond[5]
    SoSout = egg.idealSoS(approxCond[6], perfTup[2], Tout)
    Vout = Mout * SoSout
    gammaOut = approxCond[6]
    CpOut = egg.realCp(perfTup[0], perfTup[1], Tout)
    RsOut = perfTup[2]
    molOut = perfTup[3]
    condOut = (Mout, Pout, Tout, Dout, SPout, STout, SoSout, Vout, gammaOut, CpOut, RsOut, molOut)
    qOut = CpOut * (STout - condIn[5])
    return condOut, qOut
    
    
