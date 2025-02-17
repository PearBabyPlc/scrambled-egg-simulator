import math
import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import fsolve

delta1deg = 3
delta2deg = 10
delta3deg = 12
delta4deg = delta1deg + delta2deg + delta3deg

theta1deg = 11.6
theta2deg = 18.3
theta3deg = 23.2
theta4deg = 44.3

delta1 = math.radians(delta1deg)
delta2 = math.radians(delta2deg)
delta3 = math.radians(delta3deg)
delta4 = math.radians(delta4deg)
theta1 = math.radians(theta1deg)
theta2 = math.radians(theta2deg)
theta3 = math.radians(theta3deg)
theta4 = math.radians(theta4deg)

def shock1(x):
    return x * math.tan(-(theta1))

def shock2(x):
    return x * math.tan(-(delta1 + theta2))

def shock3(x):
    return x * math.tan(-(delta1 + delta2 + theta3))

def shock4(x):
    return x * math.tan(theta4 - (delta1 + delta2 + delta3))

s4l = 1 / (math.tan(theta4 - (delta1 + delta2 + delta3)))

def surface3(x):
    return (x - s4l) * math.tan(-(delta1 + delta2 + delta3)) + 1

def surface3end(x):
    return surface3(x) - shock3(x)

def surface2(x):
    return (x - surf3xMin) * math.tan(-(delta1 + delta2)) + surface3(surf3xMin)

def surface2end(x):
    return surface2(x) - shock2(x)

def surface1(x):
    return (x - surf2xMin) * math.tan(-(delta1)) + surface2(surf2xMin)

def surface1end(x):
    return surface1(x) - shock1(x)

xMin = -65.0
xMax = 5.0
xPos = np.arange(xMin,xMax,0.1)

surf3xMin = fsolve(surface3end, [0, 0])
surf3xMax = s4l
surf3xRange = np.linspace(surf3xMin, surf3xMax, num=100)

surf2xMin = fsolve(surface2end, [0, 0])
surf2xMax = surf3xMin
surf2xRange = np.linspace(surf2xMin, surf2xMax, num=100)

surf1xMin = fsolve(surface1end, [0, 0])
surf1xMax = surf2xMin
surf1xRange = np.linspace(surf1xMin, surf1xMax, num=100)

shock1range = np.linspace(surf1xMin, s4l, num=100)
shock2range = np.linspace(surf2xMin, s4l, num=100)
shock3range = np.linspace(surf3xMin, s4l, num=100)
shock4range = np.linspace(0., s4l, num=100)

#surface area for a 1m slice
def surfaceLength(x1, y1, x2, y2):
    sxr = abs(x1 - x2)
    syr = abs(y1 - y2)
    pythag = sxr**2 + syr**2
    return pythag**(1/2)

F1xm = surf1xMin[0]
F1ymAlmost = surface1(F1xm)
F1ym = F1ymAlmost[0]
F1xh = surf1xMax[0]
F1yhAlmost = surface1(F1xh)
F1yh = F1yhAlmost[0]
lengthF1 = surfaceLength(F1xm, F1ym, F1xh, F1yh)

F2xm = surf2xMin[0]
F2ymAlmost = surface2(F2xm)
F2ym = F2ymAlmost[0]
F2xh = surf2xMax[0]
F2yhAlmost = surface2(F2xh)
F2yh = F2yhAlmost[0]
lengthF2 = surfaceLength(F2xm, F2ym, F2xh, F2yh)

F3xm = surf3xMin[0]
F3ym = surface3(F3xm)
F3xh = surf3xMax
F3yh = surface3(F3xh)
lengthF3 = surfaceLength(F3xm, F3ym, F3xh, F3yh)

#force calculations
print()
print("Force calculations are for a 1m wide strip of aircraft surface")
P0 = 1196
M0 = 6
P1 = 1839
M1 = 5.6
P2 = 6314
M2 = 4.3
P3 = 20274
M3 = 3.3
P4 = 121637
M4 = 1.6
F1 = (lengthF1 * P1) / 1000
print("Force 1:", F1, "kN")
angleF1 = math.radians(90 - delta1deg)
F2 = (lengthF2 * P2) / 1000
print("Force 2:", F2, "kN")
angleF2 = math.radians(90 - (delta1deg + delta2deg))
F3 = (lengthF3 * P3) / 1000
print("Force 3:", F3, "kN")
angleF3 = math.radians(90 - (delta1deg + delta2deg + delta3deg))
L1 = F1 * math.sin(angleF1)
L2 = F2 * math.sin(angleF2)
L3 = F3 * math.sin(angleF3)
D1 = F1 * math.cos(angleF1)
D2 = F2 * math.cos(angleF2)
D3 = F3 * math.cos(angleF3)
Ltotal = L1 + L2 + L3
Dtotal = D1 + D2 + D3
Ftotal = F1 + F2 + F3
print("Total lift:", Ltotal, "kN")
print("Total drag:", Dtotal, "kN")

#finally show plot
fig, ax = plt.subplots()
#ax.plot([xMin, xMax], [0, 0])
ax.plot(shock1range, shock1(shock1range))
ax.plot(shock2range, shock2(shock2range))
ax.plot(shock3range, shock3(shock3range))
ax.plot(shock4range, shock4(shock4range))
ax.plot([0, s4l], [0, 0])
ax.plot([s4l, s4l], [0, 1])
ax.plot(surf3xRange, surface3(surf3xRange))
ax.plot(surf2xRange, surface2(surf2xRange))
ax.plot(surf1xRange, surface1(surf1xRange))
ax.set_aspect('equal')
plt.savefig("intakeGeometry.pdf")
plt.show()
