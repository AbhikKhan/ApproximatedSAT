import sys
import time
sys.path.append("/home/sukanta/App/z3-master/build")
from z3 import *

s = Optimize()
R_1_1_1, R_1_1_2, R_1_1_3, R_1_1_4, R_1_1_5  = Ints('R_1_1_1 R_1_1_2 R_1_1_3 R_1_1_4 R_1_1_5')
r_1_1_1, r_1_1_2, r_1_1_3, r_1_1_4, r_1_1_5, s_1_1  = Ints('r_1_1_1 r_1_1_2 r_1_1_3 r_1_1_4 r_1_1_5 s_1_1')# Added reagent variables
R_2_1_1, R_2_1_2, R_2_1_3, R_2_1_4, R_2_1_5  = Ints('R_2_1_1 R_2_1_2 R_2_1_3 R_2_1_4 R_2_1_5')
r_2_1_1, r_2_1_2, r_2_1_3, r_2_1_4, r_2_1_5, s_2_1  = Ints('r_2_1_1 r_2_1_2 r_2_1_3 r_2_1_4 r_2_1_5 s_2_1')# Added reagent variables
R_2_2_1, R_2_2_2, R_2_2_3, R_2_2_4, R_2_2_5  = Ints('R_2_2_1 R_2_2_2 R_2_2_3 R_2_2_4 R_2_2_5')
r_2_2_1, r_2_2_2, r_2_2_3, r_2_2_4, r_2_2_5, s_2_2  = Ints('r_2_2_1 r_2_2_2 r_2_2_3 r_2_2_4 r_2_2_5 s_2_2')# Added reagent variables
R_2_3_1, R_2_3_2, R_2_3_3, R_2_3_4, R_2_3_5  = Ints('R_2_3_1 R_2_3_2 R_2_3_3 R_2_3_4 R_2_3_5')
r_2_3_1, r_2_3_2, r_2_3_3, r_2_3_4, r_2_3_5, s_2_3  = Ints('r_2_3_1 r_2_3_2 r_2_3_3 r_2_3_4 r_2_3_5 s_2_3')# Added reagent variables
R_3_1_1, R_3_1_2, R_3_1_3, R_3_1_4, R_3_1_5  = Ints('R_3_1_1 R_3_1_2 R_3_1_3 R_3_1_4 R_3_1_5')
r_3_1_1, r_3_1_2, r_3_1_3, r_3_1_4, r_3_1_5, s_3_1  = Ints('r_3_1_1 r_3_1_2 r_3_1_3 r_3_1_4 r_3_1_5 s_3_1')# Added reagent variables
R_3_2_1, R_3_2_2, R_3_2_3, R_3_2_4, R_3_2_5  = Ints('R_3_2_1 R_3_2_2 R_3_2_3 R_3_2_4 R_3_2_5')
r_3_2_1, r_3_2_2, r_3_2_3, r_3_2_4, r_3_2_5, s_3_2  = Ints('r_3_2_1 r_3_2_2 r_3_2_3 r_3_2_4 r_3_2_5 s_3_2')# Added reagent variables
R_3_3_1, R_3_3_2, R_3_3_3, R_3_3_4, R_3_3_5  = Ints('R_3_3_1 R_3_3_2 R_3_3_3 R_3_3_4 R_3_3_5')
r_3_3_1, r_3_3_2, r_3_3_3, r_3_3_4, r_3_3_5, s_3_3  = Ints('r_3_3_1 r_3_3_2 r_3_3_3 r_3_3_4 r_3_3_5 s_3_3')# Added reagent variables
R_3_4_1, R_3_4_2, R_3_4_3, R_3_4_4, R_3_4_5  = Ints('R_3_4_1 R_3_4_2 R_3_4_3 R_3_4_4 R_3_4_5')
r_3_4_1, r_3_4_2, r_3_4_3, r_3_4_4, r_3_4_5, s_3_4  = Ints('r_3_4_1 r_3_4_2 r_3_4_3 r_3_4_4 r_3_4_5 s_3_4')# Added reagent variables
R_4_1_1, R_4_1_2, R_4_1_3, R_4_1_4, R_4_1_5  = Ints('R_4_1_1 R_4_1_2 R_4_1_3 R_4_1_4 R_4_1_5')
r_4_1_1, r_4_1_2, r_4_1_3, r_4_1_4, r_4_1_5, s_4_1  = Ints('r_4_1_1 r_4_1_2 r_4_1_3 r_4_1_4 r_4_1_5 s_4_1')# Added reagent variables
R_4_2_1, R_4_2_2, R_4_2_3, R_4_2_4, R_4_2_5  = Ints('R_4_2_1 R_4_2_2 R_4_2_3 R_4_2_4 R_4_2_5')
r_4_2_1, r_4_2_2, r_4_2_3, r_4_2_4, r_4_2_5, s_4_2  = Ints('r_4_2_1 r_4_2_2 r_4_2_3 r_4_2_4 r_4_2_5 s_4_2')# Added reagent variables
R_4_3_1, R_4_3_2, R_4_3_3, R_4_3_4, R_4_3_5  = Ints('R_4_3_1 R_4_3_2 R_4_3_3 R_4_3_4 R_4_3_5')
r_4_3_1, r_4_3_2, r_4_3_3, r_4_3_4, r_4_3_5, s_4_3  = Ints('r_4_3_1 r_4_3_2 r_4_3_3 r_4_3_4 r_4_3_5 s_4_3')# Added reagent variables
w_2_1_1_1, w_2_2_1_1, w_2_3_1_1, w_3_1_2_3, w_3_2_2_3, w_3_3_2_3, w_3_4_2_3, w_4_1_3_4, w_4_2_3_4, w_4_3_3_4  = Ints('w_2_1_1_1 w_2_2_1_1 w_2_3_1_1 w_3_1_2_3 w_3_2_2_3 w_3_3_2_3 w_3_4_2_3 w_4_1_3_4 w_4_2_3_4 w_4_3_3_4')# Added edgeVariables

t93946 = Int('t93946')
t93947 = Int('t93947')
t93948 = Int('t93948')
t93949 = Int('t93949')
t93950 = Int('t93950')
t93951 = Int('t93951')
t93952 = Int('t93952')
t93953 = Int('t93953')
t93954 = Int('t93954')
t93955 = Int('t93955')
t93956 = Int('t93956')
t93957 = Int('t93957')
t93958 = Int('t93958')
t93959 = Int('t93959')
t93960 = Int('t93960')
s.add(64*r_1_1_1 + 16*t93946 + 16*t93947 + 1*t93948  == R_1_1_1)
s.add(64*r_1_1_2 + 16*t93949 + 16*t93950 + 1*t93951  == R_1_1_2)
s.add(64*r_1_1_3 + 16*t93952 + 16*t93953 + 1*t93954  == R_1_1_3)
s.add(64*r_1_1_4 + 16*t93955 + 16*t93956 + 1*t93957  == R_1_1_4)
s.add(64*r_1_1_5 + 16*t93958 + 16*t93959 + 1*t93960  == R_1_1_5)

s.add(Implies((w_2_1_1_1 == 0), (t93946 == 0)))
s.add(Implies((w_2_1_1_1 == 1), (t93946 == 1*R_2_1_1)))
s.add(Implies((w_2_1_1_1 == 2), (t93946 == 2*R_2_1_1)))
s.add(Implies((w_2_1_1_1 == 3), (t93946 == 3*R_2_1_1)))

s.add(Implies((w_2_2_1_1 == 0), (t93947 == 0)))
s.add(Implies((w_2_2_1_1 == 1), (t93947 == 1*R_2_2_1)))
s.add(Implies((w_2_2_1_1 == 2), (t93947 == 2*R_2_2_1)))
s.add(Implies((w_2_2_1_1 == 3), (t93947 == 3*R_2_2_1)))

s.add(Implies((w_2_3_1_1 == 0), (t93948 == 0)))
s.add(Implies((w_2_3_1_1 == 1), (t93948 == 1*R_2_3_1)))
s.add(Implies((w_2_3_1_1 == 2), (t93948 == 2*R_2_3_1)))
s.add(Implies((w_2_3_1_1 == 3), (t93948 == 3*R_2_3_1)))

s.add(Implies((w_2_1_1_1 == 0), (t93949 == 0)))
s.add(Implies((w_2_1_1_1 == 1), (t93949 == 1*R_2_1_2)))
s.add(Implies((w_2_1_1_1 == 2), (t93949 == 2*R_2_1_2)))
s.add(Implies((w_2_1_1_1 == 3), (t93949 == 3*R_2_1_2)))

s.add(Implies((w_2_2_1_1 == 0), (t93950 == 0)))
s.add(Implies((w_2_2_1_1 == 1), (t93950 == 1*R_2_2_2)))
s.add(Implies((w_2_2_1_1 == 2), (t93950 == 2*R_2_2_2)))
s.add(Implies((w_2_2_1_1 == 3), (t93950 == 3*R_2_2_2)))

s.add(Implies((w_2_3_1_1 == 0), (t93951 == 0)))
s.add(Implies((w_2_3_1_1 == 1), (t93951 == 1*R_2_3_2)))
s.add(Implies((w_2_3_1_1 == 2), (t93951 == 2*R_2_3_2)))
s.add(Implies((w_2_3_1_1 == 3), (t93951 == 3*R_2_3_2)))

s.add(Implies((w_2_1_1_1 == 0), (t93952 == 0)))
s.add(Implies((w_2_1_1_1 == 1), (t93952 == 1*R_2_1_3)))
s.add(Implies((w_2_1_1_1 == 2), (t93952 == 2*R_2_1_3)))
s.add(Implies((w_2_1_1_1 == 3), (t93952 == 3*R_2_1_3)))

s.add(Implies((w_2_2_1_1 == 0), (t93953 == 0)))
s.add(Implies((w_2_2_1_1 == 1), (t93953 == 1*R_2_2_3)))
s.add(Implies((w_2_2_1_1 == 2), (t93953 == 2*R_2_2_3)))
s.add(Implies((w_2_2_1_1 == 3), (t93953 == 3*R_2_2_3)))

s.add(Implies((w_2_3_1_1 == 0), (t93954 == 0)))
s.add(Implies((w_2_3_1_1 == 1), (t93954 == 1*R_2_3_3)))
s.add(Implies((w_2_3_1_1 == 2), (t93954 == 2*R_2_3_3)))
s.add(Implies((w_2_3_1_1 == 3), (t93954 == 3*R_2_3_3)))

s.add(Implies((w_2_1_1_1 == 0), (t93955 == 0)))
s.add(Implies((w_2_1_1_1 == 1), (t93955 == 1*R_2_1_4)))
s.add(Implies((w_2_1_1_1 == 2), (t93955 == 2*R_2_1_4)))
s.add(Implies((w_2_1_1_1 == 3), (t93955 == 3*R_2_1_4)))

s.add(Implies((w_2_2_1_1 == 0), (t93956 == 0)))
s.add(Implies((w_2_2_1_1 == 1), (t93956 == 1*R_2_2_4)))
s.add(Implies((w_2_2_1_1 == 2), (t93956 == 2*R_2_2_4)))
s.add(Implies((w_2_2_1_1 == 3), (t93956 == 3*R_2_2_4)))

s.add(Implies((w_2_3_1_1 == 0), (t93957 == 0)))
s.add(Implies((w_2_3_1_1 == 1), (t93957 == 1*R_2_3_4)))
s.add(Implies((w_2_3_1_1 == 2), (t93957 == 2*R_2_3_4)))
s.add(Implies((w_2_3_1_1 == 3), (t93957 == 3*R_2_3_4)))

s.add(Implies((w_2_1_1_1 == 0), (t93958 == 0)))
s.add(Implies((w_2_1_1_1 == 1), (t93958 == 1*R_2_1_5)))
s.add(Implies((w_2_1_1_1 == 2), (t93958 == 2*R_2_1_5)))
s.add(Implies((w_2_1_1_1 == 3), (t93958 == 3*R_2_1_5)))

s.add(Implies((w_2_2_1_1 == 0), (t93959 == 0)))
s.add(Implies((w_2_2_1_1 == 1), (t93959 == 1*R_2_2_5)))
s.add(Implies((w_2_2_1_1 == 2), (t93959 == 2*R_2_2_5)))
s.add(Implies((w_2_2_1_1 == 3), (t93959 == 3*R_2_2_5)))

s.add(Implies((w_2_3_1_1 == 0), (t93960 == 0)))
s.add(Implies((w_2_3_1_1 == 1), (t93960 == 1*R_2_3_5)))
s.add(Implies((w_2_3_1_1 == 2), (t93960 == 2*R_2_3_5)))
s.add(Implies((w_2_3_1_1 == 3), (t93960 == 3*R_2_3_5)))

s.add(1*r_2_1_1  == R_2_1_1)
s.add(1*r_2_1_2  == R_2_1_2)
s.add(1*r_2_1_3  == R_2_1_3)
s.add(1*r_2_1_4  == R_2_1_4)
s.add(1*r_2_1_5  == R_2_1_5)

s.add(1*r_2_2_1  == R_2_2_1)
s.add(1*r_2_2_2  == R_2_2_2)
s.add(1*r_2_2_3  == R_2_2_3)
s.add(1*r_2_2_4  == R_2_2_4)
s.add(1*r_2_2_5  == R_2_2_5)

t93961 = Int('t93961')
t93962 = Int('t93962')
t93963 = Int('t93963')
t93964 = Int('t93964')
t93965 = Int('t93965')
t93966 = Int('t93966')
t93967 = Int('t93967')
t93968 = Int('t93968')
t93969 = Int('t93969')
t93970 = Int('t93970')
t93971 = Int('t93971')
t93972 = Int('t93972')
t93973 = Int('t93973')
t93974 = Int('t93974')
t93975 = Int('t93975')
t93976 = Int('t93976')
t93977 = Int('t93977')
t93978 = Int('t93978')
t93979 = Int('t93979')
t93980 = Int('t93980')
s.add(16*r_2_3_1 + 4*t93961 + 4*t93962 + 4*t93963 + 1*t93964  == R_2_3_1)
s.add(16*r_2_3_2 + 4*t93965 + 4*t93966 + 4*t93967 + 1*t93968  == R_2_3_2)
s.add(16*r_2_3_3 + 4*t93969 + 4*t93970 + 4*t93971 + 1*t93972  == R_2_3_3)
s.add(16*r_2_3_4 + 4*t93973 + 4*t93974 + 4*t93975 + 1*t93976  == R_2_3_4)
s.add(16*r_2_3_5 + 4*t93977 + 4*t93978 + 4*t93979 + 1*t93980  == R_2_3_5)

s.add(Implies((w_3_1_2_3 == 0), (t93961 == 0)))
s.add(Implies((w_3_1_2_3 == 1), (t93961 == 1*R_3_1_1)))
s.add(Implies((w_3_1_2_3 == 2), (t93961 == 2*R_3_1_1)))
s.add(Implies((w_3_1_2_3 == 3), (t93961 == 3*R_3_1_1)))

s.add(Implies((w_3_2_2_3 == 0), (t93962 == 0)))
s.add(Implies((w_3_2_2_3 == 1), (t93962 == 1*R_3_2_1)))
s.add(Implies((w_3_2_2_3 == 2), (t93962 == 2*R_3_2_1)))
s.add(Implies((w_3_2_2_3 == 3), (t93962 == 3*R_3_2_1)))

s.add(Implies((w_3_3_2_3 == 0), (t93963 == 0)))
s.add(Implies((w_3_3_2_3 == 1), (t93963 == 1*R_3_3_1)))
s.add(Implies((w_3_3_2_3 == 2), (t93963 == 2*R_3_3_1)))
s.add(Implies((w_3_3_2_3 == 3), (t93963 == 3*R_3_3_1)))

s.add(Implies((w_3_4_2_3 == 0), (t93964 == 0)))
s.add(Implies((w_3_4_2_3 == 1), (t93964 == 1*R_3_4_1)))
s.add(Implies((w_3_4_2_3 == 2), (t93964 == 2*R_3_4_1)))
s.add(Implies((w_3_4_2_3 == 3), (t93964 == 3*R_3_4_1)))

s.add(Implies((w_3_1_2_3 == 0), (t93965 == 0)))
s.add(Implies((w_3_1_2_3 == 1), (t93965 == 1*R_3_1_2)))
s.add(Implies((w_3_1_2_3 == 2), (t93965 == 2*R_3_1_2)))
s.add(Implies((w_3_1_2_3 == 3), (t93965 == 3*R_3_1_2)))

s.add(Implies((w_3_2_2_3 == 0), (t93966 == 0)))
s.add(Implies((w_3_2_2_3 == 1), (t93966 == 1*R_3_2_2)))
s.add(Implies((w_3_2_2_3 == 2), (t93966 == 2*R_3_2_2)))
s.add(Implies((w_3_2_2_3 == 3), (t93966 == 3*R_3_2_2)))

s.add(Implies((w_3_3_2_3 == 0), (t93967 == 0)))
s.add(Implies((w_3_3_2_3 == 1), (t93967 == 1*R_3_3_2)))
s.add(Implies((w_3_3_2_3 == 2), (t93967 == 2*R_3_3_2)))
s.add(Implies((w_3_3_2_3 == 3), (t93967 == 3*R_3_3_2)))

s.add(Implies((w_3_4_2_3 == 0), (t93968 == 0)))
s.add(Implies((w_3_4_2_3 == 1), (t93968 == 1*R_3_4_2)))
s.add(Implies((w_3_4_2_3 == 2), (t93968 == 2*R_3_4_2)))
s.add(Implies((w_3_4_2_3 == 3), (t93968 == 3*R_3_4_2)))

s.add(Implies((w_3_1_2_3 == 0), (t93969 == 0)))
s.add(Implies((w_3_1_2_3 == 1), (t93969 == 1*R_3_1_3)))
s.add(Implies((w_3_1_2_3 == 2), (t93969 == 2*R_3_1_3)))
s.add(Implies((w_3_1_2_3 == 3), (t93969 == 3*R_3_1_3)))

s.add(Implies((w_3_2_2_3 == 0), (t93970 == 0)))
s.add(Implies((w_3_2_2_3 == 1), (t93970 == 1*R_3_2_3)))
s.add(Implies((w_3_2_2_3 == 2), (t93970 == 2*R_3_2_3)))
s.add(Implies((w_3_2_2_3 == 3), (t93970 == 3*R_3_2_3)))

s.add(Implies((w_3_3_2_3 == 0), (t93971 == 0)))
s.add(Implies((w_3_3_2_3 == 1), (t93971 == 1*R_3_3_3)))
s.add(Implies((w_3_3_2_3 == 2), (t93971 == 2*R_3_3_3)))
s.add(Implies((w_3_3_2_3 == 3), (t93971 == 3*R_3_3_3)))

s.add(Implies((w_3_4_2_3 == 0), (t93972 == 0)))
s.add(Implies((w_3_4_2_3 == 1), (t93972 == 1*R_3_4_3)))
s.add(Implies((w_3_4_2_3 == 2), (t93972 == 2*R_3_4_3)))
s.add(Implies((w_3_4_2_3 == 3), (t93972 == 3*R_3_4_3)))

s.add(Implies((w_3_1_2_3 == 0), (t93973 == 0)))
s.add(Implies((w_3_1_2_3 == 1), (t93973 == 1*R_3_1_4)))
s.add(Implies((w_3_1_2_3 == 2), (t93973 == 2*R_3_1_4)))
s.add(Implies((w_3_1_2_3 == 3), (t93973 == 3*R_3_1_4)))

s.add(Implies((w_3_2_2_3 == 0), (t93974 == 0)))
s.add(Implies((w_3_2_2_3 == 1), (t93974 == 1*R_3_2_4)))
s.add(Implies((w_3_2_2_3 == 2), (t93974 == 2*R_3_2_4)))
s.add(Implies((w_3_2_2_3 == 3), (t93974 == 3*R_3_2_4)))

s.add(Implies((w_3_3_2_3 == 0), (t93975 == 0)))
s.add(Implies((w_3_3_2_3 == 1), (t93975 == 1*R_3_3_4)))
s.add(Implies((w_3_3_2_3 == 2), (t93975 == 2*R_3_3_4)))
s.add(Implies((w_3_3_2_3 == 3), (t93975 == 3*R_3_3_4)))

s.add(Implies((w_3_4_2_3 == 0), (t93976 == 0)))
s.add(Implies((w_3_4_2_3 == 1), (t93976 == 1*R_3_4_4)))
s.add(Implies((w_3_4_2_3 == 2), (t93976 == 2*R_3_4_4)))
s.add(Implies((w_3_4_2_3 == 3), (t93976 == 3*R_3_4_4)))

s.add(Implies((w_3_1_2_3 == 0), (t93977 == 0)))
s.add(Implies((w_3_1_2_3 == 1), (t93977 == 1*R_3_1_5)))
s.add(Implies((w_3_1_2_3 == 2), (t93977 == 2*R_3_1_5)))
s.add(Implies((w_3_1_2_3 == 3), (t93977 == 3*R_3_1_5)))

s.add(Implies((w_3_2_2_3 == 0), (t93978 == 0)))
s.add(Implies((w_3_2_2_3 == 1), (t93978 == 1*R_3_2_5)))
s.add(Implies((w_3_2_2_3 == 2), (t93978 == 2*R_3_2_5)))
s.add(Implies((w_3_2_2_3 == 3), (t93978 == 3*R_3_2_5)))

s.add(Implies((w_3_3_2_3 == 0), (t93979 == 0)))
s.add(Implies((w_3_3_2_3 == 1), (t93979 == 1*R_3_3_5)))
s.add(Implies((w_3_3_2_3 == 2), (t93979 == 2*R_3_3_5)))
s.add(Implies((w_3_3_2_3 == 3), (t93979 == 3*R_3_3_5)))

s.add(Implies((w_3_4_2_3 == 0), (t93980 == 0)))
s.add(Implies((w_3_4_2_3 == 1), (t93980 == 1*R_3_4_5)))
s.add(Implies((w_3_4_2_3 == 2), (t93980 == 2*R_3_4_5)))
s.add(Implies((w_3_4_2_3 == 3), (t93980 == 3*R_3_4_5)))

s.add(1*r_3_1_1  == R_3_1_1)
s.add(1*r_3_1_2  == R_3_1_2)
s.add(1*r_3_1_3  == R_3_1_3)
s.add(1*r_3_1_4  == R_3_1_4)
s.add(1*r_3_1_5  == R_3_1_5)

s.add(1*r_3_2_1  == R_3_2_1)
s.add(1*r_3_2_2  == R_3_2_2)
s.add(1*r_3_2_3  == R_3_2_3)
s.add(1*r_3_2_4  == R_3_2_4)
s.add(1*r_3_2_5  == R_3_2_5)

s.add(1*r_3_3_1  == R_3_3_1)
s.add(1*r_3_3_2  == R_3_3_2)
s.add(1*r_3_3_3  == R_3_3_3)
s.add(1*r_3_3_4  == R_3_3_4)
s.add(1*r_3_3_5  == R_3_3_5)

t93981 = Int('t93981')
t93982 = Int('t93982')
t93983 = Int('t93983')
t93984 = Int('t93984')
t93985 = Int('t93985')
t93986 = Int('t93986')
t93987 = Int('t93987')
t93988 = Int('t93988')
t93989 = Int('t93989')
t93990 = Int('t93990')
t93991 = Int('t93991')
t93992 = Int('t93992')
t93993 = Int('t93993')
t93994 = Int('t93994')
t93995 = Int('t93995')
s.add(4*r_3_4_1 + 1*t93981 + 1*t93982 + 1*t93983  == R_3_4_1)
s.add(4*r_3_4_2 + 1*t93984 + 1*t93985 + 1*t93986  == R_3_4_2)
s.add(4*r_3_4_3 + 1*t93987 + 1*t93988 + 1*t93989  == R_3_4_3)
s.add(4*r_3_4_4 + 1*t93990 + 1*t93991 + 1*t93992  == R_3_4_4)
s.add(4*r_3_4_5 + 1*t93993 + 1*t93994 + 1*t93995  == R_3_4_5)

s.add(Implies((w_4_1_3_4 == 0), (t93981 == 0)))
s.add(Implies((w_4_1_3_4 == 1), (t93981 == 1*R_4_1_1)))
s.add(Implies((w_4_1_3_4 == 2), (t93981 == 2*R_4_1_1)))
s.add(Implies((w_4_1_3_4 == 3), (t93981 == 3*R_4_1_1)))

s.add(Implies((w_4_2_3_4 == 0), (t93982 == 0)))
s.add(Implies((w_4_2_3_4 == 1), (t93982 == 1*R_4_2_1)))
s.add(Implies((w_4_2_3_4 == 2), (t93982 == 2*R_4_2_1)))
s.add(Implies((w_4_2_3_4 == 3), (t93982 == 3*R_4_2_1)))

s.add(Implies((w_4_3_3_4 == 0), (t93983 == 0)))
s.add(Implies((w_4_3_3_4 == 1), (t93983 == 1*R_4_3_1)))
s.add(Implies((w_4_3_3_4 == 2), (t93983 == 2*R_4_3_1)))
s.add(Implies((w_4_3_3_4 == 3), (t93983 == 3*R_4_3_1)))

s.add(Implies((w_4_1_3_4 == 0), (t93984 == 0)))
s.add(Implies((w_4_1_3_4 == 1), (t93984 == 1*R_4_1_2)))
s.add(Implies((w_4_1_3_4 == 2), (t93984 == 2*R_4_1_2)))
s.add(Implies((w_4_1_3_4 == 3), (t93984 == 3*R_4_1_2)))

s.add(Implies((w_4_2_3_4 == 0), (t93985 == 0)))
s.add(Implies((w_4_2_3_4 == 1), (t93985 == 1*R_4_2_2)))
s.add(Implies((w_4_2_3_4 == 2), (t93985 == 2*R_4_2_2)))
s.add(Implies((w_4_2_3_4 == 3), (t93985 == 3*R_4_2_2)))

s.add(Implies((w_4_3_3_4 == 0), (t93986 == 0)))
s.add(Implies((w_4_3_3_4 == 1), (t93986 == 1*R_4_3_2)))
s.add(Implies((w_4_3_3_4 == 2), (t93986 == 2*R_4_3_2)))
s.add(Implies((w_4_3_3_4 == 3), (t93986 == 3*R_4_3_2)))

s.add(Implies((w_4_1_3_4 == 0), (t93987 == 0)))
s.add(Implies((w_4_1_3_4 == 1), (t93987 == 1*R_4_1_3)))
s.add(Implies((w_4_1_3_4 == 2), (t93987 == 2*R_4_1_3)))
s.add(Implies((w_4_1_3_4 == 3), (t93987 == 3*R_4_1_3)))

s.add(Implies((w_4_2_3_4 == 0), (t93988 == 0)))
s.add(Implies((w_4_2_3_4 == 1), (t93988 == 1*R_4_2_3)))
s.add(Implies((w_4_2_3_4 == 2), (t93988 == 2*R_4_2_3)))
s.add(Implies((w_4_2_3_4 == 3), (t93988 == 3*R_4_2_3)))

s.add(Implies((w_4_3_3_4 == 0), (t93989 == 0)))
s.add(Implies((w_4_3_3_4 == 1), (t93989 == 1*R_4_3_3)))
s.add(Implies((w_4_3_3_4 == 2), (t93989 == 2*R_4_3_3)))
s.add(Implies((w_4_3_3_4 == 3), (t93989 == 3*R_4_3_3)))

s.add(Implies((w_4_1_3_4 == 0), (t93990 == 0)))
s.add(Implies((w_4_1_3_4 == 1), (t93990 == 1*R_4_1_4)))
s.add(Implies((w_4_1_3_4 == 2), (t93990 == 2*R_4_1_4)))
s.add(Implies((w_4_1_3_4 == 3), (t93990 == 3*R_4_1_4)))

s.add(Implies((w_4_2_3_4 == 0), (t93991 == 0)))
s.add(Implies((w_4_2_3_4 == 1), (t93991 == 1*R_4_2_4)))
s.add(Implies((w_4_2_3_4 == 2), (t93991 == 2*R_4_2_4)))
s.add(Implies((w_4_2_3_4 == 3), (t93991 == 3*R_4_2_4)))

s.add(Implies((w_4_3_3_4 == 0), (t93992 == 0)))
s.add(Implies((w_4_3_3_4 == 1), (t93992 == 1*R_4_3_4)))
s.add(Implies((w_4_3_3_4 == 2), (t93992 == 2*R_4_3_4)))
s.add(Implies((w_4_3_3_4 == 3), (t93992 == 3*R_4_3_4)))

s.add(Implies((w_4_1_3_4 == 0), (t93993 == 0)))
s.add(Implies((w_4_1_3_4 == 1), (t93993 == 1*R_4_1_5)))
s.add(Implies((w_4_1_3_4 == 2), (t93993 == 2*R_4_1_5)))
s.add(Implies((w_4_1_3_4 == 3), (t93993 == 3*R_4_1_5)))

s.add(Implies((w_4_2_3_4 == 0), (t93994 == 0)))
s.add(Implies((w_4_2_3_4 == 1), (t93994 == 1*R_4_2_5)))
s.add(Implies((w_4_2_3_4 == 2), (t93994 == 2*R_4_2_5)))
s.add(Implies((w_4_2_3_4 == 3), (t93994 == 3*R_4_2_5)))

s.add(Implies((w_4_3_3_4 == 0), (t93995 == 0)))
s.add(Implies((w_4_3_3_4 == 1), (t93995 == 1*R_4_3_5)))
s.add(Implies((w_4_3_3_4 == 2), (t93995 == 2*R_4_3_5)))
s.add(Implies((w_4_3_3_4 == 3), (t93995 == 3*R_4_3_5)))

s.add(1*r_4_1_1  == R_4_1_1)
s.add(1*r_4_1_2  == R_4_1_2)
s.add(1*r_4_1_3  == R_4_1_3)
s.add(1*r_4_1_4  == R_4_1_4)
s.add(1*r_4_1_5  == R_4_1_5)

s.add(1*r_4_2_1  == R_4_2_1)
s.add(1*r_4_2_2  == R_4_2_2)
s.add(1*r_4_2_3  == R_4_2_3)
s.add(1*r_4_2_4  == R_4_2_4)
s.add(1*r_4_2_5  == R_4_2_5)

s.add(1*r_4_3_1  == R_4_3_1)
s.add(1*r_4_3_2  == R_4_3_2)
s.add(1*r_4_3_3  == R_4_3_3)
s.add(1*r_4_3_4  == R_4_3_4)
s.add(1*r_4_3_5  == R_4_3_5)

s.add(Or(r_1_1_1 + r_1_1_2 + r_1_1_3 + r_1_1_4 + r_1_1_5 + w_2_1_1_1 + w_2_2_1_1 + w_2_3_1_1  == 4, r_1_1_1 + r_1_1_2 + r_1_1_3 + r_1_1_4 + r_1_1_5 + w_2_1_1_1 + w_2_2_1_1 + w_2_3_1_1  == 0))
s.add(Or(r_2_1_1 + r_2_1_2 + r_2_1_3 + r_2_1_4 + r_2_1_5  == 4, r_2_1_1 + r_2_1_2 + r_2_1_3 + r_2_1_4 + r_2_1_5  == 0))
s.add(w_2_1_1_1  <= 4)
s.add(Or(r_2_2_1 + r_2_2_2 + r_2_2_3 + r_2_2_4 + r_2_2_5  == 4, r_2_2_1 + r_2_2_2 + r_2_2_3 + r_2_2_4 + r_2_2_5  == 0))
s.add(w_2_2_1_1  <= 4)
s.add(Or(r_2_3_1 + r_2_3_2 + r_2_3_3 + r_2_3_4 + r_2_3_5 + w_3_1_2_3 + w_3_2_2_3 + w_3_3_2_3 + w_3_4_2_3  == 4, r_2_3_1 + r_2_3_2 + r_2_3_3 + r_2_3_4 + r_2_3_5 + w_3_1_2_3 + w_3_2_2_3 + w_3_3_2_3 + w_3_4_2_3  == 0))
s.add(w_2_3_1_1  <= 4)
s.add(Or(r_3_1_1 + r_3_1_2 + r_3_1_3 + r_3_1_4 + r_3_1_5  == 4, r_3_1_1 + r_3_1_2 + r_3_1_3 + r_3_1_4 + r_3_1_5  == 0))
s.add(w_3_1_2_3  <= 4)
s.add(Or(r_3_2_1 + r_3_2_2 + r_3_2_3 + r_3_2_4 + r_3_2_5  == 4, r_3_2_1 + r_3_2_2 + r_3_2_3 + r_3_2_4 + r_3_2_5  == 0))
s.add(w_3_2_2_3  <= 4)
s.add(Or(r_3_3_1 + r_3_3_2 + r_3_3_3 + r_3_3_4 + r_3_3_5  == 4, r_3_3_1 + r_3_3_2 + r_3_3_3 + r_3_3_4 + r_3_3_5  == 0))
s.add(w_3_3_2_3  <= 4)
s.add(Or(r_3_4_1 + r_3_4_2 + r_3_4_3 + r_3_4_4 + r_3_4_5 + w_4_1_3_4 + w_4_2_3_4 + w_4_3_3_4  == 4, r_3_4_1 + r_3_4_2 + r_3_4_3 + r_3_4_4 + r_3_4_5 + w_4_1_3_4 + w_4_2_3_4 + w_4_3_3_4  == 0))
s.add(w_3_4_2_3  <= 4)
s.add(Or(r_4_1_1 + r_4_1_2 + r_4_1_3 + r_4_1_4 + r_4_1_5  == 4, r_4_1_1 + r_4_1_2 + r_4_1_3 + r_4_1_4 + r_4_1_5  == 0))
s.add(w_4_1_3_4  <= 4)
s.add(Or(r_4_2_1 + r_4_2_2 + r_4_2_3 + r_4_2_4 + r_4_2_5  == 4, r_4_2_1 + r_4_2_2 + r_4_2_3 + r_4_2_4 + r_4_2_5  == 0))
s.add(w_4_2_3_4  <= 4)
s.add(Or(r_4_3_1 + r_4_3_2 + r_4_3_3 + r_4_3_4 + r_4_3_5  == 4, r_4_3_1 + r_4_3_2 + r_4_3_3 + r_4_3_4 + r_4_3_5  == 0))
s.add(w_4_3_3_4  <= 4)
s.add(And(r_1_1_1 >= 0, r_1_1_1 <= 3, r_1_1_2 >= 0, r_1_1_2 <= 3, r_1_1_3 >= 0, r_1_1_3 <= 3, r_1_1_4 >= 0, r_1_1_4 <= 3, r_1_1_5 >= 0, r_1_1_5 <= 3))
s.add(And(r_2_1_1 >= 0, r_2_1_1 <= 3, r_2_1_2 >= 0, r_2_1_2 <= 3, r_2_1_3 >= 0, r_2_1_3 <= 3, r_2_1_4 >= 0, r_2_1_4 <= 3, r_2_1_5 >= 0, r_2_1_5 <= 3))
s.add(And(r_2_2_1 >= 0, r_2_2_1 <= 3, r_2_2_2 >= 0, r_2_2_2 <= 3, r_2_2_3 >= 0, r_2_2_3 <= 3, r_2_2_4 >= 0, r_2_2_4 <= 3, r_2_2_5 >= 0, r_2_2_5 <= 3))
s.add(And(r_2_3_1 >= 0, r_2_3_1 <= 3, r_2_3_2 >= 0, r_2_3_2 <= 3, r_2_3_3 >= 0, r_2_3_3 <= 3, r_2_3_4 >= 0, r_2_3_4 <= 3, r_2_3_5 >= 0, r_2_3_5 <= 3))
s.add(And(r_3_1_1 >= 0, r_3_1_1 <= 3, r_3_1_2 >= 0, r_3_1_2 <= 3, r_3_1_3 >= 0, r_3_1_3 <= 3, r_3_1_4 >= 0, r_3_1_4 <= 3, r_3_1_5 >= 0, r_3_1_5 <= 3))
s.add(And(r_3_2_1 >= 0, r_3_2_1 <= 3, r_3_2_2 >= 0, r_3_2_2 <= 3, r_3_2_3 >= 0, r_3_2_3 <= 3, r_3_2_4 >= 0, r_3_2_4 <= 3, r_3_2_5 >= 0, r_3_2_5 <= 3))
s.add(And(r_3_3_1 >= 0, r_3_3_1 <= 3, r_3_3_2 >= 0, r_3_3_2 <= 3, r_3_3_3 >= 0, r_3_3_3 <= 3, r_3_3_4 >= 0, r_3_3_4 <= 3, r_3_3_5 >= 0, r_3_3_5 <= 3))
s.add(And(r_3_4_1 >= 0, r_3_4_1 <= 3, r_3_4_2 >= 0, r_3_4_2 <= 3, r_3_4_3 >= 0, r_3_4_3 <= 3, r_3_4_4 >= 0, r_3_4_4 <= 3, r_3_4_5 >= 0, r_3_4_5 <= 3))
s.add(And(r_4_1_1 >= 0, r_4_1_1 <= 3, r_4_1_2 >= 0, r_4_1_2 <= 3, r_4_1_3 >= 0, r_4_1_3 <= 3, r_4_1_4 >= 0, r_4_1_4 <= 3, r_4_1_5 >= 0, r_4_1_5 <= 3))
s.add(And(r_4_2_1 >= 0, r_4_2_1 <= 3, r_4_2_2 >= 0, r_4_2_2 <= 3, r_4_2_3 >= 0, r_4_2_3 <= 3, r_4_2_4 >= 0, r_4_2_4 <= 3, r_4_2_5 >= 0, r_4_2_5 <= 3))
s.add(And(r_4_3_1 >= 0, r_4_3_1 <= 3, r_4_3_2 >= 0, r_4_3_2 <= 3, r_4_3_3 >= 0, r_4_3_3 <= 3, r_4_3_4 >= 0, r_4_3_4 <= 3, r_4_3_5 >= 0, r_4_3_5 <= 3))
s.add(And(w_2_1_1_1 >= 0, w_2_1_1_1 <= 3, w_2_2_1_1 >= 0, w_2_2_1_1 <= 3, w_2_3_1_1 >= 0, w_2_3_1_1 <= 3, w_3_1_2_3 >= 0, w_3_1_2_3 <= 3, w_3_2_2_3 >= 0, w_3_2_2_3 <= 3, w_3_3_2_3 >= 0, w_3_3_2_3 <= 3, w_3_4_2_3 >= 0, w_3_4_2_3 <= 3, w_4_1_3_4 >= 0, w_4_1_3_4 <= 3, w_4_2_3_4 >= 0, w_4_2_3_4 <= 3, w_4_3_3_4 >= 0, w_4_3_3_4 <= 3))
s.add(And(R_1_1_1 == 13, R_1_1_2 == 75, R_1_1_3 == 46, R_1_1_4 == 59, R_1_1_5 == 63))


totalReagents = s.minimize(r_1_1_1 + r_1_1_2 + r_1_1_3 + r_1_1_4 + r_1_1_5 + r_2_1_1 + r_2_1_2 + r_2_1_3 + r_2_1_4 + r_2_1_5 + r_2_2_1 + r_2_2_2 + r_2_2_3 + r_2_2_4 + r_2_2_5 + r_2_3_1 + r_2_3_2 + r_2_3_3 + r_2_3_4 + r_2_3_5 + r_3_1_1 + r_3_1_2 + r_3_1_3 + r_3_1_4 + r_3_1_5 + r_3_2_1 + r_3_2_2 + r_3_2_3 + r_3_2_4 + r_3_2_5 + r_3_3_1 + r_3_3_2 + r_3_3_3 + r_3_3_4 + r_3_3_5 + r_3_4_1 + r_3_4_2 + r_3_4_3 + r_3_4_4 + r_3_4_5 + r_4_1_1 + r_4_1_2 + r_4_1_3 + r_4_1_4 + r_4_1_5 + r_4_2_1 + r_4_2_2 + r_4_2_3 + r_4_2_4 + r_4_2_5 + r_4_3_1 + r_4_3_2 + r_4_3_3 + r_4_3_4 + r_4_3_5 )
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
