#just something that tests whether the solver works with a small hand-specified set of configurations

configa = solveConfig(gamma, (3, 6, 10), 10, 242, 433, 0.0062, 30728)
configb = solveConfig(gamma, (2, 5, 12), 10, 242, 433, 0.0062, 30728)
configc = solveConfig(gamma, (1, 7, 11), 10, 242, 433, 0.0062, 30728)
configd = solveConfig(gamma, (5, 6, 8), 10, 242, 433, 0.0062, 30728)
confige = solveConfig(gamma, (5, 15, 20), 10, 242, 433, 0.0062, 30728)
configf = solveConfig(gamma, (5, 30, 50), 10, 242, 433, 0.0062, 30728)

SPingoing = 30728

def solverPrint(config, angles):
    M = config[1]
    T = config[2]
    P = config[3]
    kPa = P / 1000
    D = config[4]
    SP = config[5]
    SPr = (SP / SPingoing) * 100
    rampNum = config[6]
    if rampNum == 1:
        normal = "Normal shock positioned at nose."
    elif rampNum == 2:
        normal = "Normal shock positioned at the start of ramp 1."
    elif rampNum == 3:
        normal = "Normal shock positioned at the start of ramp 2."
    elif rampNum == 4:
        normal = "Normal shock positioned at the inlet lip."
    elif rampNum == 5:
        normal = "No normal shock in the external intake."
    print()
    print("Angles (deg): " + angles)
    print("Inlet Mach:", round(M, 1))
    print("Inlet T (K):", round(T, 1))
    print("Inlet P (kPa):", round(kPa, 1))
    print("Inlet D (kg/m3):", D)
    print("Inlet stag P (Pa):", SP)
    print("Stag P %:", round(SPr, 1))
    print(normal)

solverPrint(configa, "3, 6, 10")
solverPrint(configb, "2, 5, 12")
solverPrint(configc, "1, 6, 11")
solverPrint(configd, "5, 6, 8")
solverPrint(confige, "5, 15, 20")
solverPrint(configf, "5, 30, 50")
