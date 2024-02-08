import sys
import time
from z3 import *

s = Optimize()

# Adding mixer variables
R_1_1, R_1_2, R_1_3, R_1_4, R_1_5 = Ints('R_1_1 R_1_2 R_1_3 R_1_4 R_1_5')
R_2_1, R_2_2, R_2_3, R_2_4, R_2_5 = Ints('R_2_1 R_2_2 R_2_3 R_2_4 R_2_5')
R_3_1, R_3_2, R_3_3, R_3_4, R_3_5 = Ints('R_3_1 R_3_2 R_3_3 R_3_4 R_3_5')
R_4_1, R_4_2, R_4_3, R_4_4, R_4_5 = Ints('R_4_1 R_4_2 R_4_3 R_4_4 R_4_5')
R_5_1, R_5_2, R_5_3, R_5_4, R_5_5 = Ints('R_5_1 R_5_2 R_5_3 R_5_4 R_5_5')

# Creating reagent usage variable
x_1_1, x_1_2, x_1_3, x_1_4, x_1_5 = Ints('x_1_1 x_1_2 x_1_3 x_1_4 x_1_5')
x_2_1, x_2_2, x_2_3, x_2_4, x_2_5 = Ints('x_2_1 x_2_2 x_2_3 x_2_4 x_2_5')
x_3_1, x_3_2, x_3_3, x_3_4, x_3_5 = Ints('x_3_1 x_3_2 x_3_3 x_3_4 x_3_5')
x_4_1, x_4_2, x_4_3, x_4_4, x_4_5 = Ints('x_4_1 x_4_2 x_4_3 x_4_4 x_4_5')
x_5_1, x_5_2, x_5_3, x_5_4, x_5_5 = Ints('x_5_1 x_5_2 x_5_3 x_5_4 x_5_5')

# Creating intermediate fluid share variables
W_2_1 = Int('W_2_1')
W_3_2 = Int('W_3_2')
W_4_3 = Int('W_4_3')
W_5_4 = Int('W_5_4')

# Adding nonnegativity constraints on reagent usage
s.add(And(x_1_1 >= 0, x_1_1 <= 4, x_1_2 >= 0, x_1_2 <= 4, x_1_3 >= 0, x_1_3 <= 4, x_1_4 >= 0, x_1_4 <= 4, x_1_5 >= 0, x_1_5 <= 4))
s.add(And(x_2_1 >= 0, x_2_1 <= 4, x_2_2 >= 0, x_2_2 <= 4, x_2_3 >= 0, x_2_3 <= 4, x_2_4 >= 0, x_2_4 <= 4, x_2_5 >= 0, x_2_5 <= 4))
s.add(And(x_3_1 >= 0, x_3_1 <= 4, x_3_2 >= 0, x_3_2 <= 4, x_3_3 >= 0, x_3_3 <= 4, x_3_4 >= 0, x_3_4 <= 4, x_3_5 >= 0, x_3_5 <= 4))
s.add(And(x_4_1 >= 0, x_4_1 <= 4, x_4_2 >= 0, x_4_2 <= 4, x_4_3 >= 0, x_4_3 <= 4, x_4_4 >= 0, x_4_4 <= 4, x_4_5 >= 0, x_4_5 <= 4))
s.add(And(x_5_1 >= 0, x_5_1 <= 4, x_5_2 >= 0, x_5_2 <= 4, x_5_3 >= 0, x_5_3 <= 4, x_5_4 >= 0, x_5_4 <= 4, x_5_5 >= 0, x_5_5 <= 4))

# Adding nonnegativity constraints on sharing of intermediate fluids
s.add(And(W_2_1 > 0, W_2_1 <= 3, W_3_2 > 0, W_3_2 <= 3, W_4_3 > 0, W_4_3 <= 3, W_5_4 > 0, W_5_4 <= 3))

# Adding nonnegativity constraints on total mixer units
s.add(x_1_1+x_1_2+x_1_3+x_1_4+x_1_5+W_2_1==4)
s.add(x_2_1+x_2_2+x_2_3+x_2_4+x_2_5+W_3_2==4)
s.add(x_3_1+x_3_2+x_3_3+x_3_4+x_3_5+W_4_3==4)
s.add(x_4_1+x_4_2+x_4_3+x_4_4+x_4_5+W_5_4==4)
s.add(x_5_1+x_5_2+x_5_3+x_5_4+x_5_5==4)

# Adding mixer consistency constraint
s.add(R_1_1 == (4**4)*x_1_1+W_2_1*R_2_1)
s.add(R_1_2 == (4**4)*x_1_2+W_2_1*R_2_2)
s.add(R_1_3 == (4**4)*x_1_3+W_2_1*R_2_3)
s.add(R_1_4 == (4**4)*x_1_4+W_2_1*R_2_4)
s.add(R_1_5 == (4**4)*x_1_5+W_2_1*R_2_5)
s.add(R_2_1 == (4**3)*x_2_1+W_3_2*R_3_1)
s.add(R_2_2 == (4**3)*x_2_2+W_3_2*R_3_2)
s.add(R_2_3 == (4**3)*x_2_3+W_3_2*R_3_3)
s.add(R_2_4 == (4**3)*x_2_4+W_3_2*R_3_4)
s.add(R_2_5 == (4**3)*x_2_5+W_3_2*R_3_5)
s.add(R_3_1 == (4**2)*x_3_1+W_4_3*R_4_1)
s.add(R_3_2 == (4**2)*x_3_2+W_4_3*R_4_2)
s.add(R_3_3 == (4**2)*x_3_3+W_4_3*R_4_3)
s.add(R_3_4 == (4**2)*x_3_4+W_4_3*R_4_4)
s.add(R_3_5 == (4**2)*x_3_5+W_4_3*R_4_5)
s.add(R_4_1 == (4**1)*x_4_1+W_5_4*R_5_1)
s.add(R_4_2 == (4**1)*x_4_2+W_5_4*R_5_2)
s.add(R_4_3 == (4**1)*x_4_3+W_5_4*R_5_3)
s.add(R_4_4 == (4**1)*x_4_4+W_5_4*R_5_4)
s.add(R_4_5 == (4**1)*x_4_5+W_5_4*R_5_5)
s.add(R_5_1 == x_5_1)
s.add(R_5_2 == x_5_2)
s.add(R_5_3 == x_5_3)
s.add(R_5_4 == x_5_4)
s.add(R_5_5 == x_5_5)

# Adding base condition
s.add(0.208984375*(4**5) - R_1_1 <= 0.00396*(4**5))
s.add(R_1_1 - 0.208984375*(4**5) <= 0.00396*(4**5))
s.add(0.21875*(4**5) - R_1_2 <= 0.00396*(4**5))
s.add(R_1_2 - 0.21875*(4**5) <= 0.00396*(4**5))
s.add(0.2177734375*(4**5) - R_1_3 <= 0.00396*(4**5))
s.add(R_1_3 - 0.2177734375*(4**5) <= 0.00396*(4**5))
s.add(0.1162109375*(4**5) - R_1_4 <= 0.00396*(4**5))
s.add(R_1_4 - 0.1162109375*(4**5) <= 0.00396*(4**5))
s.add(0.23828125*(4**5) - R_1_5 <= 0.00396*(4**5))
s.add(R_1_5 - 0.23828125*(4**5) <= 0.00396*(4**5))

startTime = time.time()
fp = open('./z3OutputFiles/z3outputFile1029','w')
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
