import pearbaby_isa as isa
import matplotlib.pyplot as plt
plt.style.use('dark_background')

altitudes = range(0, 30001, 1)

alts = []
temps = []
denss = []
press = []
for alt in altitudes:
    temp, pres, dens, geop = isa.getISA_geom(alt)
    alts.append(alt)
    temps.append(temp)
    denss.append(dens)
    press.append(pres)

fig, (ax1, ax2, ax3) = plt.subplots(1, 3)
ax1.plot(temps, alts)
ax2.plot(denss, alts)
ax3.plot(press, alts)
ax1.set_title("Temp")
ax2.set_title("Dens")
ax3.set_title("Pres")
#ax2.set_xscale('log')
#ax3.set_xscale('log')
ax1.grid()
ax2.grid()
ax3.grid()
plt.savefig("pearbabyISA.pdf")
plt.show()

