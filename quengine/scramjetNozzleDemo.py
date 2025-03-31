import math
import numpy as np
import matplotlib.pyplot as plt
import quengine as que

M0 = 2
P0 = 200000
T0 = 3500
D0 = 10
Mlo = 2
Mhi = 6.5

maxT = 3500
gammaPerfect = 1.4
CpPerfect = 1005
Rs = 287

T_ST0 = que.realT_ST(gammaPerfect, M0, T0)
ST0 = (1 / T_ST0) * T0
P_SP0 = que.realP_SP(gammaPerfect, T_ST0, T0)
SP0 = (1 / P_SP0) * P0
SD0 = (1 / que.realD_SD(gammaPerfect, T_ST0, T0)) * T0
gamma0 = que.realGamma(gammaPerfect, T0)
Cp0 = que.realCp(gammaPerfect, CpPerfect, T0)

print("M0:", M0)
print("P0:", P0)
print("T0:", T0)
print("D0:", D0)
print("ST0:", ST0)
print("SP0:", SP0)
print("SD0:", SD0)
print("gamma0:", gamma0)
print("Cp0:", Cp0)

perfG = []
idealG = []
quasiG = []

#plot nozzle for max gamma
Mrange = np.linspace(Mlo, Mhi, 1000)
A_AchQuasi = []
P_SPQuasi = []
T_STQuasi = []
D_SDQuasi = []
quasiG = []
quasiV = []
for x in Mrange:
    testGam = que.quasiNozzleGamma(gamma0, gammaPerfect, x, ST0)
    testA = que.idealA_Ach(testGam, x)
    testP = que.idealP_SP(testGam, x)
    testT = que.idealT_ST(testGam, x)
    testD = que.idealD_SD(testGam, x)
    testTemp = testT * ST0
    Sauce = que.idealSoS(testGam, Rs, testTemp)
    Vel = Sauce * x
    A_AchQuasi.append(testA)
    P_SPQuasi.append(testP)
    T_STQuasi.append(testT)
    D_SDQuasi.append(testD)
    quasiG.append(testGam)
    quasiV.append(Vel)

A_AchP = []
P_SPP = []
T_STP = []
D_SDP = []
peG = []
peV = []
for x in Mrange:
    testGam = gamma0
    testA = que.idealA_Ach(testGam, x)
    testP = que.idealP_SP(testGam, x)
    testT = que.idealT_ST(testGam, x)
    testD = que.idealD_SD(testGam, x)
    testTemp = testT * ST0
    Sauce = que.idealSoS(testGam, Rs, testTemp)
    Vel = Sauce * x
    A_AchP.append(testA)
    P_SPP.append(testP)
    T_STP.append(testT)
    D_SDP.append(testD)
    peG.append(testGam)
    peV.append(Vel)

A_AchI = []
P_SPI = []
T_STI = []
D_SDI = []
idG = []
idV = []
for x in Mrange:
    testGam = gammaPerfect
    testA = que.idealA_Ach(testGam, x)
    testP = que.idealP_SP(testGam, x)
    testT = que.idealT_ST(testGam, x)
    testD = que.idealD_SD(testGam, x)
    testTemp = testT * ST0
    Sauce = que.idealSoS(testGam, Rs, testTemp)
    Vel = Sauce * x
    A_AchI.append(testA)
    P_SPI.append(testP)
    T_STI.append(testT)
    D_SDI.append(testD)
    idG.append(testGam)
    idV.append(Vel)

#id = perfect
#pe = ideal (yeah I messed up)

fig, (ax1, ax2, ax3, ax4) = plt.subplots(1, 4)
ax3.plot(Mrange, A_AchQuasi, label='Area ratio', color='green')
ax3.plot(Mrange, A_AchP, linestyle='dotted', color='green')
ax3.plot(Mrange, A_AchI, linestyle='dashed', color='green')
ax1.plot(Mrange, P_SPQuasi, label='Pressure ratio', color='blue')
ax1.plot(Mrange, P_SPP, linestyle='dotted', color='blue')
ax1.plot(Mrange, P_SPI, linestyle='dashed', color='blue')
ax1.plot(Mrange, T_STQuasi, label='Temperature ratio', color='orange')
ax1.plot(Mrange, T_STP, linestyle='dotted', color='orange')
ax1.plot(Mrange, T_STI, linestyle='dashed', color='orange')
ax1.plot(Mrange, D_SDQuasi, label='Density ratio', color='red')
ax1.plot(Mrange, D_SDP, linestyle='dotted', color='red')
ax1.plot(Mrange, D_SDI, linestyle='dashed', color='red')
ax4.plot(Mrange, quasiG, label='Real')
ax4.plot(Mrange, peG, linestyle='dotted', label='Ideal')
ax4.plot(Mrange, idG, linestyle='dashed', label='Perfet')
ax2.plot(A_AchQuasi, quasiV, label='Velocity')
ax2.plot(A_AchP, peV, linestyle='dotted')
ax2.plot(A_AchI, idV, linestyle='dashed')
ax1.legend()
ax2.legend()
ax3.legend()
ax4.legend()
ax4.grid()
ax3.grid()
ax1.grid()
ax2.grid('both')
ax1.set_title("Stagnation condition ratios")
ax1.set_xlabel("Mach")
ax1.set_yscale('log')
ax2.set_title("Velocity and expansion ratio")
ax2.set_xlabel("Expansion ratio")
ax2.set_ylabel("m/s")
ax2.set_xlim([0, 50])
ax3.set_title("Mach and expansion ratio")
ax3.set_xlabel("Mach")
ax4.set_title("Gamma")
ax4.set_xlabel("Mach")
plt.savefig("quazzle.pdf")
plt.show()

    
