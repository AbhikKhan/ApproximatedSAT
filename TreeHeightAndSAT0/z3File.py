from z3 import *

s = Optimize()

# Variable declaration
A_4_4_R1 = Int("A_4_4_R1")
A_4_4_R5 = Int("A_4_4_R5")
A_4_5_R1 = Int("A_4_5_R1")
A_4_5_R5 = Int("A_4_5_R5")

V_R1 = Int("V_R1")
V_R5 = Int("V_R5")

d_0_R1  = Int("d_0_R1")
d_0_R5  = Int("d_0_R5")
d_1_R1  = Int("d_1_R1")
d_1_R5  = Int("d_1_R5")
d_2_R1  = Int("d_2_R1")
d_2_R5  = Int("d_2_R5")

d_4_4_0_R1 = Int("d_4_4_0_R1")
d_4_4_1_R1 = Int("d_4_4_1_R1")
d_4_4_2_R1 = Int("d_4_4_2_R1")
d_4_4_0_R5 = Int("d_4_4_0_R5")
d_4_4_1_R5 = Int("d_4_4_1_R5")
d_4_4_2_R5 = Int("d_4_4_2_R5")
d_4_5_0_R1 = Int("d_4_5_0_R1")
d_4_5_1_R1 = Int("d_4_5_1_R1")
d_4_5_2_R1 = Int("d_4_5_2_R1")
d_4_5_0_R5 = Int("d_4_5_0_R5")
d_4_5_1_R5 = Int("d_4_5_1_R5")
d_4_5_2_R5 = Int("d_4_5_2_R5")

# Number of cells in the mixture filled with Rt reagent
s.add(And(A_4_4_R1>=0, A_4_4_R1<=1, A_4_4_R5>=0, A_4_4_R5<=1))
s.add(And(A_4_5_R1>=0, A_4_5_R1<=1, A_4_5_R5>=0, A_4_5_R5<=1))

s.add(A_4_4_R1 + A_4_5_R1 == V_R1)
s.add(A_4_4_R5 + A_4_5_R5 == V_R5)

# If a cell is filled with reagent Rt then no reagent Rk where k != t can be filled in that cell.
s.add(A_4_4_R1 + A_4_4_R5 == 1)
s.add(A_4_5_R1 + A_4_5_R5 == 1)

# To get traceability and connectivity.
s.add(If(And(A_4_4_R1 == 1, A_4_5_R1 == 0), (d_4_4_0_R1 == 1), (d_4_4_0_R1 == 0)))
s.add(If(And(A_4_5_R1 == 1, A_4_4_R1 == 0), (d_4_5_0_R1 == 1), (d_4_5_0_R1 == 0)))
s.add(If(And(A_4_4_R5 == 1, A_4_5_R5 == 0), (d_4_4_0_R5 == 1), (d_4_4_0_R5 == 0)))
s.add(If(And(A_4_5_R5 == 1, A_4_4_R5 == 0), (d_4_5_0_R5 == 1), (d_4_5_0_R5 == 0)))
s.add(If(And(A_4_4_R1 == 1, A_4_5_R1 == 1), (d_4_4_1_R1 == 1), (d_4_4_1_R1 == 0)))
s.add(If(And(A_4_5_R1 == 1, A_4_4_R1 == 1), (d_4_5_1_R1 == 1), (d_4_5_1_R1 == 0)))
s.add(If(And(A_4_4_R5 == 1, A_4_5_R5 == 1), (d_4_4_1_R5 == 1), (d_4_4_1_R5 == 0)))
s.add(If(And(A_4_5_R5 == 1, A_4_4_R5 == 1), (d_4_5_1_R5 == 1), (d_4_5_1_R5 == 0)))

s.add(d_4_4_0_R1 + d_4_5_0_R1 == d_0_R1)
s.add(d_4_4_1_R1 + d_4_5_1_R1 == d_1_R1)
s.add(d_4_4_2_R1 + d_4_5_2_R1 == d_2_R1)
s.add(d_4_4_0_R5 + d_4_5_0_R5 == d_0_R5)
s.add(d_4_4_1_R5 + d_4_5_1_R5 == d_1_R5)
s.add(d_4_4_2_R5 + d_4_5_2_R5 == d_2_R5)

s.add(Implies(V_R1 == 1, And(d_0_R1 == 1, d_1_R1 == 0, d_2_R1 == 0)))
s.add(Implies(V_R1 == 2, And(d_0_R1 == 0, d_1_R1 == 2, d_2_R1 == 0)))
s.add(Implies(V_R1 == 3, And(d_0_R1 == 0, d_1_R1 == 2, d_2_R1 == 1)))
s.add(Implies(V_R1 == 4, And(d_0_R1 == 0, d_1_R1 == 0, d_2_R1 == 4)))
s.add(Implies(V_R5 == 1, And(d_0_R5 == 1, d_1_R5 == 0, d_2_R5 == 0)))
s.add(Implies(V_R5 == 2, And(d_0_R5 == 0, d_1_R5 == 2, d_2_R5 == 0)))
s.add(Implies(V_R5 == 3, And(d_0_R5 == 0, d_1_R5 == 2, d_2_R5 == 1)))
s.add(Implies(V_R5 == 4, And(d_0_R5 == 0, d_1_R5 == 0, d_2_R5 == 4)))

s.add(And(V_R1 == 1, V_R5 == 1))

if s.check() == unsat:
	print("Not possible to create traceable graph for all reagents")
else:
	fp = open('output0.txt','w')
	values = s.model()
	if values[A_4_4_R1] == 1:
		fp.write("4,4,R1\n")
	if values[A_4_4_R5] == 1:
		fp.write("4,4,R5\n")
	if values[A_4_5_R1] == 1:
		fp.write("4,5,R1\n")
	if values[A_4_5_R5] == 1:
		fp.write("4,5,R5\n")
