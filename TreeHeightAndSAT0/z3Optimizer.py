import sys
import time
from z3 import *

s = Optimize()

# Adding mixer variables
R_1_1, R_1_2, R_1_3 = Ints('R_1_1 R_1_2 R_1_3')
R_2_1, R_2_2, R_2_3 = Ints('R_2_1 R_2_2 R_2_3')
R_3_1, R_3_2, R_3_3 = Ints('R_3_1 R_3_2 R_3_3')
R_4_1, R_4_2, R_4_3 = Ints('R_4_1 R_4_2 R_4_3')

# Creating reagent usage variable
x_1_1, x_1_2, x_1_3 = Ints('x_1_1 x_1_2 x_1_3')
x_2_1, x_2_2, x_2_3 = Ints('x_2_1 x_2_2 x_2_3')
x_3_1, x_3_2, x_3_3 = Ints('x_3_1 x_3_2 x_3_3')
x_4_1, x_4_2, x_4_3 = Ints('x_4_1 x_4_2 x_4_3')

# Creating intermediate fluid share variables
W_2_1 = Int('W_2_1')
W_3_2 = Int('W_3_2')
W_4_3 = Int('W_4_3')

# Adding nonnegativity constraints on reagent usage
s.add(And(x_1_1 >= 0, x_1_1 <= 4, x_1_2 >= 0, x_1_2 <= 4, x_1_3 >= 0, x_1_3 <= 4))
s.add(And(x_2_1 >= 0, x_2_1 <= 4, x_2_2 >= 0, x_2_2 <= 4, x_2_3 >= 0, x_2_3 <= 4))
s.add(And(x_3_1 >= 0, x_3_1 <= 4, x_3_2 >= 0, x_3_2 <= 4, x_3_3 >= 0, x_3_3 <= 4))
s.add(And(x_4_1 >= 0, x_4_1 <= 4, x_4_2 >= 0, x_4_2 <= 4, x_4_3 >= 0, x_4_3 <= 4))

# Adding nonnegativity constraints on sharing of intermediate fluids
s.add(And(W_2_1 > 0, W_2_1 <= 3, W_3_2 > 0, W_3_2 <= 3, W_4_3 > 0, W_4_3 <= 3))

# Adding nonnegativity constraints on total mixer units
s.add(x_1_1+x_1_2+x_1_3+W_2_1==4)
s.add(x_2_1+x_2_2+x_2_3+W_3_2==4)
s.add(x_3_1+x_3_2+x_3_3+W_4_3==4)
s.add(x_4_1+x_4_2+x_4_3==4)

# Adding mixer consistency constraint
s.add(R_1_1 == (4**3)*x_1_1+W_2_1*R_2_1)
s.add(R_1_2 == (4**3)*x_1_2+W_2_1*R_2_2)
s.add(R_1_3 == (4**3)*x_1_3+W_2_1*R_2_3)
s.add(R_2_1 == (4**2)*x_2_1+W_3_2*R_3_1)
s.add(R_2_2 == (4**2)*x_2_2+W_3_2*R_3_2)
s.add(R_2_3 == (4**2)*x_2_3+W_3_2*R_3_3)
s.add(R_3_1 == (4**1)*x_3_1+W_4_3*R_4_1)
s.add(R_3_2 == (4**1)*x_3_2+W_4_3*R_4_2)
s.add(R_3_3 == (4**1)*x_3_3+W_4_3*R_4_3)
s.add(R_4_1 == x_4_1)
s.add(R_4_2 == x_4_2)
s.add(R_4_3 == x_4_3)

# Adding base condition
s.add(0.35*(4**4) - R_1_1 <= 0.003*(4**4))
s.add(R_1_1 - 0.35*(4**4) <= 0.003*(4**4))
s.add(0.5*(4**4) - R_1_2 <= 0.003*(4**4))
s.add(R_1_2 - 0.5*(4**4) <= 0.003*(4**4))
s.add(0.15*(4**4) - R_1_3 <= 0.003*(4**4))
s.add(R_1_3 - 0.15*(4**4) <= 0.003*(4**4))

startTime = time.time()
fp = open('./z3OutputFiles/z3outputFile2','w')
if s.check() == sat:
	lst = s.model()
	for i in lst:
	    fp.write(str(i) + " = " + str(s.model()[i]) + '\n')
else:
	print('unsat')
	fp.write('unsat')
endTime = time.time()
executionTime = endTime - startTime
print("Execution Time = ",executionTime)
