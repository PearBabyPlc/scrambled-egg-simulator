# scrambled-egg-simulator
A variety of calculators and tools for the analysis of hypersonic aerodynamics, propulsion and rocketry. The end goal is to create a complete model of a waverider spaceplane.

For now, a single file will run the whole model for a single set of input conditions (altitude and Mach) - it then runs the maths for 4 oblique shocks in the intake, an optional normal shock, and then a Rayleigh/isentropic flow analysis of heat addition in the combustor and expansion through the exhaust nozzle (for now assumed to be de Laval). 

In future, a Fanno flow analysis of the inlet to the combustor will be performed (allowing for a better ramjet model than the rough normal shock approximation), and more detail will be added to the exhaust model to more accurately represent the performance of an airframe-integrated exhaust ramp.

Credit to the following:
- BuzzerRookie for their ISA, used in this project as buzzerrookieisa.py
- Kyle Niemeyer's Gas Dynamics notes, used in this project as kyleniemeyergasdynamics.py
