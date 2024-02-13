from z3 import *
from itertools import permutations
import csv

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

    with open(output_file, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)

        header = [f'R{i+1}' for i in range(number_of_variables)]
        writer.writerow(header)

        iter = 20

        # Iterate over all satisfying models
        while (solver.check() == sat) & (iter > 0):
            # Get the model
            iter = iter-1
            model = solver.model()

            values = [model.eval(var).as_long() for var in R]
            print(sum(values))
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
    ratio = [0.017578125,0.0048828125,0.6552734375,0.205078125,0.1171875]
    err = 0.00459
    fileName = 'output'
    for d in range(3, 6):
        get_all_possible_values(ratio, err, f"{fileName}{d}.xls", d)

# If the it is called from this function
if __name__ == "__main__":
    main()