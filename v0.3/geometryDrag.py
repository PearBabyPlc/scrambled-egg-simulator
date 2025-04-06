#old file from v0.2

import math
#import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import fsolve

def shock1(x):
    return x * math.tan(-(theta1))

def shock2(x):
    return x * math.tan(-(delta1 + theta2))

def shock3(x):
    return x * math.tan(-(delta1 + delta2 + theta3))

def shock4(x):
    return x * math.tan(theta4 - (delta1 + delta2 + delta3))

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

#surface area for a 1m slice
def surfaceLength(x1, y1, x2, y2):
    sxr = abs(x1 - x2)
    syr = abs(y1 - y2)
    pythag = sxr**2 + syr**2
    return pythag**(1/2)

#finally show plot
#fig, ax = plt.subplots()
#ax.plot([xMin, xMax], [0, 0])
#ax.plot(shock1range, shock1(shock1range))
#ax.plot(shock2range, shock2(shock2range))
#ax.plot(shock3range, shock3(shock3range))
#ax.plot(shock4range, shock4(shock4range))
#ax.plot([0, s4l], [0, 0])
#ax.plot([s4l, s4l], [0, 1])
#ax.plot(surf3xRange, surface3(surf3xRange))
#ax.plot(surf2xRange, surface2(surf2xRange))
#ax.plot(surf1xRange, surface1(surf1xRange))
#ax.set_aspect('equal')
#plt.savefig("intakeGeometryDebug.pdf")
#plt.show()

def solveDrag(deltas, thetas, pressures):
    global delta1, delta2, delta3, delta4
    global theta1, theta2, theta3, theta4
    global surf3xMin, surf2xMin
    
    delta1 = deltas[0]
    delta2 = deltas[1]
    delta3 = deltas[2]
    delta4 = deltas[3]
    theta1 = thetas[0]
    theta2 = thetas[1]
    theta3 = thetas[2]
    theta4 = thetas[3]

    global s4l
    s4l = 1 / (math.tan(theta4 - (delta1 + delta2 + delta3)))
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

    P1 = pressures[0]
    P2 = pressures[1]
    P3 = pressures[2]
    F1 = (lengthF1 * P1)
    angleF1 = math.radians(90) - delta1
    F2 = (lengthF2 * P2)
    angleF2 = math.radians(90) - (delta1 + delta2)
    F3 = (lengthF3 * P3)
    angleF3 = math.radians(90) - (delta1 + delta2 + delta3)
    L1 = F1 * math.sin(angleF1)
    L2 = F2 * math.sin(angleF2)
    L3 = F3 * math.sin(angleF3)
    D1 = F1 * math.cos(angleF1)
    D2 = F2 * math.cos(angleF2)
    D3 = F3 * math.cos(angleF3)
    Ltotal = L1 + L2 + L3
    Dtotal = D1 + D2 + D3
    Ftotal = F1 + F2 + F3

    length = abs(F1xm - s4l)
    height = abs(F1ym)
    
    return Ltotal, Dtotal, length, height

#dd1 = math.radians(3)
#dd2 = math.radians(6)
#dd3 = math.radians(10)
#dd4 = math.radians(19)
#dt1 = math.radians(7.8)
#dt2 = math.radians(11.0)
#dt3 = math.radians(16.2)
#dt4 = math.radians(29.0)

#debug = solveDrag((dd1, dd2, dd3, dd4), (dt1, dt2, dt3, dt4), (867, 2831, 13103))
#print(debug)

    
