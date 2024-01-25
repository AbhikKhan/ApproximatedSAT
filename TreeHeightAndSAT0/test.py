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


def addvariables(d, N, opfile):
    # Creating mixer variables
    opfile.write("# Adding mixer variables\n")
    for i in range(1, d+1):
        variables = ""
        for j in range(1, N+1):
            variables += f"R_{i}_{j}, "
        variables = variables[:-2]
        variables += " = Ints('"
        for j in range(1, N+1):
            variables += f"R_{i}_{j} "
        variables = variables[:-1]+"')\n"
        opfile.write(variables)
    
    # Creating reagent variables for each level
    opfile.write("\n# Creating reagent usage variable\n")
    for i in range(1, d+1):
        variables = ""
        for j in range(1, N+1):
            variables += f"x_{i}_{j}, "
        variables = variables[:-2]
        variables += " = Ints('"
        for j in range(1, N+1):
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
    opfile.write("h = Int('h')\n")
    for i in range(2, d+1):
        opfile.write(f"h_{i} = Int('h_{i}')\n")


def ratioConsistencyConstraints():
    pass        


def mixerConsistencyConstraints(d, N, opfile):   
    # Adding ratios at each mixers
    opfile.write("\n# Adding mixer consistency constraint\n")
    for i in range(1, d):
        for j in range(1, N+1):
            opfile.write(f"s.add(R_{i}_{j} == {N}*x_{i}_{j}+W_{i+1}_{i}*x_{i+1}_{j})\n")
    for j in range(1, N+1):
        opfile.write(f"s.add(R_{d}_{j} == x_{d}_{j})\n")


def nonNegativityConstraints(d, N, opfile):  
    # Adding nonnegativity constraints
    opfile.write("\n# Adding nonnegativity constraints on reagent usage\n")
    for i in range(1, d+1):
        values = "s.add(And("
        for j in range(1, N+1):
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
        for j in range(1, N+1):
            variables += f"x_{i}_{j}+"
        if i < d:
            variables += f"W_{i+1}_{i}+"
        variables = "s.add(Or("+variables[:-1]+"==0, "+variables[:-1]+"==4))\n"
        opfile.write(variables)
            

def heightConstraints(d, N, opfile):
    opfile.write("\n# Adding height constraint\n")
    for i in range(2, d+1):
        constraint = f"s.add(If("
        for j in range(1, N+1):
            constraint += f"x_{i}_{j}+"
        # If part
        constraint = constraint[:-1]+f"==0, And("
        for k in range(i, d+1):
            constraint += f"W_{k}_{k-1} == 0, "
        # Else part
        constraint = constraint[:-2]+"), And("
        for k in range(i, d+1):
            constraint += f"W_{k}_{k-1} >= 0, "
        constraint = constraint[:-2]+")))\n"
        opfile.write(constraint)
    opfile.write("\n")

    for i in range(2, d+1):
        opfile.write(f"s.add(If(W_{i}_{i-1} == 0, h_{i} == 0, h_{i} == 1))\n")

    constraint = "\ns.add(h == 1+"
    for i in range(2, d+1):
        constraint += f"h_{i}+"
    constraint = constraint[:-1]+")\n"
    opfile.write(constraint)


def setTarget(target, err, d, N, opfile):
    opfile.write("\n# Adding base condition\n")
    for i in range(1, N+1):
        condition1 = f"s.add({target[i-1]}*({N}**h) - R_1_{i} <= {err}*({N}**h))\n"
        condition2 = f"s.add(R_1_{i} - {target[i-1]}*({N}**h) <= {err}*({N}**h))\n"
        opfile.write(condition1)
        opfile.write(condition2)


def genMixing(M:list):
    outputTree = genMix(M, len(M))
    outputTree = hda(outputTree)
    saveTree(outputTree, './OutputTree/hda.png')


if __name__ == "__main__":
    N, d = 4, 4

    targetRatio = [0.30, 0.23, 0.24, 0.23]
    err = 0.007

    file = "z3Optimizer.py"
    opfile = open(file, "w+")
    initOPT(opfile)
    addvariables(d, N, opfile)
    nonNegativityConstraints(d, N, opfile)
    mixerConsistencyConstraints(d, N, opfile)
    heightConstraints(d, N, opfile)
    setTarget(targetRatio, err, d, N, opfile)
    finishOPT(opfile)
    # ratio = input('mixing ratio: ')
    # ratio = '19:15:15:15'
    # M = [(f'r{i}', int(x)) for i, x in enumerate(ratio.split(':'))]
    # genMixing(M)