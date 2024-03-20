import subprocess

reagents = {}
maxDegree = 2

def getReagents(mixtures):
    '''
        Set of reagents used in mixture M
    '''
    for reagent in mixtures:
        if reagent in reagents:
            reagents[reagent] += 1
        else:
            reagents[reagent] = 1


def header(opfile):
    '''
        Takes a file pointer and add the following 2 lines in that open-file.
    '''
    opfile.write('from z3 import *\n\n')
    opfile.write('s = Optimize()\n\n')
    

def variableDeclaration(coordinates, opfile):    
    ''' 
        A_i_j_Rt == 1 if (i, j) cell is loaded with fluid Rt else 0
    '''
    opfile.write('# Variable declaration\n')
    for cell in coordinates:
        for reagent in reagents:
            opstring = ""
            opstring += 'A_'+str(cell[0])+'_'+str(cell[1])+'_'+reagent
            opstring += ' = Int("'
            opstring += 'A_'+str(cell[0])+'_'+str(cell[1])+'_'+reagent+'")\n'
            opfile.write(opstring)
    opfile.write('\n')
    '''
        V_Rt variable which denote total number of cells that are loaded with fluid Rt
    '''
    for reagent in reagents:
        opstring = ""
        opstring += 'V_'+reagent
        opstring += ' = Int("'
        opstring += 'V_'+reagent+'")\n'
        opfile.write(opstring)
    opfile.write('\n')
    '''
        d_k_Rt represent the count of k degree vertices in "HRt"
        Max degree possible is 4 as it is a grid
    '''
    for i in range(maxDegree+1):
        for reagent in reagents:
            opstring = ""
            opstring += 'd_'+str(i)+'_'+reagent+' '
            opstring += ' = Int("'
            opstring += 'd_'+str(i)+'_'+reagent+'")\n'
            opfile.write(opstring)
    opfile.write('\n')
    '''
        degree variable for each coordinate
    '''
    for cell in coordinates:
        for reagent in reagents:
            for i in range(maxDegree+1):
                opstring = ''
                opstring += 'd_'+str(cell[0])+'_'+str(cell[1])+'_'+str(i)+'_'+reagent
                opstring += ' = Int("d_'+str(cell[0])+'_'+str(cell[1])+'_'+str(i)+'_'+reagent+'")\n'
                opfile.write(opstring)
    opfile.write('\n')


def countOfReagents(coordinates, opfile):
    '''
        A_i_j_Rt is a binary variable 
        which is 1 iff cell(i, j) is filled with Rt
        else 0
    '''
    opfile.write('# Number of cells in the mixture filled with Rt reagent\n')
    for cell in coordinates:
        opstring = "s.add(And("
        for reagent in reagents:
            opstring += 'A_'+str(cell[0])+'_'+str(cell[1])+'_'+reagent + '>=0, '+ 'A_'+str(cell[0])+'_'+str(cell[1])+'_'+reagent+ '<=1, '
        opstring = opstring[:-2]
        opstring += '))\n'
        opfile.write(opstring)
    opfile.write('\n')

    '''
        V_Rt is total number of reagents in mixture which is equals to
        sum(A_i_j_Rt) for all cell(i, j)
    '''
    for reagent in reagents:
        opstring = 's.add('
        for cell in coordinates:
            opstring += 'A_'+str(cell[0])+'_'+str(cell[1])+'_'+reagent+' + '
        opstring = opstring[:-3]
        opstring += ' == V_'+reagent+')\n'
        opfile.write(opstring)
    opfile.write('\n')


def nonOverlappingConstraint(coordinates, opfile):
    '''
        If a cell (i, j) is filled with Rk reagent, i.e A_i_j_Rk == 1
        then other reagent Rj (j != k) can not occupy the cell (i, j)
    '''
    opfile.write('# If a cell is filled with reagent Rt then no reagent Rk where k != t can be filled in that cell.\n')
    for cell in coordinates:
        opstring = "s.add("
        for reagent in reagents:
            opstring += 'A_'+str(cell[0])+'_'+str(cell[1])+'_'+reagent+' + '
        opstring = opstring[:-3]
        opstring += ' == 1)\n'
        opfile.write(opstring)
    opfile.write('\n')


def conncectivityConstrsaint(coordinates, opfile):
    '''
        To attain connectivity and traceablility
    '''
    opfile.write('# To get traceability and connectivity.\n')
    neighbours = [-1, 0, 1, 0, -1] # To get all the neighbour of a cell (i, j)
    for d in range(maxDegree+1):
        for reagent in reagents:
            for cell in coordinates:
                neighbour = []
                opstring = "s.add(If(And("+"A_"+str(cell[0])+'_'+str(cell[1])+'_'+reagent+" == 1, "
                for i in range(len(neighbours)-1):
                    nx, ny = cell[0]+neighbours[i], cell[1]+neighbours[i+1]
                    if [nx, ny] in coordinates: # If the neighbour is inside the Mixture
                        neighbour.append([nx, ny])
                if len(neighbour) >= d: # it is not possible to have d > number of neighbour
                    for [nx, ny] in neighbour:
                        opstring += 'A_'+str(nx)+'_'+str(ny)+'_'+reagent+' + '
                    opstring = opstring[:-3]
                    # opstring += f' == {d}), (d_{cell[0]}_{cell[1]}_{d}_{reagent} == 1), (d_{cell[0]}_{cell[1]}_{d}_{reagent} == 0)))\n'
                    opstring += ' == '+str(d)+'), ('+'d_'+str(cell[0])+'_'+str(cell[1])+'_'+str(d)+'_'+reagent+' == 1), (d_'+str(cell[0])+'_'+str(cell[1])+'_'+str(d)+'_'+reagent+' == 0)))\n'
                    opfile.write(opstring)
    opfile.write('\n')

    for reagent in reagents:
        for d in range(maxDegree+1):
            opstring = 's.add('
            for cell in coordinates:
                opstring += 'd_'+str(cell[0])+'_'+str(cell[1])+'_'+str(d)+'_'+reagent+' + '
            opstring = opstring[:-3]
            opstring += ' == d_'+str(d)+'_'+reagent+')\n'
            opfile.write(opstring)
    opfile.write('\n')

    for reagent in reagents:
        opfile.write('s.add(Implies(V_'+reagent+' == 1, And(d_0_'+reagent+' == 1, d_1_'+reagent+' == 0, d_2_'+reagent+' == 0)))\n')
        opfile.write('s.add(Implies(V_'+reagent+' == 2, And(d_0_'+reagent+' == 0, d_1_'+reagent+' == 2, d_2_'+reagent+' == 0)))\n')
        opfile.write('s.add(Implies(V_'+reagent+' == 3, And(d_0_'+reagent+' == 0, d_1_'+reagent+' == 2, d_2_'+reagent+' == 1)))\n')
        opfile.write('s.add(Implies(V_'+reagent+' == 4, And(d_0_'+reagent+' == 0, d_1_'+reagent+' == 0, d_2_'+reagent+' == 4)))\n')

    opfile.write('\n')


def z3Condition(opfile):
    ''' 
        Values for V_Rt are fixed and stored in reagents dictionary
    '''
    opstring = "s.add(And("
    for reagent in reagents:
        opstring += 'V_'+reagent+' == '+str(reagents[reagent])+', '
    opstring = opstring[:-2] + '))\n\n'
    opfile.write(opstring)


def footer(coordinates, opfile, outfile):
    opfile.write('if s.check() == unsat:\n')
    opfile.write('\tprint("Not possible to create traceable graph for all reagents")\n')
    opfile.write('else:\n')
    opfile.write('\tfp = open(\''+outfile+'\',\'w\')\n')
    opfile.write('\tvalues = s.model()\n')
    for cell in coordinates:
        for reagent in reagents:
            opfile.write('\tif values[A_'+str(cell[0])+'_'+str(cell[1])+'_'+reagent+'] == 1:\n')
            opstring = '\t\tfp.write('
            opstring += '"'+str(cell[0])+','+str(cell[1])+','+reagent+'\\n")\n'
            opfile.write(opstring)


def createFile(mixtures, coordinates, infile, outfile):
    getReagents(mixtures) # get all the [ratio, count] in a dictionary
    global reagents
    if len(reagents) == 0:
        return []
    
    opfile = open(infile, 'w')
    header(opfile) # Adds header section to z3 file
    variableDeclaration(coordinates, opfile) # Add variables for z3 solver
    countOfReagents(coordinates, opfile) # Adds count reagents costraint to z3 solver
    nonOverlappingConstraint(coordinates, opfile) # Adds non overlapping constraint to z3 solver
    conncectivityConstrsaint(coordinates, opfile)
    z3Condition(opfile)
    footer(coordinates, opfile, outfile)
    
    opfile.close()
    reagents.clear()

    subprocess.call(["python3",infile])
    assignment = {}

    # Reading the output file that z3 produced
    outputFile = open(outfile, 'r')
    for line in outputFile:
        line = line[:-1]
        values = line.split(',')
        if values[2] in assignment:
            assignment[values[2]].append([int(values[0]), int(values[1])])
        else:
            assignment[values[2]] = [[int(values[0]), int(values[1])]]

    outputFile.close()
    return assignment


def main():
    # Avoid cases when all reagants are same.
    mixtures = ["R3", "R3", "R3", "R4"]
    coordinates = [[6,4],[6,5],[7,4],[7,5]]
    assignment = createFile(mixtures, coordinates, 'z3File.py', 'output.txt')

    for reagent in assignment:
        print(reagent, assignment[reagent])

if __name__ == "__main__":
    main()