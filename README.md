# Scrambled Egg Simulator - Scramjet, Scramble, Haha, Get It?
Scrambled Egg Simulator is a foolhardy attempt at modelling hypersonic flight - starting with ramjets/scramjet engines. Depending on what you want to do, you need to use either of the two (as of 1 March 2025) versions:
- [v0.1 is for assessing the performance of a single ram/scramjet design for a single set of conditions:](https://github.com/PearBabyPlc/scrambled-egg-simulator/tree/main/v0.1) it creates a nice intake geometry plot, and gives you vague performance values.
- [v0.2 is for roughly estimating performance of only scramjets (not ramjets) within a range of intake ramp angle configs:](https://github.com/PearBabyPlc/scrambled-egg-simulator/tree/main/v0.2) it iterates through the configs for a defined Mach range and dynamic pressure, and outputs a plot of performance indicators (specific impulse and excess thrust), as well as a bunch of other values in the churning command line (which may have thousands of entries)

Accreditations in the readme.md in each version folder.
CC BY-SA 4.0

## Examples 
![v0.1 - Intake geometry for a ramjet at 30km, Mach 6, and ramp deflection angles of 3, 10 and 12 degrees](https://github.com/PearBabyPlc/scrambled-egg-simulator/blob/main/v0.1/intakeGeometry-30km-M6-3-10-12.png)
_v0.1 - Intake geometry for a ramjet at 30km, Mach 6, and ramp deflection angles of 3, 10 and 12 degrees._

![v0.2 - Plot of specific impulse (s) and thrust (kN) for a theoretical highly variable geometry scramjet, from Mach 4-14. Dynamic pressure is 45kPa, brighter in the colour map means hotter combustion chamber temperatures.](https://github.com/PearBabyPlc/scrambled-egg-simulator/blob/main/v0.2/Isp_Thrust_Mach%2045kPa.png)
_v0.2 - Plot of specific impulse (s) and thrust (kN) for a theoretical highly variable geometry scramjet, from Mach 4-14. Dynamic pressure is 45kPa, brighter in the colour map means hotter combustion chamber temperatures._
