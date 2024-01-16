from z3 import *
from itertools import permutations
import csv

def get_all_possible_values(ratio, err, output_file, depth):
    # Create a Z3 solver
    number_of_variables = len(ratio)
    solver = Solver()

    # Create Z3 variables for x1, x2, x3, and x4
    R = []
    for i in range(number_of_variables):
        var_name = f'R{i+1}'
        var = Int(var_name)
        solver.add(var > 0)
        R.append(var)

    # Adding constraint
    for i in range(number_of_variables):
        solver.add(R[i]/4**depth - ratio[i] <= err)
        solver.add(ratio[i] - R[i]/4**depth <= err)
    solver.add(Sum(R) == 4**depth)

    with open(output_file, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)

        header = [f'R{i+1}' for i in range(number_of_variables)]
        writer.writerow(header)

        iter = 10

        # Iterate over all satisfying models
        while (solver.check() == sat) & (iter > 0):
            # Get the model
            iter = iter-1
            model = solver.model()

            values = [model.eval(var).as_long() for var in R]

            # write in CSV file
            writer.writerow(values)

            # Print the values dynamically based on the number of variables
            variables_str = ', '.join(f'R{i+1} = {val}' for i, val in enumerate(values))
            print(variables_str)

            # Add constraint to exclude the current solution and it's permutations
            allPermuations = list(permutations(values))
            for per in allPermuations:
                constraint = Or(*[var != val for var, val in zip(R, per)])
                solver.add(constraint)

# Get and print all possible values
def main():
    # ratio = [float(x) for x in input("Target ratio: ").split(',')]
    # err = float(input("Error: "))
    # fileName = input("File name: ")
    ratio = [0.25, 0.30, 0.45]
    err = 0.004
    fileName = 'output.xls'
    for d in range(3, 4):
        get_all_possible_values(ratio, err, fileName, d)

# If the it is called from this function
if __name__ == "__main__":
    main()