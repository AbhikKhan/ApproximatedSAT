from z3 import *

s = Optimize()

# Variable declaration
A_5_4_R1 = Int("A_5_4_R1")
A_5_4_R4 = Int("A_5_4_R4")
A_5_4_R5 = Int("A_5_4_R5")
A_5_3_R1 = Int("A_5_3_R1")
A_5_3_R4 = Int("A_5_3_R4")
A_5_3_R5 = Int("A_5_3_R5")
A_4_3_R1 = Int("A_4_3_R1")
A_4_3_R4 = Int("A_4_3_R4")
A_4_3_R5 = Int("A_4_3_R5")

V_R1 = Int("V_R1")
V_R4 = Int("V_R4")
V_R5 = Int("V_R5")

d_0_R1  = Int("d_0_R1")
d_0_R4  = Int("d_0_R4")
d_0_R5  = Int("d_0_R5")
d_1_R1  = Int("d_1_R1")
d_1_R4  = Int("d_1_R4")
d_1_R5  = Int("d_1_R5")
d_2_R1  = Int("d_2_R1")
d_2_R4  = Int("d_2_R4")
d_2_R5  = Int("d_2_R5")

d_5_4_0_R1 = Int("d_5_4_0_R1")
d_5_4_1_R1 = Int("d_5_4_1_R1")
d_5_4_2_R1 = Int("d_5_4_2_R1")
d_5_4_0_R4 = Int("d_5_4_0_R4")
d_5_4_1_R4 = Int("d_5_4_1_R4")
d_5_4_2_R4 = Int("d_5_4_2_R4")
d_5_4_0_R5 = Int("d_5_4_0_R5")
d_5_4_1_R5 = Int("d_5_4_1_R5")
d_5_4_2_R5 = Int("d_5_4_2_R5")
d_5_3_0_R1 = Int("d_5_3_0_R1")
d_5_3_1_R1 = Int("d_5_3_1_R1")
d_5_3_2_R1 = Int("d_5_3_2_R1")
d_5_3_0_R4 = Int("d_5_3_0_R4")
d_5_3_1_R4 = Int("d_5_3_1_R4")
d_5_3_2_R4 = Int("d_5_3_2_R4")
d_5_3_0_R5 = Int("d_5_3_0_R5")
d_5_3_1_R5 = Int("d_5_3_1_R5")
d_5_3_2_R5 = Int("d_5_3_2_R5")
d_4_3_0_R1 = Int("d_4_3_0_R1")
d_4_3_1_R1 = Int("d_4_3_1_R1")
d_4_3_2_R1 = Int("d_4_3_2_R1")
d_4_3_0_R4 = Int("d_4_3_0_R4")
d_4_3_1_R4 = Int("d_4_3_1_R4")
d_4_3_2_R4 = Int("d_4_3_2_R4")
d_4_3_0_R5 = Int("d_4_3_0_R5")
d_4_3_1_R5 = Int("d_4_3_1_R5")
d_4_3_2_R5 = Int("d_4_3_2_R5")

# Number of cells in the mixture filled with Rt reagent
s.add(And(A_5_4_R1>=0, A_5_4_R1<=1, A_5_4_R4>=0, A_5_4_R4<=1, A_5_4_R5>=0, A_5_4_R5<=1))
s.add(And(A_5_3_R1>=0, A_5_3_R1<=1, A_5_3_R4>=0, A_5_3_R4<=1, A_5_3_R5>=0, A_5_3_R5<=1))
s.add(And(A_4_3_R1>=0, A_4_3_R1<=1, A_4_3_R4>=0, A_4_3_R4<=1, A_4_3_R5>=0, A_4_3_R5<=1))

s.add(A_5_4_R1 + A_5_3_R1 + A_4_3_R1 == V_R1)
s.add(A_5_4_R4 + A_5_3_R4 + A_4_3_R4 == V_R4)
s.add(A_5_4_R5 + A_5_3_R5 + A_4_3_R5 == V_R5)

# If a cell is filled with reagent Rt then no reagent Rk where k != t can be filled in that cell.
s.add(A_5_4_R1 + A_5_4_R4 + A_5_4_R5 == 1)
s.add(A_5_3_R1 + A_5_3_R4 + A_5_3_R5 == 1)
s.add(A_4_3_R1 + A_4_3_R4 + A_4_3_R5 == 1)

# To get traceability and connectivity.
s.add(If(And(A_5_4_R1 == 1, A_5_3_R1 == 0), (d_5_4_0_R1 == 1), (d_5_4_0_R1 == 0)))
s.add(If(And(A_5_3_R1 == 1, A_4_3_R1 + A_5_4_R1 == 0), (d_5_3_0_R1 == 1), (d_5_3_0_R1 == 0)))
s.add(If(And(A_4_3_R1 == 1, A_5_3_R1 == 0), (d_4_3_0_R1 == 1), (d_4_3_0_R1 == 0)))
s.add(If(And(A_5_4_R4 == 1, A_5_3_R4 == 0), (d_5_4_0_R4 == 1), (d_5_4_0_R4 == 0)))
s.add(If(And(A_5_3_R4 == 1, A_4_3_R4 + A_5_4_R4 == 0), (d_5_3_0_R4 == 1), (d_5_3_0_R4 == 0)))
s.add(If(And(A_4_3_R4 == 1, A_5_3_R4 == 0), (d_4_3_0_R4 == 1), (d_4_3_0_R4 == 0)))
s.add(If(And(A_5_4_R5 == 1, A_5_3_R5 == 0), (d_5_4_0_R5 == 1), (d_5_4_0_R5 == 0)))
s.add(If(And(A_5_3_R5 == 1, A_4_3_R5 + A_5_4_R5 == 0), (d_5_3_0_R5 == 1), (d_5_3_0_R5 == 0)))
s.add(If(And(A_4_3_R5 == 1, A_5_3_R5 == 0), (d_4_3_0_R5 == 1), (d_4_3_0_R5 == 0)))
s.add(If(And(A_5_4_R1 == 1, A_5_3_R1 == 1), (d_5_4_1_R1 == 1), (d_5_4_1_R1 == 0)))
s.add(If(And(A_5_3_R1 == 1, A_4_3_R1 + A_5_4_R1 == 1), (d_5_3_1_R1 == 1), (d_5_3_1_R1 == 0)))
s.add(If(And(A_4_3_R1 == 1, A_5_3_R1 == 1), (d_4_3_1_R1 == 1), (d_4_3_1_R1 == 0)))
s.add(If(And(A_5_4_R4 == 1, A_5_3_R4 == 1), (d_5_4_1_R4 == 1), (d_5_4_1_R4 == 0)))
s.add(If(And(A_5_3_R4 == 1, A_4_3_R4 + A_5_4_R4 == 1), (d_5_3_1_R4 == 1), (d_5_3_1_R4 == 0)))
s.add(If(And(A_4_3_R4 == 1, A_5_3_R4 == 1), (d_4_3_1_R4 == 1), (d_4_3_1_R4 == 0)))
s.add(If(And(A_5_4_R5 == 1, A_5_3_R5 == 1), (d_5_4_1_R5 == 1), (d_5_4_1_R5 == 0)))
s.add(If(And(A_5_3_R5 == 1, A_4_3_R5 + A_5_4_R5 == 1), (d_5_3_1_R5 == 1), (d_5_3_1_R5 == 0)))
s.add(If(And(A_4_3_R5 == 1, A_5_3_R5 == 1), (d_4_3_1_R5 == 1), (d_4_3_1_R5 == 0)))
s.add(If(And(A_5_3_R1 == 1, A_4_3_R1 + A_5_4_R1 == 2), (d_5_3_2_R1 == 1), (d_5_3_2_R1 == 0)))
s.add(If(And(A_5_3_R4 == 1, A_4_3_R4 + A_5_4_R4 == 2), (d_5_3_2_R4 == 1), (d_5_3_2_R4 == 0)))
s.add(If(And(A_5_3_R5 == 1, A_4_3_R5 + A_5_4_R5 == 2), (d_5_3_2_R5 == 1), (d_5_3_2_R5 == 0)))

s.add(d_5_4_0_R1 + d_5_3_0_R1 + d_4_3_0_R1 == d_0_R1)
s.add(d_5_4_1_R1 + d_5_3_1_R1 + d_4_3_1_R1 == d_1_R1)
s.add(d_5_4_2_R1 + d_5_3_2_R1 + d_4_3_2_R1 == d_2_R1)
s.add(d_5_4_0_R4 + d_5_3_0_R4 + d_4_3_0_R4 == d_0_R4)
s.add(d_5_4_1_R4 + d_5_3_1_R4 + d_4_3_1_R4 == d_1_R4)
s.add(d_5_4_2_R4 + d_5_3_2_R4 + d_4_3_2_R4 == d_2_R4)
s.add(d_5_4_0_R5 + d_5_3_0_R5 + d_4_3_0_R5 == d_0_R5)
s.add(d_5_4_1_R5 + d_5_3_1_R5 + d_4_3_1_R5 == d_1_R5)
s.add(d_5_4_2_R5 + d_5_3_2_R5 + d_4_3_2_R5 == d_2_R5)

s.add(Implies(V_R1 == 1, And(d_0_R1 == 1, d_1_R1 == 0, d_2_R1 == 0)))
s.add(Implies(V_R1 == 2, And(d_0_R1 == 0, d_1_R1 == 2, d_2_R1 == 0)))
s.add(Implies(V_R1 == 3, And(d_0_R1 == 0, d_1_R1 == 2, d_2_R1 == 1)))
s.add(Implies(V_R1 == 4, And(d_0_R1 == 0, d_1_R1 == 0, d_2_R1 == 4)))
s.add(Implies(V_R4 == 1, And(d_0_R4 == 1, d_1_R4 == 0, d_2_R4 == 0)))
s.add(Implies(V_R4 == 2, And(d_0_R4 == 0, d_1_R4 == 2, d_2_R4 == 0)))
s.add(Implies(V_R4 == 3, And(d_0_R4 == 0, d_1_R4 == 2, d_2_R4 == 1)))
s.add(Implies(V_R4 == 4, And(d_0_R4 == 0, d_1_R4 == 0, d_2_R4 == 4)))
s.add(Implies(V_R5 == 1, And(d_0_R5 == 1, d_1_R5 == 0, d_2_R5 == 0)))
s.add(Implies(V_R5 == 2, And(d_0_R5 == 0, d_1_R5 == 2, d_2_R5 == 0)))
s.add(Implies(V_R5 == 3, And(d_0_R5 == 0, d_1_R5 == 2, d_2_R5 == 1)))
s.add(Implies(V_R5 == 4, And(d_0_R5 == 0, d_1_R5 == 0, d_2_R5 == 4)))

s.add(And(V_R1 == 1, V_R4 == 1, V_R5 == 1))

if s.check() == unsat:
	print("Not possible to create traceable graph for all reagents")
else:
	fp = open('output0.txt','w')
	values = s.model()
	if values[A_5_4_R1] == 1:
		fp.write("5,4,R1\n")
	if values[A_5_4_R4] == 1:
		fp.write("5,4,R4\n")
	if values[A_5_4_R5] == 1:
		fp.write("5,4,R5\n")
	if values[A_5_3_R1] == 1:
		fp.write("5,3,R1\n")
	if values[A_5_3_R4] == 1:
		fp.write("5,3,R4\n")
	if values[A_5_3_R5] == 1:
		fp.write("5,3,R5\n")
	if values[A_4_3_R1] == 1:
		fp.write("4,3,R1\n")
	if values[A_4_3_R4] == 1:
		fp.write("4,3,R4\n")
	if values[A_4_3_R5] == 1:
		fp.write("4,3,R5\n")
