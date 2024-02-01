from NTM import *
import subprocess

def initOPT(opFile):
    opFile.write("import sys\n")
    opFile.write("import time\n")
    opFile.write("from z3 import *\n\n")
    opFile.write("s = Optimize()\n\n")


def finishOPT(opFile, ind):
    opFile.write("\nstartTime = time.time()\n")
    opFile.write(f"fp = open(\'z3outputFile{ind}\',\'w\')\n")
    opFile.write("if s.check() == sat:\n")
    opFile.write("\tlst = s.model()\n")
    opFile.write("\tfor i in lst:\n")
    opFile.write("\t    fp.write(str(i) + \" = \" + str(s.model()[i]) + '\\n')\n")    
    opFile.write("else:\n")
    opFile.write("\tprint('unsat')\n")
    opFile.write("\tfp.write('unsat')\n")
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
    
    # opfile.write("\n# Creating height variables\n")
    # for i in range(1, d+1):
    #     opfile.write(f"h_{i}, H_{i} = Ints('h_{i} H_{i}')\n")


def mixerConsistencyConstraints(d, N, R, opfile):   
    # Adding ratios at each mixers
    opfile.write("\n# Adding mixer consistency constraint\n")
    for i in range(1, d):
        for j in range(1, R+1):
            opfile.write(f"s.add(R_{i}_{j} == ({N}**{d-i})*x_{i}_{j}+W_{i+1}_{i}*R_{i+1}_{j})\n") # Need to change in case of considering height as variable
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
        values += f"W_{i}_{i-1} > 0, W_{i}_{i-1} <= 3, " # Need to change in case of considering height as variable
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
        variables =f"s.add({variables[:-1]}==4)\n" # Need to change in case of considering height as variable
        opfile.write(variables)
            

"""
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
"""

def setTarget(target, err, R, N, d, opfile):
    opfile.write("\n# Adding base condition\n")
    for i in range(1, R+1):
        condition1 = f"s.add({target[i-1]}*({N}**{d}) - R_1_{i} <= {err}*({N}**{d}))\n"
        condition2 = f"s.add(R_1_{i} - {target[i-1]}*({N}**{d}) <= {err}*({N}**{d}))\n"
        opfile.write(condition1)
        opfile.write(condition2)


def genMixing(M:list):
    outputTree = genMix(M, len(M))
    outputTree = hda(outputTree)
    saveTree(outputTree, './OutputTree/hda.png')


if __name__ == "__main__":
    targetRatios = [[0.30, 0.23, 0.24, 0.23],
                   [0.25, 0.30, 0.45],
                   [0.35, 0.50, 0.15],
                   [0.25, 0.38, 0.25, 0.12],
                   [0.17, 0.27, 0.31, 0.25],
                   [0.15, 0.45, 0.18, 0.22],
                   [0.18, 0.39, 0.23, 0.2]]
    errs = [0.007, 0.007, 0.003, 0.009, 0.01, 0.015, 0.006]
    ind = 0
    for targetRatio, err in zip(targetRatios, errs):
        N, R, d = 4, len(targetRatio), 3
        while d< 10:
            file = "z3Optimizer.py"
            opfile = open(file, "w+")
            initOPT(opfile)
            addvariables(d, R, opfile)
            nonNegativityConstraints(d, N, R, opfile)
            mixerConsistencyConstraints(d, N, R, opfile)
            setTarget(targetRatio, err, R, N, d, opfile)
            finishOPT(opfile, ind)
            subprocess.call(["python3","z3Optimizer.py"])
            z3File = open(f'z3outputFile{ind}', "r")
            if(z3File.read() == "unsat"):
                d+=1
            else:
                break
        ind+=1