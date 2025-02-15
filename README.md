# scrambled-egg-simulator
A variety of calculators and tools for the analysis of hypersonic aerodynamics, propulsion and rocketry. The end goal is to create a complete model of a waverider spaceplane.

For now, a single file will run the whole model for a single set of input conditions (altitude and Mach) - it then runs the maths for 4 oblique shocks in the intake, an optional normal shock, and then a Rayleigh/isentropic flow analysis of heat addition in the combustor and expansion through the exhaust nozzle (for now assumed to be de Laval). 

There is no rhyme or reason to the structuring of the files - they're just what came out of numerous very long nights of geeking out. In future I know that I'll have to probably do a complete rewrite of the main file so I'm able to matplotlib different parameters for optimisation. A lot of efficiency parameters (Isp, stagnation pressure ratios, idk...) are yet to be included. Maybe I should write a complete todo here:
- Stagnation pressure ratio analysis of the intake, comparison to idealised values, dunno?
- Fanno flow analysis of the combustor inlet
- Exhaust ramp analysis, instead of the current de Laval nozzle approximation
- Intake drag analysis, for performance stats (Isp, thrust, etc...)

Credit to the following:
- The entire University of Queensland hypersonics Youtube channel (https://www.youtube.com/@uqxhypers301xhypersonics7)
- BuzzerRookie for their ISA, used in this project as buzzerrookieisa.py (https://gist.github.com/buzzerrookie/5b6438c603eabf13d07e)
- Kyle Niemeyer's Gas Dynamics notes, used in this project as kylesObliqueShocks.py and maybe an additional Prandlt-Meyer thingy (https://kyleniemeyer.github.io/gas-dynamics-notes/compressible-flows/oblique-shocks.html)
