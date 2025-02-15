### Extraneous Fanno flow friction analysis ###
### References:
### https://www.youtube.com/watch?v=Tov3xLenxX0
### https://www.youtube.com/watch?v=DXK0AAEkj1E
import math
import numpy as np

### subsonic input parameters
D = 0.4
L = 2.0
inletM = 0.5
f = 0.002
gamma = 1.4
print("Diameter (m):", D)
print("Length (m):", L)
print("Inlet Mach:", inletM)
print("Friction coefficient:", f)
print("gamma =", gamma)

### Predefined functions ##
def SP_chokedSP(M):
    a = (1 + ((gamma - 1) / 2) * M**2) / (1 + ((gamma - 1) / 2))
    b = (gamma / (gamma - 1))
    c = (1 / M)
    d = math.sqrt((gamma + 1) / (2 + (gamma - 1) * M**2))
    return c * d * (a**b)

def getFannoParam(M):
    return ((1 - M**2) / (gamma * M**2)) + ((gamma + 1) / (2 * gamma)) * math.log(M**2 / ((2 / (gamma + 1)) * (1 + ((gamma - 1) / 2) * M**2)))

def getMachFromFannoParam(M, FP):
    if (M > 1):
        maxSupM = float(M + 1.000)
        supM = list(np.round(np.arange(1.,maxSupM,0.00001), 6))
        supFP = [getFannoParam(x) for x in supM]
        supFanno = dict(zip(supM, supFP))
        approxSupM, approxSupFP = min(supFanno.items(), key=lambda x: abs(FP - x[1]))
        approxM = approxSupM
        approxFP = approxSupFP
    elif (M < 1):
        subM = list(np.round(np.arange(0.00001,2.,0.00001), 6)) #be careful of the asymptote at x=0 in the Fanno parameter equation
        subFP = [getFannoParam(x) for x in subM]
        subFanno = dict(zip(subM, subFP))
        approxSubM, approxSubFP = min(subFanno.items(), key=lambda x: abs(FP - x[1]))
        approxM = approxSubM
        approxFP = approxSubFP
    return approxM, approxFP

### all the "should be"s are for the parameters given in the referenced videos.
### D = 0.4
### L = 0.5
### inletM = 3.5
### f = 0.002
### gamma = 1.4

#1.
inletFannoParam = getFannoParam(inletM)
print("Inlet Fanno parameter:", inletFannoParam) #should be 0.58642897, correct

inletSP_chokedSP = SP_chokedSP(inletM)
print("Inlet SP/Choked SP:", inletSP_chokedSP) #should be 6.78962053, correct

#2.
exitFannoParam = inletFannoParam - ((4 * f * L) / D)
print("Exit Fanno parameter:", exitFannoParam) #should be 0.576, correct

exitChokedL = (D * exitFannoParam) / (4 * f)
print("Exit choked length:", exitChokedL) #should be 28.82, correct

#3.
approxM, approxFP = getMachFromFannoParam(inletM, exitFannoParam)
fannoParamError = abs(exitFannoParam - approxFP)
print("Fanno parameter (M, FP, error):", approxM, approxFP, fannoParamError)
exitM = approxM
print("Exit M:", exitM) #should be 3.41, close enough given approx
exitSP_chokedSP = SP_chokedSP(exitM)
print("Exit SP/Choked SP:", exitSP_chokedSP) #should be 6.24535398, close enough given approx

#4.
exitSP_inletSP = (exitSP_chokedSP) / (inletSP_chokedSP)
print("Exit SP/Inlet SP:", exitSP_inletSP) #should be 0.92, close enough given approx
