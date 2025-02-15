# scrambled-egg-simulator
A variety of calculators and tools for the analysis of hypersonic aerodynamics, propulsion and rocketry. In future the goal is to create a complete model of a waverider spaceplane.



Planned structure (for easy matplotlib analysis later down the line):

1 - conditions.py for ambient atmosphere and velocity/dynamic pressure of aircraft

2 - intake.py for n-oblique shock analysis 

3 - inlet.py for normal shock and Fanno flow analysis of the scram/ramjet intake

4 - combustor.py for Rayleigh flow analysis of heat addition with different fuels; also updates flow params (i.e. gamma) given fuel added

5 - exhaust.py for Rayleigh/isentropic analysis of either a de Laval nozzle or an expansion ramp/aerospike exhaust

6 - geometryIntake.py for drag/lift analysis of the intake defined by intake.py

7 - geometryWhole.py for drag/lift analysis of the whole craft, including geometryIntake.py data

8 - runModel.py runs all of the prior 7 modules in order and as needed, providing a nice little command line input/output



Potentially, in future a .csv parser/writer and matplotlib stuff. For now, just those 8 files.
