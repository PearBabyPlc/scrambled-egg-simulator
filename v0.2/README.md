# Scrambled Egg Simulator v0.2 (Iterable Boogaloo)
![Plot of specific impulse (s) and thrust (kN) for a theoretical highly variable geometry scramjet, from Mach 4-14. Dynamic pressure is 45kPa, brighter in the colour map means hotter combustion chamber temperatures.](https://github.com/PearBabyPlc/scrambled-egg-simulator/blob/main/v0.2/Isp_Thrust_Mach%2045kPa.png)
_Plot of specific impulse (s) and thrust (kN) for a theoretical highly variable geometry scramjet, from Mach 4-14. Dynamic pressure is 45kPa, brighter in the colour map means hotter combustion chamber temperatures._

## About
Scrambled Egg Simulator v0.2 is really only good for roughly estimating potential performance of a scramjet within a range of intake configs, and if you want to assess the performance of a single design your best bet is to try out v0.1 - which has helpful command line input prompts, unlike v0.2. This version also does not model ramjets, only scramjets with fully supersonic flow; it does not produce any visualisations of the intake geometries either.

## How to use
Define test conditions at near the top of [the main Python file:](https://github.com/PearBabyPlc/scrambled-egg-simulator/blob/main/v0.2/runModel.py)
- Mlo, Mhi, step: mach range, for np.arange() creation
- Q: dynamic pressure, to calculate a constant dynamic pressure altitude-Mach trajectory
- gamma = 1.4 generally
- R = 287 in dry air
- Cp = 1005 in dry air
- chamberA = 1, leave as is
- expansionRatio: ratio of combustion chamber area to de Laval nozzle exhaust area
- temperatureLimit: maximum allowable chamber temperature
- lengthLimit: maximum allowable intake length from inlet to leading edge of the aircraft, remember that this is relative to the inlet area (set at 1m2, dimensions of 1x1 metres)
- ramp1range, ramp2range, ramp3range: tuple containing the ranges of angles for each ramp, itertools is used to create a list of all possible intake ramp angle configs, current bug means all tuples must contain the same number of values or else it can't iterate

After defining all necessary variables (don't touch any other ones), the program will chug along in the command line. Each subsequent model component result cascades into what should ultimately be either a pass or fail for the config. All of the following conditions have to be met for the model to pass:
- Inlet Mach number above 1.0
- Combustor temperature within limit at 99% of choked flow heat addition
- Intake length within size limit
- Overall model produces positive thrust with drag taken into consideration

The pass/fail conditions aren't terribly well enforced, so expect lots of weird outliers in the final output plot.

## Future
v0.3 will be split into several smaller models that will encompass the functionalities of both v0.1 and v0.2, as well as attempt to model the whole aircraft (dimensions, geometry, performance, practicality). In the meantime, good luck making sense of anything these two dozen YandereDev-nested-if-statements-in-a-trenchcoat manage to plot.

## Credits
- The entire University of Queensland hypersonics Youtube channel (https://www.youtube.com/@uqxhypers301xhypersonics7)
- BuzzerRookie for their ISA, used in this project as buzzerrookie_isa.py (https://gist.github.com/buzzerrookie/5b6438c603eabf13d07e)
- Kyle Niemeyer's Gas Dynamics notes, used in this project as kyleniemeyer_gasdynamics.py (https://kyleniemeyer.github.io/gas-dynamics-notes/compressible-flows/oblique-shocks.html)
- The NASA Glenn Research Centre (mainly https://www.grc.nasa.gov/www/k-12/airplane/index.html)

CC BY-SA 4.0

## Structure
- runModel.py (Numerically solving for the best performance at a given Mach for a set of ramp angles)
- buzzerrookie_isa.py (BuzzerRookie's International Standard Atmosphere calculator, with a few tweaks for my use)
- kyleniemeyer_gasdynamics.py (Whenever my attempts at solving various aerodynamics problems fails, Kyle Niemeyer is there to help)
- formulaegg.py (Random equations and shit that other bits of code can use for science)
- nozzle.py (Rayleigh flow de Laval nozzle solver for estimation)
- geometryDrag.py (Calculates intake geometry and drag, for evaluation of practicality and performance (excess thrust, specific impulse)
- unused.py (I have no idea)

## Dependencies
- numpy
- matplotlib
- scipy
- (built-in modules: math, itertools)
