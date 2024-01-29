import sys
import time
from z3 import *

s = Optimize()

# Adding mixer variables
R_1_1, R_1_2, R_1_3 = Ints('R_1_1 R_1_2 R_1_3')
R_2_1, R_2_2, R_2_3 = Ints('R_2_1 R_2_2 R_2_3')
R_3_1, R_3_2, R_3_3 = Ints('R_3_1 R_3_2 R_3_3')

# Creating reagent usage variable
x_1_1, x_1_2, x_1_3 = Ints('x_1_1 x_1_2 x_1_3')
x_2_1, x_2_2, x_2_3 = Ints('x_2_1 x_2_2 x_2_3')
x_3_1, x_3_2, x_3_3 = Ints('x_3_1 x_3_2 x_3_3')

# Creating intermediate fluid share variables
W_2_1 = Int('W_2_1')
W_3_2 = Int('W_3_2')

# Creating height variables
h_1, H_1 = Ints('h_1 H_1')
h_2, H_2 = Ints('h_2 H_2')
h_3, H_3 = Ints('h_3 H_3')

# Adding nonnegativity constraints on reagent usage
s.add(And(x_1_1 >= 0, x_1_1 <= 4, x_1_2 >= 0, x_1_2 <= 4, x_1_3 >= 0, x_1_3 <= 4))
s.add(And(x_2_1 >= 0, x_2_1 <= 4, x_2_2 >= 0, x_2_2 <= 4, x_2_3 >= 0, x_2_3 <= 4))
s.add(And(x_3_1 >= 0, x_3_1 <= 4, x_3_2 >= 0, x_3_2 <= 4, x_3_3 >= 0, x_3_3 <= 4))

# Adding nonnegativity constraints on sharing of intermediate fluids
s.add(And(W_2_1 >= 0, W_2_1 <= 3, W_3_2 >= 0, W_3_2 <= 3))

# Adding nonnegativity constraints on total mixer units
s.add(Or(x_1_1+x_1_2+x_1_3+W_2_1==0, x_1_1+x_1_2+x_1_3+W_2_1==4))
s.add(Or(x_2_1+x_2_2+x_2_3+W_3_2==0, x_2_1+x_2_2+x_2_3+W_3_2==4))
s.add(Or(x_3_1+x_3_2+x_3_3==0, x_3_1+x_3_2+x_3_3==4))

# Adding mixer consistency constraint
s.add(R_1_1 == (4**H_2)*x_1_1+W_2_1*R_2_1)
s.add(R_1_2 == (4**H_2)*x_1_2+W_2_1*R_2_2)
s.add(R_1_3 == (4**H_2)*x_1_3+W_2_1*R_2_3)
s.add(R_2_1 == (4**H_3)*x_2_1+W_3_2*R_3_1)
s.add(R_2_2 == (4**H_3)*x_2_2+W_3_2*R_3_2)
s.add(R_2_3 == (4**H_3)*x_2_3+W_3_2*R_3_3)
s.add(R_3_1 == x_3_1)
s.add(R_3_2 == x_3_2)
s.add(R_3_3 == x_3_3)

# Adding sharing constraint
constraint2 = x_2_1+x_2_2+x_2_3==0
s.add(Implies(constraint2, And(W_2_1 == 0, W_3_2 == 0)))
s.add(Implies(Not(constraint2), And(W_2_1 >= 0, W_3_2 >= 0)))
constraint3 = x_3_1+x_3_2+x_3_3==0
s.add(Implies(constraint3, And(W_3_2 == 0)))
s.add(Implies(Not(constraint3), And(W_3_2 >= 0)))

# Adding height constraint
s.add(h_1 == 1)
s.add(Implies(W_2_1 == 0, h_2 == 0))
s.add(Implies(W_2_1 > 0, h_2 == 1))
s.add(Implies(W_3_2 == 0, h_3 == 0))
s.add(Implies(W_3_2 > 0, h_3 == 1))
s.add(H_1 == H_2+h_1)
s.add(H_2 == H_3+h_2)
s.add(H_3 == h_3)

# Adding base condition
s.add(0.25*(4**H_1) - R_1_1 <= 0.007*(4**H_1))
s.add(R_1_1 - 0.25*(4**H_1) <= 0.007*(4**H_1))
s.add(0.3*(4**H_1) - R_1_2 <= 0.007*(4**H_1))
s.add(R_1_2 - 0.3*(4**H_1) <= 0.007*(4**H_1))
s.add(0.45*(4**H_1) - R_1_3 <= 0.007*(4**H_1))
s.add(R_1_3 - 0.45*(4**H_1) <= 0.007*(4**H_1))

startTime = time.time()
if s.check() == sat:
	fp = open('z3outputFile','w')
	lst = s.model()
	for i in lst:
	    fp.write(str(i) + " = " + str(s.model()[i]) + '\n')
else:
	print('unsat')
endTime = time.time()
executionTime = endTime - startTime
print("Execution Time = ",executionTime)
