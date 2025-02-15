###extraneous Rayleigh/isentropic analysis of heat addition. Based on UQx Hypersonics 4.3.3.1

import rayleigh
import inputhelper as iohelper
import math

#combustor in main doc = inlet here
inletM = 3.5
inletT = 600
inletP = 100000
inletD = 0.5805
q = 500000
gamma = 1.4
Cp = 1005
ramOrScram = str()
if (inletM < 1):
    ramOrScram = "ram"
elif (inletM > 1):
    ramOrScram = "scram"

print("Ram or scram?", ramOrScram)

#1.
inletT_ST = (1 + ((gamma - 1) / 2) * inletM**2)**(-1)
print("Inlet T/ST:", inletT_ST)
inletST = inletT / inletT_ST
print("Inlet ST:", inletST)

#2.
exitST = (q / Cp) + inletST
print("Exit ST:", exitST)

#3.
chokedRayleighFactor = rayleigh.rayleighFunc(1, gamma)
print("Choked Rayleigh factor:", chokedRayleighFactor)
inletST_chokedST = rayleigh.rayleighFunc(inletM, gamma) / chokedRayleighFactor
print("Inlet ST/Choked ST:", inletST_chokedST)
exitST_chokedST = (exitST / inletST) * inletST_chokedST
print("Exit ST/Choked ST):", exitST_chokedST)

#4.
exitRF = exitST_chokedST * chokedRayleighFactor
exitM_subsonic = int()
exitM_supersonic = int()
lookupRF_subsonic = int()
lookupRF_supersonic = int()
exitM_subsonic, lookupRF_subsonic, exitM_supersonic, lookupRF_supersonic = rayleigh.getMachFromRF(exitRF, gamma)
subsonicError = abs(exitRF - lookupRF_subsonic)
supersonicError = abs(exitRF - lookupRF_supersonic)
#todo: error correction, some sort of multiplier based on linear extrapolation of line between the 2 closest lookup table values
print("Subsonic Rayleigh factor (M, RF, error):", exitM_subsonic, lookupRF_subsonic, subsonicError)
print("Supersonic Rayleigh factor (M, RF, error):", exitM_supersonic, lookupRF_supersonic, supersonicError)
exitM = exitM_supersonic #generally an exhaust will speed the flow up lmao
print("Exit M:", exitM)

#5.
exitT_ST = (1 + ((gamma - 1) / 2) * exitM**2)**(-1)
print("Exit T/ST:", exitT_ST)
exitT = exitST * exitT_ST
print("Exit T:", exitT)

def SP_chokedSP(M, gamma):
    return ((gamma + 1) / (1 + gamma * M**2)) * ((2 / (gamma + 1)) * (1 + ((gamma - 1) / 2) * M**2))**(gamma / (gamma - 1))

exitSP_inletSP = SP_chokedSP(exitM, gamma) * (1 / (SP_chokedSP(inletM, gamma)))
print("Exit SP/Inlet SP:", exitSP_inletSP)




