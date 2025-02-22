### a rejig of BuzzerRookie's ISA calculator: https://gist.github.com/buzzerrookie/5b6438c603eabf13d07e
### input - geometric altitude OR geopotential altitude
### outputs - temperature, pressure, density, speed of sound (ambient Mach)
### required - numpy

import math
import numpy as np

### PearBabyPlc code:
semiMinorAxisEarth = 6356752.3141 #IUGG value in metres

def geomISA(geomAlt):
        geopAlt = (semiMinorAxisEarth * geomAlt) / (geomAlt + semiMinorAxisEarth)
        temperature, pressure, density, mach = isa(geopAlt)
        return temperature, pressure, density, mach
        
def geopISA(geopAlt):
        temperature, pressure, density, mach = isa(geopAlt)
        return temperature, pressure, density, mach

### BuzzerRookie's code (everything from now on, lines starting w # are disabled as unneeded):

#altitude = float(input("Enter geopotential altitude in (0-47,000m): "))

g = 9.80665
R = 287.00

def cal(p0, t0, a, h0, h1):
	if a != 0:
		t1 = t0 + a * (h1 - h0)
		p1 = p0 * (t1 / t0) ** (-g / a / R)
	else:
		t1 = t0
		p1 = p0 * math.exp(-g / R / t0 * (h1 - h0))
	return t1, p1

def isa(altitude):
	a = [-0.0065, 0, 0.001, 0.0028]
	h = [11000, 20000, 32000, 47000]
	p0 = 101325
	t0 = 288.15
	prevh = 0
	if altitude < 0 or altitude > 47000:
		print("altitude must be in [0, 47000]")
		return
	for i in range(0, 4):
		if altitude <= h[i]:
			temperature, pressure = cal(p0, t0, a[i], prevh, altitude)
			break;
		else:
			# sth like dynamic programming
			t0, p0 = cal(p0, t0, a[i], prevh, h[i])
			prevh = h[i]

	density = pressure / (R * temperature)
	#strformat = 'Temperature: {0:.2f} \nPressure: {1:.2f} \nDensity: {2:.4f}'
	#print(strformat.format(temperature, pressure, density))
	mach = math.sqrt(1.4 * 287 * temperature)
	return temperature, pressure, density, mach
