# Scrambled Egg Simulator - Scramjet, Scramble, Haha, Get It?
Scrambled Egg Simulator is a foolhardy attempt at modelling hypersonic flight - starting with ramjets/scramjet engines. Depending on what you want to do, you need to use either of the two (as of 7 April 2025) versions:
- [v0.1 is for assessing the performance of a single ram/scramjet design for a single set of conditions:](https://github.com/PearBabyPlc/scrambled-egg-simulator/tree/main/v0.1) it creates a nice intake geometry plot, and gives you vague performance values.
- [v0.2 is for roughly estimating performance of only scramjets (not ramjets) within a range of intake ramp angle configs:](https://github.com/PearBabyPlc/scrambled-egg-simulator/tree/main/v0.2) it iterates through the configs for a defined Mach range and dynamic pressure, and outputs a plot of performance indicators (specific impulse and excess thrust), as well as a bunch of other values in the churning command line (which may have thousands of entries)

v0.1 and v0.2 solely deal with ideal gas dynamics - v0.3 (with some calorically imperfect gas dynamics incorporated) is currently under active development:
- v0.3 contains 3 models - one outputs a single set of performance values [(runModelSingle.py)](https://github.com/PearBabyPlc/scrambled-egg-simulator/blob/main/v0.3/runModelSingle.py), another generates a heatmapped scatter plot of metrics across configurations and Mach numbers with constant dynamic pressure [(runModelRange.py)](https://github.com/PearBabyPlc/scrambled-egg-simulator/blob/main/v0.3/runModelRange.py), and the final produces a curve for thrust and Isp, fitted to the maximum thrust config for a given Mach number [(runModelChunks.py)](https://github.com/PearBabyPlc/scrambled-egg-simulator/blob/main/v0.3/runModelChunks.py) In future will also take into account composition changes with fuel addition and high temperature dissociation. Currently a horrifying mess!

## Credits
- The entire University of Queensland hypersonics Youtube channel (https://www.youtube.com/@uqxhypers301xhypersonics7)
- BuzzerRookie for their ISA, used in this project as buzzerrookie_isa.py (https://gist.github.com/buzzerrookie/5b6438c603eabf13d07e)
- Kyle Niemeyer's Gas Dynamics notes, used in this project as kyleniemeyer_gasdynamics.py (https://kyleniemeyer.github.io/gas-dynamics-notes/compressible-flows/oblique-shocks.html)
- The NASA Glenn Research Centre (mainly https://www.grc.nasa.gov/www/k-12/airplane/index.html)

CC BY-SA 4.0

## Examples 
![v0.1 - Intake geometry for a ramjet at 30km, Mach 6, and ramp deflection angles of 3, 10 and 12 degrees](https://github.com/PearBabyPlc/scrambled-egg-simulator/blob/main/v0.1/intakeGeometry-30km-M6-3-10-12.png)
_v0.1 - Intake geometry for a ramjet at 30km, Mach 6, and ramp deflection angles of 3, 10 and 12 degrees._

![v0.2 - Plot of specific impulse (s) and thrust (kN) for a theoretical highly variable geometry scramjet, from Mach 4-14. Dynamic pressure is 45kPa, brighter in the colour map means hotter combustion chamber temperatures.](https://github.com/PearBabyPlc/scrambled-egg-simulator/blob/main/v0.2/Isp_Thrust_Mach%2045kPa.png)
_v0.2 - Plot of specific impulse (s) and thrust (kN) for a theoretical highly variable geometry scramjet, from Mach 4-14. Dynamic pressure is 45kPa, brighter in the colour map means hotter combustion chamber temperatures._
