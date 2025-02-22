import math
import numpy as np
#import inputhelper as iohelper

#testRatio = iohelper.restrictedInput("Enter test ratio (0 to 1): ", 0, True, 1, True)

#Mach2/Mach1 = StagT2/StagT1
#max Rayleigh function is at Mach 1, that's what scramjets and ramjets aim for
gamma = 1.4

def rayleighFunc(M, gamma):
    return ((1 + ((gamma - 1) / 2)*M**2)*M**2) / ((1 + gamma*M**2)**2)

#machNumber = list(np.round(np.arange(0.,30.,0.01), 3))
#rayleighFactor = [rayleighFunc(x) for x in machNumber]
#rayleighUnscaled = dict(zip(machNumber, rayleighFactor))

#queryone = iohelper.restrictedInput("Enter Mach number (0 to 30): ", 0, True, 30, True)
#print(rayleighUnscaled[queryone])



#maxRF = rayleighFunc(1)
#querystring = str("Enter Rayleigh factor (0 to " + str(maxRF) + "): ")
#querytwo = iohelper.restrictedInput(querystring, 0, True, maxRF, True)
#sub_M, sub_RF = min(rayleighSubsonic.items(), key=lambda x: abs(querytwo - x[1]))
#print("Subsonic solution: Mach", sub_M, ", RF =", sub_RF)
#sup_M, sup_RF = min(rayleighSupersonic.items(), key=lambda x: abs(querytwo - x[1]))
#print("Supersonic solution: Mach", sup_M, ", RF =", sup_RF)

def getMachFromRF(RF, gamma):
    subsonicM = list(np.round(np.arange(0.,1.,0.01), 3))
    subsonicRF = [rayleighFunc(x, gamma) for x in subsonicM]
    rayleighSubsonic = dict(zip(subsonicM, subsonicRF))
    supersonicM = list(np.round(np.arange(1.,30.,0.01), 3))
    supersonicRF = [rayleighFunc(x, gamma) for x in supersonicM]
    rayleighSupersonic = dict(zip(supersonicM, supersonicRF))
    sub_M, sub_RF = min(rayleighSubsonic.items(), key=lambda x: abs(RF - x[1]))
    sup_M, sup_RF = min(rayleighSupersonic.items(), key=lambda x: abs(RF - x[1]))
    return sub_M, sub_RF, sup_M, sup_RF



