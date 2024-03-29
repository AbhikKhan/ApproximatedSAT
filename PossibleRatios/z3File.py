from z3 import *

s = Optimize()

# Variable declaration
A_7_2_r2 = Int("A_7_2_r2")
A_7_2_r4 = Int("A_7_2_r4")
A_7_2_r5 = Int("A_7_2_r5")
A_8_2_r2 = Int("A_8_2_r2")
A_8_2_r4 = Int("A_8_2_r4")
A_8_2_r5 = Int("A_8_2_r5")
A_8_1_r2 = Int("A_8_1_r2")
A_8_1_r4 = Int("A_8_1_r4")
A_8_1_r5 = Int("A_8_1_r5")
A_7_1_r2 = Int("A_7_1_r2")
A_7_1_r4 = Int("A_7_1_r4")
A_7_1_r5 = Int("A_7_1_r5")

V_r2 = Int("V_r2")
V_r4 = Int("V_r4")
V_r5 = Int("V_r5")

d_0_r2  = Int("d_0_r2")
d_0_r4  = Int("d_0_r4")
d_0_r5  = Int("d_0_r5")
d_1_r2  = Int("d_1_r2")
d_1_r4  = Int("d_1_r4")
d_1_r5  = Int("d_1_r5")
d_2_r2  = Int("d_2_r2")
d_2_r4  = Int("d_2_r4")
d_2_r5  = Int("d_2_r5")

d_7_2_0_r2 = Int("d_7_2_0_r2")
d_7_2_1_r2 = Int("d_7_2_1_r2")
d_7_2_2_r2 = Int("d_7_2_2_r2")
d_7_2_0_r4 = Int("d_7_2_0_r4")
d_7_2_1_r4 = Int("d_7_2_1_r4")
d_7_2_2_r4 = Int("d_7_2_2_r4")
d_7_2_0_r5 = Int("d_7_2_0_r5")
d_7_2_1_r5 = Int("d_7_2_1_r5")
d_7_2_2_r5 = Int("d_7_2_2_r5")
d_8_2_0_r2 = Int("d_8_2_0_r2")
d_8_2_1_r2 = Int("d_8_2_1_r2")
d_8_2_2_r2 = Int("d_8_2_2_r2")
d_8_2_0_r4 = Int("d_8_2_0_r4")
d_8_2_1_r4 = Int("d_8_2_1_r4")
d_8_2_2_r4 = Int("d_8_2_2_r4")
d_8_2_0_r5 = Int("d_8_2_0_r5")
d_8_2_1_r5 = Int("d_8_2_1_r5")
d_8_2_2_r5 = Int("d_8_2_2_r5")
d_8_1_0_r2 = Int("d_8_1_0_r2")
d_8_1_1_r2 = Int("d_8_1_1_r2")
d_8_1_2_r2 = Int("d_8_1_2_r2")
d_8_1_0_r4 = Int("d_8_1_0_r4")
d_8_1_1_r4 = Int("d_8_1_1_r4")
d_8_1_2_r4 = Int("d_8_1_2_r4")
d_8_1_0_r5 = Int("d_8_1_0_r5")
d_8_1_1_r5 = Int("d_8_1_1_r5")
d_8_1_2_r5 = Int("d_8_1_2_r5")
d_7_1_0_r2 = Int("d_7_1_0_r2")
d_7_1_1_r2 = Int("d_7_1_1_r2")
d_7_1_2_r2 = Int("d_7_1_2_r2")
d_7_1_0_r4 = Int("d_7_1_0_r4")
d_7_1_1_r4 = Int("d_7_1_1_r4")
d_7_1_2_r4 = Int("d_7_1_2_r4")
d_7_1_0_r5 = Int("d_7_1_0_r5")
d_7_1_1_r5 = Int("d_7_1_1_r5")
d_7_1_2_r5 = Int("d_7_1_2_r5")

# Number of cells in the mixture filled with Rt reagent
s.add(And(A_7_2_r2>=0, A_7_2_r2<=1, A_7_2_r4>=0, A_7_2_r4<=1, A_7_2_r5>=0, A_7_2_r5<=1))
s.add(And(A_8_2_r2>=0, A_8_2_r2<=1, A_8_2_r4>=0, A_8_2_r4<=1, A_8_2_r5>=0, A_8_2_r5<=1))
s.add(And(A_8_1_r2>=0, A_8_1_r2<=1, A_8_1_r4>=0, A_8_1_r4<=1, A_8_1_r5>=0, A_8_1_r5<=1))
s.add(And(A_7_1_r2>=0, A_7_1_r2<=1, A_7_1_r4>=0, A_7_1_r4<=1, A_7_1_r5>=0, A_7_1_r5<=1))

s.add(A_7_2_r2 + A_8_2_r2 + A_8_1_r2 + A_7_1_r2 == V_r2)
s.add(A_7_2_r4 + A_8_2_r4 + A_8_1_r4 + A_7_1_r4 == V_r4)
s.add(A_7_2_r5 + A_8_2_r5 + A_8_1_r5 + A_7_1_r5 == V_r5)

# If a cell is filled with reagent Rt then no reagent Rk where k != t can be filled in that cell.
s.add(A_7_2_r2 + A_7_2_r4 + A_7_2_r5 == 1)
s.add(A_8_2_r2 + A_8_2_r4 + A_8_2_r5 == 1)
s.add(A_8_1_r2 + A_8_1_r4 + A_8_1_r5 == 1)
s.add(A_7_1_r2 + A_7_1_r4 + A_7_1_r5 == 1)

# To get traceability and connectivity.
s.add(If(And(A_7_2_r2 == 1, A_8_2_r2 + A_7_1_r2 == 0), (d_7_2_0_r2 == 1), (d_7_2_0_r2 == 0)))
s.add(If(And(A_8_2_r2 == 1, A_7_2_r2 + A_8_1_r2 == 0), (d_8_2_0_r2 == 1), (d_8_2_0_r2 == 0)))
s.add(If(And(A_8_1_r2 == 1, A_7_1_r2 + A_8_2_r2 == 0), (d_8_1_0_r2 == 1), (d_8_1_0_r2 == 0)))
s.add(If(And(A_7_1_r2 == 1, A_7_2_r2 + A_8_1_r2 == 0), (d_7_1_0_r2 == 1), (d_7_1_0_r2 == 0)))
s.add(If(And(A_7_2_r4 == 1, A_8_2_r4 + A_7_1_r4 == 0), (d_7_2_0_r4 == 1), (d_7_2_0_r4 == 0)))
s.add(If(And(A_8_2_r4 == 1, A_7_2_r4 + A_8_1_r4 == 0), (d_8_2_0_r4 == 1), (d_8_2_0_r4 == 0)))
s.add(If(And(A_8_1_r4 == 1, A_7_1_r4 + A_8_2_r4 == 0), (d_8_1_0_r4 == 1), (d_8_1_0_r4 == 0)))
s.add(If(And(A_7_1_r4 == 1, A_7_2_r4 + A_8_1_r4 == 0), (d_7_1_0_r4 == 1), (d_7_1_0_r4 == 0)))
s.add(If(And(A_7_2_r5 == 1, A_8_2_r5 + A_7_1_r5 == 0), (d_7_2_0_r5 == 1), (d_7_2_0_r5 == 0)))
s.add(If(And(A_8_2_r5 == 1, A_7_2_r5 + A_8_1_r5 == 0), (d_8_2_0_r5 == 1), (d_8_2_0_r5 == 0)))
s.add(If(And(A_8_1_r5 == 1, A_7_1_r5 + A_8_2_r5 == 0), (d_8_1_0_r5 == 1), (d_8_1_0_r5 == 0)))
s.add(If(And(A_7_1_r5 == 1, A_7_2_r5 + A_8_1_r5 == 0), (d_7_1_0_r5 == 1), (d_7_1_0_r5 == 0)))
s.add(If(And(A_7_2_r2 == 1, A_8_2_r2 + A_7_1_r2 == 1), (d_7_2_1_r2 == 1), (d_7_2_1_r2 == 0)))
s.add(If(And(A_8_2_r2 == 1, A_7_2_r2 + A_8_1_r2 == 1), (d_8_2_1_r2 == 1), (d_8_2_1_r2 == 0)))
s.add(If(And(A_8_1_r2 == 1, A_7_1_r2 + A_8_2_r2 == 1), (d_8_1_1_r2 == 1), (d_8_1_1_r2 == 0)))
s.add(If(And(A_7_1_r2 == 1, A_7_2_r2 + A_8_1_r2 == 1), (d_7_1_1_r2 == 1), (d_7_1_1_r2 == 0)))
s.add(If(And(A_7_2_r4 == 1, A_8_2_r4 + A_7_1_r4 == 1), (d_7_2_1_r4 == 1), (d_7_2_1_r4 == 0)))
s.add(If(And(A_8_2_r4 == 1, A_7_2_r4 + A_8_1_r4 == 1), (d_8_2_1_r4 == 1), (d_8_2_1_r4 == 0)))
s.add(If(And(A_8_1_r4 == 1, A_7_1_r4 + A_8_2_r4 == 1), (d_8_1_1_r4 == 1), (d_8_1_1_r4 == 0)))
s.add(If(And(A_7_1_r4 == 1, A_7_2_r4 + A_8_1_r4 == 1), (d_7_1_1_r4 == 1), (d_7_1_1_r4 == 0)))
s.add(If(And(A_7_2_r5 == 1, A_8_2_r5 + A_7_1_r5 == 1), (d_7_2_1_r5 == 1), (d_7_2_1_r5 == 0)))
s.add(If(And(A_8_2_r5 == 1, A_7_2_r5 + A_8_1_r5 == 1), (d_8_2_1_r5 == 1), (d_8_2_1_r5 == 0)))
s.add(If(And(A_8_1_r5 == 1, A_7_1_r5 + A_8_2_r5 == 1), (d_8_1_1_r5 == 1), (d_8_1_1_r5 == 0)))
s.add(If(And(A_7_1_r5 == 1, A_7_2_r5 + A_8_1_r5 == 1), (d_7_1_1_r5 == 1), (d_7_1_1_r5 == 0)))
s.add(If(And(A_7_2_r2 == 1, A_8_2_r2 + A_7_1_r2 == 2), (d_7_2_2_r2 == 1), (d_7_2_2_r2 == 0)))
s.add(If(And(A_8_2_r2 == 1, A_7_2_r2 + A_8_1_r2 == 2), (d_8_2_2_r2 == 1), (d_8_2_2_r2 == 0)))
s.add(If(And(A_8_1_r2 == 1, A_7_1_r2 + A_8_2_r2 == 2), (d_8_1_2_r2 == 1), (d_8_1_2_r2 == 0)))
s.add(If(And(A_7_1_r2 == 1, A_7_2_r2 + A_8_1_r2 == 2), (d_7_1_2_r2 == 1), (d_7_1_2_r2 == 0)))
s.add(If(And(A_7_2_r4 == 1, A_8_2_r4 + A_7_1_r4 == 2), (d_7_2_2_r4 == 1), (d_7_2_2_r4 == 0)))
s.add(If(And(A_8_2_r4 == 1, A_7_2_r4 + A_8_1_r4 == 2), (d_8_2_2_r4 == 1), (d_8_2_2_r4 == 0)))
s.add(If(And(A_8_1_r4 == 1, A_7_1_r4 + A_8_2_r4 == 2), (d_8_1_2_r4 == 1), (d_8_1_2_r4 == 0)))
s.add(If(And(A_7_1_r4 == 1, A_7_2_r4 + A_8_1_r4 == 2), (d_7_1_2_r4 == 1), (d_7_1_2_r4 == 0)))
s.add(If(And(A_7_2_r5 == 1, A_8_2_r5 + A_7_1_r5 == 2), (d_7_2_2_r5 == 1), (d_7_2_2_r5 == 0)))
s.add(If(And(A_8_2_r5 == 1, A_7_2_r5 + A_8_1_r5 == 2), (d_8_2_2_r5 == 1), (d_8_2_2_r5 == 0)))
s.add(If(And(A_8_1_r5 == 1, A_7_1_r5 + A_8_2_r5 == 2), (d_8_1_2_r5 == 1), (d_8_1_2_r5 == 0)))
s.add(If(And(A_7_1_r5 == 1, A_7_2_r5 + A_8_1_r5 == 2), (d_7_1_2_r5 == 1), (d_7_1_2_r5 == 0)))

s.add(d_7_2_0_r2 + d_8_2_0_r2 + d_8_1_0_r2 + d_7_1_0_r2 == d_0_r2)
s.add(d_7_2_1_r2 + d_8_2_1_r2 + d_8_1_1_r2 + d_7_1_1_r2 == d_1_r2)
s.add(d_7_2_2_r2 + d_8_2_2_r2 + d_8_1_2_r2 + d_7_1_2_r2 == d_2_r2)
s.add(d_7_2_0_r4 + d_8_2_0_r4 + d_8_1_0_r4 + d_7_1_0_r4 == d_0_r4)
s.add(d_7_2_1_r4 + d_8_2_1_r4 + d_8_1_1_r4 + d_7_1_1_r4 == d_1_r4)
s.add(d_7_2_2_r4 + d_8_2_2_r4 + d_8_1_2_r4 + d_7_1_2_r4 == d_2_r4)
s.add(d_7_2_0_r5 + d_8_2_0_r5 + d_8_1_0_r5 + d_7_1_0_r5 == d_0_r5)
s.add(d_7_2_1_r5 + d_8_2_1_r5 + d_8_1_1_r5 + d_7_1_1_r5 == d_1_r5)
s.add(d_7_2_2_r5 + d_8_2_2_r5 + d_8_1_2_r5 + d_7_1_2_r5 == d_2_r5)

s.add(Implies(V_r2 == 1, And(d_0_r2 == 1, d_1_r2 == 0, d_2_r2 == 0)))
s.add(Implies(V_r2 == 2, And(d_0_r2 == 0, d_1_r2 == 2, d_2_r2 == 0)))
s.add(Implies(V_r2 == 3, And(d_0_r2 == 0, d_1_r2 == 2, d_2_r2 == 1)))
s.add(Implies(V_r2 == 4, And(d_0_r2 == 0, d_1_r2 == 0, d_2_r2 == 4)))
s.add(Implies(V_r4 == 1, And(d_0_r4 == 1, d_1_r4 == 0, d_2_r4 == 0)))
s.add(Implies(V_r4 == 2, And(d_0_r4 == 0, d_1_r4 == 2, d_2_r4 == 0)))
s.add(Implies(V_r4 == 3, And(d_0_r4 == 0, d_1_r4 == 2, d_2_r4 == 1)))
s.add(Implies(V_r4 == 4, And(d_0_r4 == 0, d_1_r4 == 0, d_2_r4 == 4)))
s.add(Implies(V_r5 == 1, And(d_0_r5 == 1, d_1_r5 == 0, d_2_r5 == 0)))
s.add(Implies(V_r5 == 2, And(d_0_r5 == 0, d_1_r5 == 2, d_2_r5 == 0)))
s.add(Implies(V_r5 == 3, And(d_0_r5 == 0, d_1_r5 == 2, d_2_r5 == 1)))
s.add(Implies(V_r5 == 4, And(d_0_r5 == 0, d_1_r5 == 0, d_2_r5 == 4)))

s.add(And(V_r2 == 1, V_r4 == 1, V_r5 == 2))

if s.check() == unsat:
	print("Not possible to create traceable graph for all reagents")
else:
	fp = open('output0.txt','w')
	values = s.model()
	if values[A_7_2_r2] == 1:
		fp.write("7,2,r2\n")
	if values[A_7_2_r4] == 1:
		fp.write("7,2,r4\n")
	if values[A_7_2_r5] == 1:
		fp.write("7,2,r5\n")
	if values[A_8_2_r2] == 1:
		fp.write("8,2,r2\n")
	if values[A_8_2_r4] == 1:
		fp.write("8,2,r4\n")
	if values[A_8_2_r5] == 1:
		fp.write("8,2,r5\n")
	if values[A_8_1_r2] == 1:
		fp.write("8,1,r2\n")
	if values[A_8_1_r4] == 1:
		fp.write("8,1,r4\n")
	if values[A_8_1_r5] == 1:
		fp.write("8,1,r5\n")
	if values[A_7_1_r2] == 1:
		fp.write("7,1,r2\n")
	if values[A_7_1_r4] == 1:
		fp.write("7,1,r4\n")
	if values[A_7_1_r5] == 1:
		fp.write("7,1,r5\n")
