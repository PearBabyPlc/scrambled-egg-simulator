import math

SMB = 6356750
g = 9.80655
R = 8.3145
mol = 0.0289644

def solveConditions(ref, geop):
    (refT, refP, refD, lapse, refGeop) = ref
    temp = refT - (lapse * (geop - refGeop))
    if lapse == 0:
        pExp = (-g * mol * (geop - refGeop)) / (R * refT)
        pres = refP * math.exp(pExp)
        dens = refD * math.exp(pExp)
    else:
        pExp = (g * mol) / (R * lapse)
        pres = refP * (1 - (lapse / refT)*(geop - refGeop))**pExp
        dExp = pExp - 1
        dens = refD * ((refT - (geop - refGeop)*lapse) / refT)**dExp
    return temp, pres, dens

def getISA_geom(geom):
    geop = (SMB * geom) / (SMB + geom)
    if geop < 11000:
        ref = (288.15, 101325, 1.225, 0.0065, 0)
    elif (geop >= 11000) and (geop < 20000):
        ref = (216.65, 22632.1, 0.36391, 0, 11000)
    elif (geop >= 20000) and (geop < 32000):
        ref = (216.65, 5474.89, 0.08803, -0.001, 20000)
    elif (geop >= 32000) and (geop < 47000):
        ref = (228.65, 868.02, 0.01322, -0.0028, 32000)
    elif (geop >= 47000) and (geop < 51000):
        ref = (270.65, 110.91, 0.00143, 0, 47000)
    elif (geop >= 51000) and (geop < 71000):
        ref = (270.65, 66.94, 0.00086, 0.0028, 51000)
    elif geop >= 71000:
        ref = (214.65, 3.96, 0.000064, 0.002, 71000)
    else:
        print("idfk")
        ref = (-288.15, -101325, -1.225, -0.0065, -11000)
    temp, pres, dens = solveConditions(ref, geop)
    return temp, pres, dens, geop
