import math

Theta = 3055 + (5 / 9)

def CpT(gami, Cpi, T):
    ThT = Theta / T
    square = ThT**2 * (math.e**ThT / (math.e**ThT - 1)**2)
    return Cpi * (1 + ((gami - 1) / gami) * square)

def gamT(gami, T):
    ThT = Theta / T
    square = ThT**2 * (math.e**ThT / (math.e**ThT - 1)**2)
    return 1 + ((gami - 1) / (1 + (gami - 1) * square))

def idealST_T(gam, M):
    return 1 + ((gam - 1) / 2) * M**2

def idealSP_P(gam, M):
    return idealST_T(gam, M)**(gam / (gam - 1))

def idealSD_D(gam, M):
    return idealST_T(gam, M)**(1 / (gam - 1))

def idealA_Ach(gam, M):
    top = (gam + 1) / 2
    btm = idealST_T(gam, M)
    pwr = (gam + 1) / (2 - (2 * gam))
    return (1 / M) * (top / btm)**pwr

def idealMassFlow(SP, Rs, ST, A, gam, M):
    front = SP / math.sqrt(Rs * ST)
    mid = A * math.sqrt(gam) * M
    back = idealST_T(gam, M)**((gam + 1) / (2 - (2 * gam)))
    return front * mid * back

def idealST_STch(gam, M):
    a = 2 * (gam + 1) * M**2
    b = (1 + gam*M**2)**2
    c = 1 + ((gam - 1) / 2) * M**2
    return (a / b) * c

def idealSP_SPch(gam, M):
    first = (gam + 1) / (1 + gam*M**2)
    secnd = 2 / (gam + 1)
    return first * (secnd * idealST_T(gam, M))**(gam / (gam - 1))

def idealP_Pch(gam, M):
    return (gam + 1) / (1 + gam*M**2)

def idealD_Dch(gam, M):
    return (1 + gam*M**2) / ((gam + 1) * M**2)

def idealT_Tch(gam, M):
    return ((gam + 1)**2 * M**2) / (1 + gam*M**2)**2
