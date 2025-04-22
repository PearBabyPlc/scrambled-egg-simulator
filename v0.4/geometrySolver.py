import math
import numpy as np
from scipy.optimize import fsolve
import matplotlib.pyplot as plt

def shock1(x):
    return x * math.tan(-theta1)

def shock2(x):
    return x * math.tan(-(delta1 + theta2))

def shock3(x):
    return x * math.tan(-(delta1 + delta2 + theta3))

def shock4(x):
    return x * math.tan(theta4 - (delta1 + delta2 + delta3))

def surface3(x):
    return (x - s4l) * math.tan(-(delta1 + delta2 + delta3)) + 1

def surf3end(x):
    return surface3(x) - shock3(x)

def surface2(x):
    return (x - surf3xMin) * math.tan(-(delta1 + delta2)) + surface3(surf3xMin)

def surf2end(x):
    return surface2(x) - shock2(x)

def surface1(x):
    return (x - surf2xMin) * math.tan(-delta1) + surface2(surf2xMin)

def surf1end(x):
    return surface1(x) - shock1(x)

def surfaceLen(x1, y1, x2, y2):
    sxr = abs(x1 - x2)
    syr = abs(y1 - y2)
    return (sxr**2 + syr**2)**(1 / 2)

def solve(deltas, thetas, conds):
    global delta1, delta2, delta3, delta4
    global theta1, theta2, theta3, theta4
    global s4l, surf3xMin, surf3xMax, surf2xMin, surf2xMax, surf1xMin, surf1xMax
    
    delta0, delta1, delta2, delta3, delta4 = deltas
    theta0, theta1, theta2, theta3, theta4 = thetas
    cond0, cond1, cond2, cond3, cond4 = conds

    s4l = 1 / shock4(1)
    surf3xMin = fsolve(surf3end, [0, 0])
    surf3xMax = s4l
    surf2xMin = fsolve(surf2end, [0, 0])
    surf2xMax = surf3xMin
    surf1xMin = fsolve(surf1end, [0, 0])
    surf1xMax = surf2xMin

    F1xm = surf1xMin
    F1ym = surface1(F1xm)
    F1xh = surf1xMax
    F1yh = surface1(F1xm)
    lenF1 = surfaceLen(F1xm, F1ym, F1xh, F1yh)
    F2xm = surf2xMin
    F2ym = surface2(F2xm)
    F2xh = surf2xMax
    F2yh = surface2(F2xh)
    lenF2 = surfaceLen(F2xm, F2ym, F2xh, F2yh)
    F3xm = surf3xMin
    F3ym = surface3(F3xm)
    F3xh = surf3xMax
    F3yh = surface3(F3xh)
    lenF3 = surfaceLen(F3xm, F3ym, F3xh, F3yh)

    ra = math.radians(90)
    P1, P2, P3 = cond1[1], cond2[1], cond3[1]
    F1 = P1 * lenF1
    F2 = P2 * lenF2
    F3 = P3 * lenF3
    radF1 = ra - delta1
    radF2 = ra - (delta1 + delta2)
    radF3 = ra - (delta1 + delta2 + delta3)
    L1 = F1 * math.sin(radF1)
    L2 = F2 * math.sin(radF2)
    L3 = F3 * math.sin(radF3)
    D1 = F1 * math.cos(radF1)
    D2 = F2 * math.cos(radF2)
    D3 = F3 * math.cos(radF3)
    Ltotal = L1 + L2 + L3
    Dtotal = D1 + D2 + D3
    lenTotal = abs(F1xm - s4l)
    height = abs(F1ym)
    lenRamp = lenTotal - (lenF1 * math.cos(delta1))
    return Ltotal, Dtotal, lenTotal, lenRamp, height

def solveAndPlot(deltas, thetas, conds):
    Ltotal, Dtotal, lenTotal, lenRamp, height = solve(deltas, thetas, conds)
    print("Length (total):", lenTotal)
    print("Length (ramp):", lenRamp)
    print("Height (total):", height)
    print("Lift:", Ltotal)
    print("Drag:", Dtotal)
    surf1xRange = np.linspace(surf1xMin, surf1xMax, num=100)
    surf2xRange = np.linspace(surf2xMin, surf2xMax, num=100)
    surf3xRange = np.linspace(surf3xMin, surf3xMax, num=100)
    shock1range = np.linspace(surf1xMin, s4l, num=100)
    shock2range = np.linspace(surf2xMin, s4l, num=100)
    shock3range = np.linspace(surf3xMin, s4l, num=100)
    shock4range = np.linspace(0, s4l, num=100)
    plt.style.use("dark_background")
    fig, ax = plt.subplots()
    ax.plot(shock1range, shock1(shock1range), linestyle='dotted')
    ax.plot(shock2range, shock2(shock2range), linestyle='dotted')
    ax.plot(shock3range, shock3(shock3range), linestyle='dotted')
    ax.plot(shock4range, shock4(shock4range), linestyle='dotted')
    ax.plot([0, s4l], [0, 0])
    ax.plot([s4l, s4l], [0, 1])
    ax.plot(surf3xRange, surface3(surf3xRange))
    ax.plot(surf2xRange, surface2(surf2xRange))
    ax.plot(surf1xRange, surface1(surf1xRange))
    ax.set_aspect('equal')
    plt.savefig("intakeGeometryPlot.pdf")
    plt.show()
