import csv
import matplotlib.pyplot as plt

fig, (ax1, ax2) = plt.subplots(1, 2)

def importCSV(filename, lineColour, label):
    rowList = []
    with open(filename, newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=' ', quotechar="|")
        for row in reader:
            rowList.append(row)
    plotM = []
    plotT = []
    plotI = []
    plotListS = []
    for x in rowList:
        plotList = []
        for y in x:
            try:
                yF = float(y)
            except:
                yF = "string unconverted"
            plotList.append(yF)
        plotListS.append(plotList)
    for x in plotListS:
        plotM.append(x[0])
        plotT.append(x[8])
        plotI.append(x[9])
    plotM.pop(0)
    plotM.pop(-1)
    plotT.pop(0)
    plotT.pop(-1)
    plotI.pop(0)
    plotI.pop(-1)
    ax1.plot(plotM, plotT, color=lineColour, label=label)
    ax2.plot(plotM, plotI, color=lineColour, label=label)

importCSV("chunks Q=30.csv", "r", "Q = 30kPa")
importCSV("chunks Q=40.csv", "b", "Q = 40kPa")
importCSV("chunks Q=50.csv", "g", "Q = 50kPa")
ax1.grid()
ax2.grid()
ax1.legend()
ax2.legend()
ax1.set_xlabel("Mach")
ax2.set_xlabel("Mach")
ax1.set_ylabel("kN")
ax2.set_ylabel("Isp")
ax1.set_title("Thrust")
ax2.set_title("Specific impulse")
plt.savefig("csvReconstruction.pdf")
plt.show()


