import math
import geometrySolver as geom

cond0 = (5, 600)
cond1 = (4, 1500)
cond2 = (3.2, 3000)
cond3 = (2.8, 8000)
cond4 = (1.9, 23000)

delta0 = math.radians(2)
delta1 = math.radians(3)
delta2 = math.radians(10)
delta3 = math.radians(12)
delta4 = delta1 + delta2 + delta3

theta0 = math.radians(6.9)
theta1 = math.radians(11.6)
theta2 = math.radians(18.3)
theta3 = math.radians(23.2)
theta4 = math.radians(44.3)

deltas = (delta0, delta1, delta2, delta3, delta4)
thetas = (theta0, theta1, theta2, theta3, theta4)
conds = (cond0, cond1, cond2, cond3, cond4)

geom.solveAndPlot(deltas, thetas, conds)
