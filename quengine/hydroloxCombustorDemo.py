import math
import numpy as np
import matplotlib.pyplot as plt
import quengine as que

def lazyDensity(mol, P, Rs, T):
    return ((mol * P) / (Rs * T))

### INPUTS HERE ###

M0 = 0.95
P0 = 100000 * 200
T0 = 3500
D0 = lazyDensity(18, P0, 462, T0)
Mlo = 0.1
Mhi = 1.0

maxT = 4000
gammaPerfect = 1.33
CpPerfect = 1850
Rs = 462

#0 = pre combustion
#1 = post combustion
#2 = throat
#3 = exit

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

#plot chamber for max gamma (gammaPerfect) w dashed line
Mrange = np.linspace(Mlo, Mhi, 1000)
P_PchPerf = []
T_TchPerf = []
D_DchPerf = []
SP_SPchPerf = []
ST_STchPerf = []
qP = []
for x in Mrange:
    testGam = gammaPerfect
    testP_Pch = que.idealP_Pch(testGam, x)
    testT_Tch = que.idealT_Tch(testGam, x)
    testD_Dch = que.idealD_Dch(testGam, x)
    testSP_SPch = que.idealSP_SPch(testGam, x)
    testST_STch = que.idealST_STch(testGam, x)
    P_PchPerf.append(testP_Pch)
    T_TchPerf.append(testT_Tch)
    D_DchPerf.append(testD_Dch)
    SP_SPchPerf.append(testSP_SPch)
    ST_STchPerf.append(testST_STch)
    perfG.append(gammaPerfect)
    q = (((1 / testST_STch) * ST0) - ST0) * Cp0
    qP.append(q)

#plot for min gamma (gamma0) w dotted line
P_PchIdeal = []
T_TchIdeal = []
D_DchIdeal = []
SP_SPchIdeal = []
ST_STchIdeal = []
qI = []
for x in Mrange:
    testGam = gamma0
    testP_Pch = que.idealP_Pch(testGam, x)
    testT_Tch = que.idealT_Tch(testGam, x)
    testD_Dch = que.idealD_Dch(testGam, x)
    testSP_SPch = que.idealSP_SPch(testGam, x)
    testST_STch = que.idealST_STch(testGam, x)
    P_PchIdeal.append(testP_Pch)
    T_TchIdeal.append(testT_Tch)
    D_DchIdeal.append(testD_Dch)
    SP_SPchIdeal.append(testSP_SPch)
    ST_STchIdeal.append(testST_STch)
    idealG.append(gamma0)
    q = (((1 / testST_STch) * ST0) - ST0) * Cp0
    qI.append(q)

#plot for variable gamma w solid line
P_PchQuasi = []
T_TchQuasi = []
D_DchQuasi = []
SP_SPchQuasi = []
ST_STchQuasi = []
qQ = []
for x in Mrange:
    testGam = que.quasiRayleighGamma(gamma0, gammaPerfect, x, maxT)
    testP_Pch = que.idealP_Pch(testGam, x)
    testT_Tch = que.idealT_Tch(testGam, x)
    testD_Dch = que.idealD_Dch(testGam, x)
    testSP_SPch = que.idealSP_SPch(testGam, x)
    testST_STch = que.idealST_STch(testGam, x)
    P_PchQuasi.append(testP_Pch)
    T_TchQuasi.append(testT_Tch)
    D_DchQuasi.append(testD_Dch)
    SP_SPchQuasi.append(testSP_SPch)
    ST_STchQuasi.append(testST_STch)
    quasiG.append(testGam)
    q = (((1 / testST_STch) * ST0) - ST0) * Cp0
    qQ.append(q)

fig, (ax1, ax2, ax3) = plt.subplots(1, 3)
ax1.plot(Mrange, P_PchQuasi, color='blue', label='Pressure ratio')
ax1.scatter(1, 1)
ax1.plot(Mrange, T_TchQuasi, color='orange', label='Temperature ratio')
ax1.plot(Mrange, D_DchQuasi, color='red', label='Density ratio')
ax1.plot(Mrange, P_PchPerf, color='blue', linestyle='dashed')
ax1.plot(Mrange, T_TchPerf, color='orange', linestyle='dashed')
ax1.plot(Mrange, D_DchPerf, color='red', linestyle='dashed')
ax1.plot(Mrange, P_PchIdeal, color='blue', linestyle='dotted')
ax1.plot(Mrange, T_TchIdeal, color='orange', linestyle='dotted')
ax1.plot(Mrange, D_DchIdeal, color='red', linestyle='dotted')
ax2.plot(Mrange, perfG, linestyle='dashed', label='Perfect')
ax2.plot(Mrange, idealG, linestyle='dotted', label='Ideal')
ax2.plot(Mrange, quasiG, label='Real')
ax3.plot(Mrange, qQ, label='J/kg')
ax3.plot(Mrange, qI, linestyle='dotted')
ax3.plot(Mrange, qP, linestyle='dashed')
ax3.legend()
ax3.grid()
ax3.set_yscale('log')
ax1.legend()
ax2.legend()
ax1.grid()
ax2.grid()
ax1.set_xlabel("Mach")
ax2.set_xlabel("Mach")
ax3.set_xlabel("Mach")
ax1.set_title("Choked condition ratios")
ax2.set_title("Gamma")
ax3.set_title("Heat flux required to choke flow")
ax1.set_ylim([0, 6])
plt.savefig("hydroloxCombustorDemo.pdf")
plt.show()
