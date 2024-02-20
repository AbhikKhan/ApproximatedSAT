from z3 import *
from itertools import permutations
import csv

from FloSPA import *

def get_all_possible_values(ratio, err, output_file, depth):
    # Create a Z3 solver
    number_of_variables = len(ratio)
    solver = Solver()

    # Create Z3 variables for x1, x2, x3...xn
    R = []
    for i in range(number_of_variables):
        var_name = f'R{i+1}'
        var = Int(var_name)
        solver.add(var > 0)
        R.append(var)

    # Adding constraint
    for i in range(number_of_variables):
        solver.add(R[i] - ratio[i]*(4**depth) <= err*(4**depth))
        solver.add(ratio[i]*(4**depth) - R[i] <= err*(4**depth))
    solver.add(Sum(R) == 4**depth)

    iter = 20
    with open(output_file, 'w+') as opfile:

        # Iterate over all satisfying models
        while (solver.check() == sat) & (iter > 0):
            # Get the model
            iter-=1
            model = solver.model()

            values = [model.eval(var).as_long() for var in R]
            # write in file
            opstring = ""
            for var in values:
                opstring += f"{var},"

            opstring = opstring[:-1]+"\n"
            opfile.write(opstring)
            # Print the values dynamically based on the number of variables
            variables_str = ', '.join(f'R{i+1} = {val}' for i, val in enumerate(values))
            print(variables_str)

            # Add constraint to exclude the current solution and it's permutations
            allPermuations = list(permutations(values))
            for per in allPermuations:
                constraint = Or(*[var != val for var, val in zip(R, per)])
                solver.add(constraint)

    return iter

# Get and print all possible values
def main():
    ind = 0
    k = 3
    inputFile = 'ip.txt'
    with open(inputFile, 'r') as ip:
        # Read the input file line by line
        line = ip.readline()
        while line:
            # Cleaning the values
            all = [float(val) for val in line.split(',')]
            
            ratio = all[:-1] # actual Target ratio
            err = all[-1] # error tolerance

            if len(ratio) != k:  # To take target ratios with k reagents
                ind += 1
                line = ip.readline()
                continue

            fileName = 'output.txt'
            for d in range(3, 7):
                generatedRatios = get_all_possible_values(ratio, err, fileName, d)
                if generatedRatios < 20:
                    '''
                        Now as we have some target ratios (at most 20) we can
                        Gnerate FloSPA tree for all of them and get max and min ragent usage
                        Later we can coompare with our result.
                    '''
                    minWaste, minSumReagentUsage, maxWaste, maxSumReagentUsage = 4<<10, 4<<10, 0, 0
                    minReagentUsage = []
                    maxReagentUsage = []
                    ratioFormin = []
                    ratioFormax = []
                    with open(fileName, 'r') as ratioFile:
                        ratio = ratioFile.readline()
                        while ratio:
                            targetRatio = [int(val) for val in ratio.split(',')] # Integer values derived after approximation
                            fact = [4]*len(targetRatio)
                            name = getName(targetRatio)
                            waste, reagentUsage = skeletonTreeGeneration(targetRatio, fact, f"./FloSPA-op/{name}.png")
                            totalReagentUsage = sum(reagentUsage)
                            # Total reagent usage is high
                            if totalReagentUsage > maxSumReagentUsage:
                                maxSumReagentUsage = totalReagentUsage
                                maxWaste = waste
                                maxReagentUsage = reagentUsage
                                ratioFormax = targetRatio
                            # Tootal regent usage is low
                            if totalReagentUsage < minSumReagentUsage:
                                minSumReagentUsage = totalReagentUsage
                                minWaste = waste
                                minReagentUsage = reagentUsage
                                ratioFormin = targetRatio
                            ratio = ratioFile.readline()
                    with open(f'flospa_output_{k}.xls', 'a', newline='') as csvfile:
                        writer = csv.writer(csvfile)
                        values = [ind, *ratioFormin, *minReagentUsage, minWaste, *ratioFormax, *maxReagentUsage, maxWaste]
                        print(values)
                        writer.writerow(values)
                    break
            line = ip.readline()
            ind+=1
    

# If the it is called from this function
if __name__ == "__main__":
    main()