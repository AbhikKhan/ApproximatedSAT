from z3 import *
from itertools import permutations
import csv

def get_all_possible_values(number_of_variables, output_file):
    # Create a Z3 solver
    solver = Solver()

    # Create Z3 variables for x1, x2, x3...xn
    R = []
    pR = []
    precison = 100
    for i in range(number_of_variables):
        var_name1 = f'R{i+1}'
        var1 = Real(var_name1)
        solver.add(And(var1 >= 0.15, var1 <= 0.6))
        R.append(var1)

        var_name2 = f'pR{i+1}'
        var2 = Int(var_name2)
        solver.add(var2 == var1*precison)
        pR.append(var2)

    # Adding constraint
    solver.add(Sum(pR) == 1*precison)

    with open(output_file, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)

        header = [f'R{i+1}' for i in range(number_of_variables)]
        writer.writerow(header)

        iter = 100

        # Iterate over all satisfying models
        while (solver.check() == sat) & (iter > 0):
            # Get the model
            iter = iter-1
            model = solver.model()

            values = [model.eval(var).as_decimal(3) for var in R]

            # write in CSV file
            writer.writerow(values)

            # Print the values dynamically based on the number of variables
            variables_str = ', '.join(f'R{i+1} = {val}' for i, val in enumerate(values))
            print(variables_str)

            # Add constraint to exclude the current solution and it's permutations
            values = [model.eval(var).as_long() for var in pR]
            allPermuations = list(permutations(values))
            for per in allPermuations:
                constraint = Or(*[var != val for var, val in zip(pR, per)])
                solver.add(constraint)



# Get and print all possible values
def main():
    fileName = 'testCases.xls'
    N = 4
    get_all_possible_values(N, fileName)

# If the it is called from this function
if __name__ == "__main__":
    main()