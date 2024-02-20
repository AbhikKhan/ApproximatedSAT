import sys
import time
sys.path.append("/home/sukanta/App/z3-master/build")
from z3 import *

s = Optimize()
R_1_1_1, R_1_1_2, R_1_1_3  = Ints('R_1_1_1 R_1_1_2 R_1_1_3')
r_1_1_1, r_1_1_2, r_1_1_3, s_1_1  = Ints('r_1_1_1 r_1_1_2 r_1_1_3 s_1_1')# Added reagent variables
R_2_1_1, R_2_1_2, R_2_1_3  = Ints('R_2_1_1 R_2_1_2 R_2_1_3')
r_2_1_1, r_2_1_2, r_2_1_3, s_2_1  = Ints('r_2_1_1 r_2_1_2 r_2_1_3 s_2_1')# Added reagent variables
R_2_2_1, R_2_2_2, R_2_2_3  = Ints('R_2_2_1 R_2_2_2 R_2_2_3')
r_2_2_1, r_2_2_2, r_2_2_3, s_2_2  = Ints('r_2_2_1 r_2_2_2 r_2_2_3 s_2_2')# Added reagent variables
R_3_1_1, R_3_1_2, R_3_1_3  = Ints('R_3_1_1 R_3_1_2 R_3_1_3')
r_3_1_1, r_3_1_2, r_3_1_3, s_3_1  = Ints('r_3_1_1 r_3_1_2 r_3_1_3 s_3_1')# Added reagent variables
w_2_1_1_1, w_2_2_1_1, w_3_1_2_2  = Ints('w_2_1_1_1 w_2_2_1_1 w_3_1_2_2')# Added edgeVariables

t1 = Int('t1')
t2 = Int('t2')
t3 = Int('t3')
t4 = Int('t4')
t5 = Int('t5')
t6 = Int('t6')
s.add(16*r_1_1_1 + 4*t1 + 1*t2  == R_1_1_1)
s.add(16*r_1_1_2 + 4*t3 + 1*t4  == R_1_1_2)
s.add(16*r_1_1_3 + 4*t5 + 1*t6  == R_1_1_3)

s.add(Implies((w_2_1_1_1 == 0), (t1 == 0)))
s.add(Implies((w_2_1_1_1 == 1), (t1 == 1*R_2_1_1)))
s.add(Implies((w_2_1_1_1 == 2), (t1 == 2*R_2_1_1)))
s.add(Implies((w_2_1_1_1 == 3), (t1 == 3*R_2_1_1)))

s.add(Implies((w_2_2_1_1 == 0), (t2 == 0)))
s.add(Implies((w_2_2_1_1 == 1), (t2 == 1*R_2_2_1)))
s.add(Implies((w_2_2_1_1 == 2), (t2 == 2*R_2_2_1)))
s.add(Implies((w_2_2_1_1 == 3), (t2 == 3*R_2_2_1)))

s.add(Implies((w_2_1_1_1 == 0), (t3 == 0)))
s.add(Implies((w_2_1_1_1 == 1), (t3 == 1*R_2_1_2)))
s.add(Implies((w_2_1_1_1 == 2), (t3 == 2*R_2_1_2)))
s.add(Implies((w_2_1_1_1 == 3), (t3 == 3*R_2_1_2)))

s.add(Implies((w_2_2_1_1 == 0), (t4 == 0)))
s.add(Implies((w_2_2_1_1 == 1), (t4 == 1*R_2_2_2)))
s.add(Implies((w_2_2_1_1 == 2), (t4 == 2*R_2_2_2)))
s.add(Implies((w_2_2_1_1 == 3), (t4 == 3*R_2_2_2)))

s.add(Implies((w_2_1_1_1 == 0), (t5 == 0)))
s.add(Implies((w_2_1_1_1 == 1), (t5 == 1*R_2_1_3)))
s.add(Implies((w_2_1_1_1 == 2), (t5 == 2*R_2_1_3)))
s.add(Implies((w_2_1_1_1 == 3), (t5 == 3*R_2_1_3)))

s.add(Implies((w_2_2_1_1 == 0), (t6 == 0)))
s.add(Implies((w_2_2_1_1 == 1), (t6 == 1*R_2_2_3)))
s.add(Implies((w_2_2_1_1 == 2), (t6 == 2*R_2_2_3)))
s.add(Implies((w_2_2_1_1 == 3), (t6 == 3*R_2_2_3)))

s.add(1*r_2_1_1  == R_2_1_1)
s.add(1*r_2_1_2  == R_2_1_2)
s.add(1*r_2_1_3  == R_2_1_3)

t7 = Int('t7')
t8 = Int('t8')
t9 = Int('t9')
s.add(4*r_2_2_1 + 1*t7  == R_2_2_1)
s.add(4*r_2_2_2 + 1*t8  == R_2_2_2)
s.add(4*r_2_2_3 + 1*t9  == R_2_2_3)

s.add(Implies((w_3_1_2_2 == 0), (t7 == 0)))
s.add(Implies((w_3_1_2_2 == 1), (t7 == 1*R_3_1_1)))
s.add(Implies((w_3_1_2_2 == 2), (t7 == 2*R_3_1_1)))
s.add(Implies((w_3_1_2_2 == 3), (t7 == 3*R_3_1_1)))

s.add(Implies((w_3_1_2_2 == 0), (t8 == 0)))
s.add(Implies((w_3_1_2_2 == 1), (t8 == 1*R_3_1_2)))
s.add(Implies((w_3_1_2_2 == 2), (t8 == 2*R_3_1_2)))
s.add(Implies((w_3_1_2_2 == 3), (t8 == 3*R_3_1_2)))

s.add(Implies((w_3_1_2_2 == 0), (t9 == 0)))
s.add(Implies((w_3_1_2_2 == 1), (t9 == 1*R_3_1_3)))
s.add(Implies((w_3_1_2_2 == 2), (t9 == 2*R_3_1_3)))
s.add(Implies((w_3_1_2_2 == 3), (t9 == 3*R_3_1_3)))

s.add(1*r_3_1_1  == R_3_1_1)
s.add(1*r_3_1_2  == R_3_1_2)
s.add(1*r_3_1_3  == R_3_1_3)

waste = Int('waste')
s.add(waste == 4-w_2_1_1_1+4-w_2_2_1_1+4-w_3_1_2_2)
s.add(Or(r_1_1_1 + r_1_1_2 + r_1_1_3 + w_2_1_1_1 + w_2_2_1_1  == 4, r_1_1_1 + r_1_1_2 + r_1_1_3 + w_2_1_1_1 + w_2_2_1_1  == 0))
s.add(Or(r_2_1_1 + r_2_1_2 + r_2_1_3  == 4, r_2_1_1 + r_2_1_2 + r_2_1_3  == 0))
s.add(w_2_1_1_1  <= 4)
s.add(Or(r_2_2_1 + r_2_2_2 + r_2_2_3 + w_3_1_2_2  == 4, r_2_2_1 + r_2_2_2 + r_2_2_3 + w_3_1_2_2  == 0))
s.add(w_2_2_1_1  <= 4)
s.add(Or(r_3_1_1 + r_3_1_2 + r_3_1_3  == 4, r_3_1_1 + r_3_1_2 + r_3_1_3  == 0))
s.add(w_3_1_2_2  <= 4)
s.add(And(r_1_1_1 >= 0, r_1_1_1 <= 3, r_1_1_2 >= 0, r_1_1_2 <= 3, r_1_1_3 >= 0, r_1_1_3 <= 3))
s.add(And(r_2_1_1 >= 0, r_2_1_1 <= 3, r_2_1_2 >= 0, r_2_1_2 <= 3, r_2_1_3 >= 0, r_2_1_3 <= 3))
s.add(And(r_2_2_1 >= 0, r_2_2_1 <= 3, r_2_2_2 >= 0, r_2_2_2 <= 3, r_2_2_3 >= 0, r_2_2_3 <= 3))
s.add(And(r_3_1_1 >= 0, r_3_1_1 <= 3, r_3_1_2 >= 0, r_3_1_2 <= 3, r_3_1_3 >= 0, r_3_1_3 <= 3))
s.add(And(w_2_1_1_1 >= 0, w_2_1_1_1 <= 3, w_2_2_1_1 >= 0, w_2_2_1_1 <= 3, w_3_1_2_2 >= 0, w_3_1_2_2 <= 3))
s.add(And(R_1_1_1 == 13, R_1_1_2 == 29, R_1_1_3 == 22))


totalReagents = s.minimize(r_1_1_1 + r_1_1_2 + r_1_1_3 + r_2_1_1 + r_2_1_2 + r_2_1_3 + r_2_2_1 + r_2_2_2 + r_2_2_3 + r_3_1_1 + r_3_1_2 + r_3_1_3 )
startTime = time.time()
if s.check() == sat:
	print("Total reagents = ", totalReagents.value())
	fp = open('z3opFile','w')
	lst = s.model()
	for i in lst:
	    fp.write(str(i) + " = " + str(s.model()[i]) + '\n')
else:
	print('unsat')
endTime = time.time()
executionTime = endTime - startTime
print("Execution Time = ",executionTime)
