#safe input that ensures only numerical values
#variable = safeInput(prompt) will loop
def safeInput(prompt):
    localOutput = None
    while True:
        localInput = input(prompt)
        localInputType = type(localInput)
        try:
            localOutput = float(localInput)
            return localOutput
            break
        except:
            print("Try a numerical input.")

#restricted input that includes the safe input functionality
def restrictedInput(prompt, low, inclusiveL, high, inclusiveH):
    if (inclusiveL == False) and (inclusiveH == False):
        while True:
            localOutput = None
            localInput = safeInput(prompt)
            if localInput <= low:
                print("Try a higher input.")
            elif localInput >= high:
                print("Try a lower input.")
            elif (localInput > low) and (localInput < high):
                localOutput = localInput
                return localOutput
                break
    elif (inclusiveL == True) and (inclusiveH == False):
        while True:
            localOutput = None
            localInput = safeInput(prompt)
            if localInput < low:
                print("Try a higher input.")
            elif localInput >= high:
                print("Try a lower input.")
            elif (localInput >= low) and (localInput < high):
                localOutput = localInput
                return localOutput
                break
    elif (inclusiveL == False) and (inclusiveH == True):
        while True:
            localOutput = None
            localInput = safeInput(prompt)
            if localInput <= low:
                print("Try a higher input.")
            elif localInput > high:
                print("Try a lower input.")
            elif (localInput > low) and (localInput <= high):
                localOutput = localInput
                return localOutput
                break
    elif (inclusiveL == True) and (inclusiveH == True):
        while True:
            localOutput = None
            localInput = safeInput(prompt)
            if localInput < low:
                print("Try a higher input.")
            elif localInput > high:
                print("Try a lower input.")
            elif (localInput >= low) and (localInput <= high):
                localOutput = localInput
                return localOutput
                break

#safeInputTest = safeInput("Test safe input: ")
#print(safeInputTest)
#print("(Range: 0 <= input < 1000)")
#restrictedInputTest = restrictedInput("Test restricted input: ", 0, True, 1000, False)
#print(restrictedInputTest)
