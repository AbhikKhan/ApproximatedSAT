from NTM import *

def initOPT(opFile):
    opFile.write("import sys\n")
    opFile.write("import time\n")
    opFile.write("from z3 import *\n\n")
    opFile.write("s = Optimize()\n\n")


def finishOPT(opFile):
    opFile.write("\nstartTime = time.time()\n")
    opFile.write("if s.check() == sat:\n")
    opFile.write("\tfp = open(\'z3outputFile\',\'w\')\n")
    opFile.write("\tlst = s.model()\n")
    opFile.write("\tfor i in lst:\n")
    opFile.write("\t    fp.write(str(i) + \" = \" + str(s.model()[i]) + '\\n')\n")    
    opFile.write("else:\n")
    opFile.write("\tprint('unsat')\n")
    opFile.write('endTime = time.time()\n')
    opFile.write('executionTime = endTime - startTime\n')
    opFile.write("print(\"Execution Time = \",executionTime)\n")
    opFile.close()


def addvariables(d, R, opfile):
    # Creating mixer variables
    opfile.write("# Adding mixer variables\n")
    for i in range(1, d+1):
        variables = ""
        for j in range(1, R+1):
            variables += f"R_{i}_{j}, "
        variables = variables[:-2]
        variables += " = Ints('"
        for j in range(1, R+1):
            variables += f"R_{i}_{j} "
        variables = variables[:-1]+"')\n"
        opfile.write(variables)
    
    # Creating reagent variables for each level
    opfile.write("\n# Creating reagent usage variable\n")
    for i in range(1, d+1):
        variables = ""
        for j in range(1, R+1):
            variables += f"x_{i}_{j}, "
        variables = variables[:-2]
        variables += " = Ints('"
        for j in range(1, R+1):
            variables += f"x_{i}_{j} "
        variables = variables[:-1]+"')\n"
        opfile.write(variables)
    
    # Creating variables representing intermediate fluids shared between each parent and child node
    opfile.write("\n# Creating intermediate fluid share variables\n")
    for i in range(2, d+1):
        variables = ""
        variables += f"W_{i}_{i-1}"
        variables += " = Int('"
        variables += f"W_{i}_{i-1}')\n"
        opfile.write(variables)
    
    opfile.write("\n# Creating height variables\n")
    for i in range(1, d+1):
        opfile.write(f"h_{i}, H_{i} = Ints('h_{i} H_{i}')\n")


def mixerConsistencyConstraints(d, N, R, opfile):   
    # Adding ratios at each mixers
    opfile.write("\n# Adding mixer consistency constraint\n")
    for i in range(1, d):
        for j in range(1, R+1):
            opfile.write(f"s.add(R_{i}_{j} == ({N}**H_{i+1})*x_{i}_{j}+W_{i+1}_{i}*R_{i+1}_{j})\n")
    for j in range(1, R+1):
        opfile.write(f"s.add(R_{d}_{j} == x_{d}_{j})\n")


def nonNegativityConstraints(d, N, R, opfile):  
    # Adding nonnegativity constraints
    opfile.write("\n# Adding nonnegativity constraints on reagent usage\n")
    for i in range(1, d+1):
        values = "s.add(And("
        for j in range(1, R+1):
            values += f"x_{i}_{j} >= 0, x_{i}_{j} <= 4, "
        values = values[:-2]
        values += "))\n"
        opfile.write(values)
    
    opfile.write("\n# Adding nonnegativity constraints on sharing of intermediate fluids\n")
    values = "s.add(And("
    for i in range(2, d+1):
        values += f"W_{i}_{i-1} >= 0, W_{i}_{i-1} <= 3, "
    values = values[:-2]
    values += "))\n"
    opfile.write(values)

    opfile.write("\n# Adding nonnegativity constraints on total mixer units\n")
    for i in range(1, d+1):
        variables = ""
        for j in range(1, R+1):
            variables += f"x_{i}_{j}+"
        if i < d:
            variables += f"W_{i+1}_{i}+"
        variables = "s.add(Or("+variables[:-1]+"==0, "+variables[:-1]+"==4))\n"
        opfile.write(variables)
            

def heightConstraints(d, R, opfile):
    opfile.write("\n# Adding sharing constraint\n")
    for i in range(2, d+1):
        constraint = f"constraint{i} = "
        for j in range(1, R+1):
            constraint += f"x_{i}_{j}+"
        # If part
        constraint = constraint[:-1]+f"==0\n"
        opfile.write(constraint)
        condition = "And("
        for k in range(i, d+1):
            condition += f"W_{k}_{k-1} == 0, "
        condition = condition[:-2]+")"
        opfile.write(f"s.add(Implies(constraint{i}, {condition}))\n")
        # Else part
        condition = "And("
        for k in range(i, d+1):
            condition += f"W_{k}_{k-1} >= 0, "
        condition = condition[:-2]+")"
        opfile.write(f"s.add(Implies(Not(constraint{i}), {condition}))\n")

    opfile.write("\n# Adding height constraint\n")
    opfile.write("s.add(h_1 == 1)\n")
    for i in range(2, d+1):
        opfile.write(f"s.add(Implies(W_{i}_{i-1} == 0, h_{i} == 0))\n")
        opfile.write(f"s.add(Implies(W_{i}_{i-1} > 0, h_{i} == 1))\n")

    for i in range(1, d):
        constraint = f"s.add(H_{i} == H_{i+1}+h_{i})\n"
        opfile.write(constraint)
    opfile.write(f"s.add(H_{d} == h_{d})\n")
    

def setTarget(target, err, R, N, opfile):
    opfile.write("\n# Adding base condition\n")
    for i in range(1, R+1):
        condition1 = f"s.add({target[i-1]}*({N}**H_1) - R_1_{i} <= {err}*({N}**H_1))\n"
        condition2 = f"s.add(R_1_{i} - {target[i-1]}*({N}**H_1) <= {err}*({N}**H_1))\n"
        opfile.write(condition1)
        opfile.write(condition2)

def demoSetTarget(N, opfile):
    opfile.write("\n# Adding base condition\n")
    opfile.write("s.add(R_1_1 == 19)\n")
    opfile.write("s.add(R_1_2 == 15)\n")
    opfile.write("s.add(R_1_3 == 15)\n")
    opfile.write("s.add(R_1_4 == 15)\n")

def genMixing(M:list):
    outputTree = genMix(M, len(M))
    outputTree = hda(outputTree)
    saveTree(outputTree, './OutputTree/hda.png')


if __name__ == "__main__":
    N, R, d = 4, 3, 3

    # targetRatio = [0.30, 0.23, 0.24, 0.23]
    targetRatio = [0.25, 0.30, 0.45]
    err = 0.007

    file = "z3Optimizer.py"
    opfile = open(file, "w+")
    initOPT(opfile)
    addvariables(d, R, opfile)
    nonNegativityConstraints(d, N, R, opfile)
    mixerConsistencyConstraints(d, N, R, opfile)
    heightConstraints(d, R, opfile)
    setTarget(targetRatio, err, R, N, opfile)
    # demoSetTarget(N, opfile)
    finishOPT(opfile)
    # ratio = input('mixing ratio: ')
    # ratio = '19:15:15:15'
    # M = [(f'r{i}', int(x)) for i, x in enumerate(ratio.split(':'))]
    # genMixing(M)