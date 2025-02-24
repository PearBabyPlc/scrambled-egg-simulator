### a rejig of BuzzerRookie's ISA calculator: https://gist.github.com/buzzerrookie/5b6438c603eabf13d07e
### input - geometric altitude
### outputs - temperature, pressure, density, OR just pressure

import math

smb = 6356750
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

def isa(altitudeGeom):
	a = [-0.0065, 0, 0.001, 0.0028]
	h = [11000, 20000, 32000, 47000]
	p0 = 101325
	t0 = 288.15
	prevh = 0
	altitude = (smb * altitudeGeom) / (altitudeGeom + smb)
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
	return temperature, pressure, density

def Pisa(altitudeGeom):
        temperature, pressure, density = isa(altitudeGeom)
        return pressure

def Disa(altitudeGeom):
        temperature, pressure, density = isa(altitudeGeom)
        return density

def Tisa(altitudeGeom):
        temperature, pressure, density = isa(altitudeGeom)
        return temperature


