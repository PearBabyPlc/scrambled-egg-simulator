import math

B = 6.1 * 10**(-5) #molecular size constant
C = -2130.09088 #intermolecular force constant
Theta = 3055 + (5 / 9)
Rs = 287
gammaIdeal = 1.4
GamUpIdeal = gammaIdeal**2 - 3*gammaIdeal + 3

def findIMFconst(B):
    #do this shit later, Berthelot equation of state
    pass

def Ach_Aideal(M, gamma):
    a = (gamma + 1) / 2
    b = 1 + ((gamma - 1) / 2) * M**2
    c = (gamma + 1) / (2 * (gamma - 1))
    Ach_Aideal = M * (a / b)**c
    return Ach_Aideal

def D_SDideal(M):
    a = 1 + ((gammaIdeal - 1) / 2) * M**2
    D_SDideal = a**(-1 / (gammaIdeal - 1))
    return D_SDideal

def P_SPideal(M):
    a = 1 + ((gammaIdeal - 1) / 2) * M**2
    P_SPideal = a**(-gammaIdeal / (gammaIdeal - 1))
    return P_SPideal

def B1(M):
    a = P_SPideal(M) - D_SDideal(M)
    b = 1 - P_SPideal(M)
    B1 = a + ((gammaIdeal - 1) / gammaIdeal)*b
    return B1

def B4(M):
    a = (gammaIdeal + 1) / (2 * (gammaIdeal - 1))
    B4 = a*B1(M) - B1(1)
    return B4

def C1(M):
    a = 2 * (GamUpIdeal / gammaIdeal) * D_SDideal(M)**(2 - gammaIdeal)
    b = 1 - D_SDideal(M)**(1 - gammaIdeal)
    c = 3 * ((gammaIdeal - 1) / gammaIdeal)
    d = 1 - D_SDideal(M)**(2 - gammaIdeal)
    C1 = a*b - c*d
    return C1

def C4(M):
    a = (gammaIdeal + 1) / (2 * (gammaIdeal - 1))
    b = (GamUpIdeal - gammaIdeal) / gammaIdeal
    c = D_SDideal(M)**(3 - 2*gammaIdeal) - D_SDideal(M)**(3 - 2*gammaIdeal)
    C4 = a * (C1(M) - C1(1))+b*c
    return C4

def ST_Tideal(M):
    ST_Tideal = 1 + ((gammaIdeal - 1) / 2) * M**2
    return ST_Tideal

def ST_Tchideal(M):
    ST_Tchideal = ST_Tideal(1)
    return ST_Tchideal

def D1(ST, M):
    a = 1 - math.e**(-(Theta / ST) * (ST_Tideal(M) - 1))
    b = (gammaIdeal - 1) * (Theta / ST) * ST_Tideal(M)
    c = ST_Tideal(M) - 1
    D1 = ((gammaIdeal - 1) / gammaIdeal) * (a * (1 - b*c))
    return D1

def D4(ST, M):
    a = (gammaIdeal + 1) / (2 * (gammaIdeal - 1))
    b = D1(ST, M) - D1(ST, 1)
    c = math.e**(-(Theta / ST) * (ST_Tideal(M) - 1))
    d = ST_Tideal(M) + (ST / Theta)*(1 - ((gammaIdeal - 1)**2 / 2*gammaIdeal) * (Theta / ST)**2 * ST_Tideal(M)**2)
    e = math.e**(-(Theta / ST) * (ST_Tchideal(M) - 1))
    f = ST_Tchideal(M) + (ST / Theta)*(1 - ((gammaIdeal - 1)**2 / 2*gammaIdeal) * (Theta / ST)**2 * ST_Tchideal(M)**2)
    D4 = a*b + c*d - e*f
    return D4

def Ach_A(M, SD, ST):
    a = Ach_Aideal(M, gammaIdeal)
    b = B4(M) * B * SD
    c = C4(M) * ((C * SD) / (Rs * ST**2))
    d = D4(ST, M) * (Theta / ST) * math.e**(Theta / ST)
    Ach_A = a * (1 + b + c + d)
    return Ach_A

print("M = 0.5, SD = 1, ST = 4000")
test = Ach_A(0.5, 1, 4000)
print("Ach / A =", test, "(calorically imperfect)")
ideal = Ach_Aideal(0.5, gammaIdeal)
print("Ach / A =", ideal, "(ideal)")
