import sys
import time
from z3 import *

s = Optimize()

# Adding mixer variables
R_1_1, R_1_2, R_1_3, R_1_4 = Ints('R_1_1 R_1_2 R_1_3 R_1_4')
R_2_1, R_2_2, R_2_3, R_2_4 = Ints('R_2_1 R_2_2 R_2_3 R_2_4')
R_3_1, R_3_2, R_3_3, R_3_4 = Ints('R_3_1 R_3_2 R_3_3 R_3_4')
R_4_1, R_4_2, R_4_3, R_4_4 = Ints('R_4_1 R_4_2 R_4_3 R_4_4')

# Creating reagent usage variable
x_1_1, x_1_2, x_1_3, x_1_4 = Ints('x_1_1 x_1_2 x_1_3 x_1_4')
x_2_1, x_2_2, x_2_3, x_2_4 = Ints('x_2_1 x_2_2 x_2_3 x_2_4')
x_3_1, x_3_2, x_3_3, x_3_4 = Ints('x_3_1 x_3_2 x_3_3 x_3_4')
x_4_1, x_4_2, x_4_3, x_4_4 = Ints('x_4_1 x_4_2 x_4_3 x_4_4')

# Creating intermediate fluid share variables
W_2_1 = Int('W_2_1')
W_3_2 = Int('W_3_2')
W_4_3 = Int('W_4_3')

# Creating height variables
h = Int('h')
h_2 = Int('h_2')
h_3 = Int('h_3')
h_4 = Int('h_4')

# Adding nonnegativity constraints on reagent usage
s.add(And(x_1_1 >= 0, x_1_1 <= 4, x_1_2 >= 0, x_1_2 <= 4, x_1_3 >= 0, x_1_3 <= 4, x_1_4 >= 0, x_1_4 <= 4))
s.add(And(x_2_1 >= 0, x_2_1 <= 4, x_2_2 >= 0, x_2_2 <= 4, x_2_3 >= 0, x_2_3 <= 4, x_2_4 >= 0, x_2_4 <= 4))
s.add(And(x_3_1 >= 0, x_3_1 <= 4, x_3_2 >= 0, x_3_2 <= 4, x_3_3 >= 0, x_3_3 <= 4, x_3_4 >= 0, x_3_4 <= 4))
s.add(And(x_4_1 >= 0, x_4_1 <= 4, x_4_2 >= 0, x_4_2 <= 4, x_4_3 >= 0, x_4_3 <= 4, x_4_4 >= 0, x_4_4 <= 4))

# Adding nonnegativity constraints on sharing of intermediate fluids
s.add(And(W_2_1 >= 0, W_2_1 <= 3, W_3_2 >= 0, W_3_2 <= 3, W_4_3 >= 0, W_4_3 <= 3))

# Adding nonnegativity constraints on total mixer units
s.add(Or(x_1_1+x_1_2+x_1_3+x_1_4+W_2_1==0, x_1_1+x_1_2+x_1_3+x_1_4+W_2_1==4))
s.add(Or(x_2_1+x_2_2+x_2_3+x_2_4+W_3_2==0, x_2_1+x_2_2+x_2_3+x_2_4+W_3_2==4))
s.add(Or(x_3_1+x_3_2+x_3_3+x_3_4+W_4_3==0, x_3_1+x_3_2+x_3_3+x_3_4+W_4_3==4))
s.add(Or(x_4_1+x_4_2+x_4_3+x_4_4==0, x_4_1+x_4_2+x_4_3+x_4_4==4))

# Adding mixer consistency constraint
s.add(R_1_1 == 4*x_1_1+W_2_1*x_2_1)
s.add(R_1_2 == 4*x_1_2+W_2_1*x_2_2)
s.add(R_1_3 == 4*x_1_3+W_2_1*x_2_3)
s.add(R_1_4 == 4*x_1_4+W_2_1*x_2_4)
s.add(R_2_1 == 4*x_2_1+W_3_2*x_3_1)
s.add(R_2_2 == 4*x_2_2+W_3_2*x_3_2)
s.add(R_2_3 == 4*x_2_3+W_3_2*x_3_3)
s.add(R_2_4 == 4*x_2_4+W_3_2*x_3_4)
s.add(R_3_1 == 4*x_3_1+W_4_3*x_4_1)
s.add(R_3_2 == 4*x_3_2+W_4_3*x_4_2)
s.add(R_3_3 == 4*x_3_3+W_4_3*x_4_3)
s.add(R_3_4 == 4*x_3_4+W_4_3*x_4_4)
s.add(R_4_1 == x_4_1)
s.add(R_4_2 == x_4_2)
s.add(R_4_3 == x_4_3)
s.add(R_4_4 == x_4_4)

# Adding height constraint
s.add(If(x_2_1+x_2_2+x_2_3+x_2_4==0, And(W_2_1 == 0, W_3_2 == 0, W_4_3 == 0), And(W_2_1 >= 0, W_3_2 >= 0, W_4_3 >= 0)))
s.add(If(x_3_1+x_3_2+x_3_3+x_3_4==0, And(W_3_2 == 0, W_4_3 == 0), And(W_3_2 >= 0, W_4_3 >= 0)))
s.add(If(x_4_1+x_4_2+x_4_3+x_4_4==0, And(W_4_3 == 0), And(W_4_3 >= 0)))

s.add(If(W_2_1 == 0, h_2 == 0, h_2 == 1))
s.add(If(W_3_2 == 0, h_3 == 0, h_3 == 1))
s.add(If(W_4_3 == 0, h_4 == 0, h_4 == 1))

s.add(h == 1+h_2+h_3+h_4)

# Adding base condition
s.add(0.3*(4**h) - R_1_1 <= 0.007*(4**h))
s.add(R_1_1 - 0.3*(4**h) <= 0.007*(4**h))
s.add(0.23*(4**h) - R_1_2 <= 0.007*(4**h))
s.add(R_1_2 - 0.23*(4**h) <= 0.007*(4**h))
s.add(0.24*(4**h) - R_1_3 <= 0.007*(4**h))
s.add(R_1_3 - 0.24*(4**h) <= 0.007*(4**h))
s.add(0.23*(4**h) - R_1_4 <= 0.007*(4**h))
s.add(R_1_4 - 0.23*(4**h) <= 0.007*(4**h))

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
