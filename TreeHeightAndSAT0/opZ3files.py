import csv

def parseZ3file(fileName, N):
    with open(fileName, 'r') as fp:
        line = fp.readline()
        waste, mixer = 0, 1
        reagents = [0]*N
        if line == "unsat":
            return -1, -1, reagents
        while line:
            all = line.split(' = ')
            if all[0][0] == "W":
                waste += 4-int(all[1])
                mixer += 1
            elif all[0][0] == "x":
                x = all[0].split("_")
                reagents[int(x[2])-1] += int(all[1])
            line = fp.readline()
    return waste, mixer, reagents


if __name__ == "__main__":    
    ind = 0
    k = 5
    inputFile = 'cleanTargetRatio.txt'
    outputFile = f"skewed_output{k}.xls"
    with open(inputFile, 'r') as ip:
        # Read the input file line by line
        line = ip.readline()
        while line:
            # Cleaning the values
            all = [float(val) for val in line.split(',')]
            targetRatio = all[:-1] # Target ratio
            err = all[-1] # error tolerance

            if len(targetRatio) == k:
                fileName = f"./z3OutputFiles/z3outputFile{ind}"
                waste, mixer, reagentList = parseZ3file(fileName, k)
                values = [ind, waste, mixer, *reagentList]
                print(values)
                with open(outputFile, "a", newline= '') as op:
                    writer = csv.writer(op)
                    writer.writerow(values)
            ind+=1

            line = ip.readline()