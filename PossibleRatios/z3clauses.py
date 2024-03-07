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

t3013 = Int('t3013')
t3014 = Int('t3014')
t3015 = Int('t3015')
t3016 = Int('t3016')
t3017 = Int('t3017')
t3018 = Int('t3018')
s.add(16*r_1_1_1 + 4*t3013 + 1*t3014  == R_1_1_1)
s.add(16*r_1_1_2 + 4*t3015 + 1*t3016  == R_1_1_2)
s.add(16*r_1_1_3 + 4*t3017 + 1*t3018  == R_1_1_3)

s.add(Implies((w_2_1_1_1 == 0), (t3013 == 0)))
s.add(Implies((w_2_1_1_1 == 1), (t3013 == 1*R_2_1_1)))
s.add(Implies((w_2_1_1_1 == 2), (t3013 == 2*R_2_1_1)))
s.add(Implies((w_2_1_1_1 == 3), (t3013 == 3*R_2_1_1)))

s.add(Implies((w_2_2_1_1 == 0), (t3014 == 0)))
s.add(Implies((w_2_2_1_1 == 1), (t3014 == 1*R_2_2_1)))
s.add(Implies((w_2_2_1_1 == 2), (t3014 == 2*R_2_2_1)))
s.add(Implies((w_2_2_1_1 == 3), (t3014 == 3*R_2_2_1)))

s.add(Implies((w_2_1_1_1 == 0), (t3015 == 0)))
s.add(Implies((w_2_1_1_1 == 1), (t3015 == 1*R_2_1_2)))
s.add(Implies((w_2_1_1_1 == 2), (t3015 == 2*R_2_1_2)))
s.add(Implies((w_2_1_1_1 == 3), (t3015 == 3*R_2_1_2)))

s.add(Implies((w_2_2_1_1 == 0), (t3016 == 0)))
s.add(Implies((w_2_2_1_1 == 1), (t3016 == 1*R_2_2_2)))
s.add(Implies((w_2_2_1_1 == 2), (t3016 == 2*R_2_2_2)))
s.add(Implies((w_2_2_1_1 == 3), (t3016 == 3*R_2_2_2)))

s.add(Implies((w_2_1_1_1 == 0), (t3017 == 0)))
s.add(Implies((w_2_1_1_1 == 1), (t3017 == 1*R_2_1_3)))
s.add(Implies((w_2_1_1_1 == 2), (t3017 == 2*R_2_1_3)))
s.add(Implies((w_2_1_1_1 == 3), (t3017 == 3*R_2_1_3)))

s.add(Implies((w_2_2_1_1 == 0), (t3018 == 0)))
s.add(Implies((w_2_2_1_1 == 1), (t3018 == 1*R_2_2_3)))
s.add(Implies((w_2_2_1_1 == 2), (t3018 == 2*R_2_2_3)))
s.add(Implies((w_2_2_1_1 == 3), (t3018 == 3*R_2_2_3)))

s.add(1*r_2_1_1  == R_2_1_1)
s.add(1*r_2_1_2  == R_2_1_2)
s.add(1*r_2_1_3  == R_2_1_3)

t3019 = Int('t3019')
t3020 = Int('t3020')
t3021 = Int('t3021')
s.add(4*r_2_2_1 + 1*t3019  == R_2_2_1)
s.add(4*r_2_2_2 + 1*t3020  == R_2_2_2)
s.add(4*r_2_2_3 + 1*t3021  == R_2_2_3)

s.add(Implies((w_3_1_2_2 == 0), (t3019 == 0)))
s.add(Implies((w_3_1_2_2 == 1), (t3019 == 1*R_3_1_1)))
s.add(Implies((w_3_1_2_2 == 2), (t3019 == 2*R_3_1_1)))
s.add(Implies((w_3_1_2_2 == 3), (t3019 == 3*R_3_1_1)))

s.add(Implies((w_3_1_2_2 == 0), (t3020 == 0)))
s.add(Implies((w_3_1_2_2 == 1), (t3020 == 1*R_3_1_2)))
s.add(Implies((w_3_1_2_2 == 2), (t3020 == 2*R_3_1_2)))
s.add(Implies((w_3_1_2_2 == 3), (t3020 == 3*R_3_1_2)))

s.add(Implies((w_3_1_2_2 == 0), (t3021 == 0)))
s.add(Implies((w_3_1_2_2 == 1), (t3021 == 1*R_3_1_3)))
s.add(Implies((w_3_1_2_2 == 2), (t3021 == 2*R_3_1_3)))
s.add(Implies((w_3_1_2_2 == 3), (t3021 == 3*R_3_1_3)))

s.add(1*r_3_1_1  == R_3_1_1)
s.add(1*r_3_1_2  == R_3_1_2)
s.add(1*r_3_1_3  == R_3_1_3)

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
s.add(And(R_1_1_1 == 27, R_1_1_2 == 25, R_1_1_3 == 12))


totalReagents = s.minimize(r_1_1_1 + r_1_1_2 + r_1_1_3 + r_2_1_1 + r_2_1_2 + r_2_1_3 + r_2_2_1 + r_2_2_2 + r_2_2_3 + r_3_1_1 + r_3_1_2 + r_3_1_3 )
startTime = time.time()
fp = open('z3opFile','w')
if s.check() == sat:
	print("Total reagents = ", totalReagents.value())
	lst = s.model()
	for i in lst:
	    fp.write(str(i) + " = " + str(s.model()[i]) + '\n')
else:
	fp.write('unsat')
	print('unsat')
endTime = time.time()
executionTime = endTime - startTime
print("Execution Time = ",executionTime)
