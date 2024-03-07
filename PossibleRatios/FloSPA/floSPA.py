import subprocess
import networkx as nx
from collections import deque
import pandas as pd
from openpyxl import load_workbook

from .PathWayTree import *
from .showImages import *
from .parseTree import *

from .NTM import *
from .LAFCADFL import *

__Id = 1
__IdStorage = 1

k = 100
    

# To store the information about nodes having more than one children and add constraint to limit the edge weight to < 2
moreThanOneChild = {}
    

def getNewTempVar():
    # Returns a new temporary variable
    global __Id
    newVar = "t"+str(__Id)
    __Id = __Id + 1
    return newVar

def getNewTempVarForStorage():
    # Returns a new temporary variable
    global __IdStorage
    newVar = "s"+str(__IdStorage)
    __IdStorage = __IdStorage + 1
    return newVar

def initOPT(opFile):
#===============================================================================
# init() appends the initial conditions for the z3 solver to analyze the clauses
#===============================================================================
    opFile.write("import sys\n")
    opFile.write("import time\n")
    opFile.write("sys.path.append(\"/home/sukanta/App/z3-master/build\")\n")
    opFile.write("from z3 import *\n\n")
    opFile.write("s = Optimize()\n")
    #opFile.write("s.set(priority='pareto')\n")
    
def finishOPT(G,opFile):
    
    opString = "totalReagents = " + "s.minimize("
    for u in G.nodes():
        reagentList = G.nodes[u]['reagent']
        for (reagentStr,_) in reagentList:
            opString += reagentStr + " + "
    opString = opString[:-2] + ")\n"
    opFile.write(opString)
    opFile.write("startTime = time.time()\n")
    opFile.write("fp = open(\'z3opFile\',\'w\')\n")
    opFile.write("if s.check() == sat:\n")
    opFile.write("\tprint(\"Total reagents = \", totalReagents.value())\n")
    opFile.write("\tlst = s.model()\n")
    opFile.write("\tfor i in lst:\n")
    opFile.write("\t    fp.write(str(i) + \" = \" + str(s.model()[i]) + '\\n')\n")    
    opFile.write("else:\n")
    opFile.write("\tfp.write('unsat')\n")
    opFile.write("\tprint('unsat')\n")
    opFile.write('endTime = time.time()\n')
    opFile.write('executionTime = endTime - startTime\n')
    opFile.write("print(\"Execution Time = \",executionTime)\n")
    opFile.close()

def annotatePathWayTree(G,ipRatio):
    # Annotate mixing tree with (variables, value) pairs
    # added as node attributes
    numReagents = len(ipRatio)    #numReagent = number of reagents
    for v in G.nodes():
        # put ratio and input reagent variables in each node
        # R_l_i_reagent-number, r_l_i_reagnet-number; 1 <= reagent_number <= numReagents
        ratioList = []
        reagentList = []
        l = G.nodes[v]['level']
        i = G.nodes[v]['index']
        for reagentNumber in range(1,numReagents+1):
            ratioVar = 'R_' + str(l) + "_" + str(i) + "_" + str(reagentNumber)
            reagentVar = 'r_' + str(l) + "_" + str(i) + "_" + str(reagentNumber)
            ratioList.append([ratioVar,0])
            reagentList.append([reagentVar,0])
        #Add variables to node
        G.nodes[v]['ratio'] = ratioList[:]
        G.nodes[v]['reagent'] = reagentList[:]
    
    # Add edge attributes
    for (u,v) in G.edges():
        (l_u,i_u) = (G.nodes[u]['level'], G.nodes[u]['index'])
        (l_v,i_v) = (G.nodes[v]['level'], G.nodes[v]['index'])
        
        edgeVar = "w_" + str(l_v) + "_" + str(i_v) + "_" + str(l_u) + "_" + str(i_u)
        G[u][v]['edgeVar'] = [edgeVar,0]
        key = edgeVar[-3:]
        if key in moreThanOneChild:
            moreThanOneChild[key].append(edgeVar)
        else:
            moreThanOneChild[key] = [edgeVar]
        
def addvariables(G,opFile):
    for v in G.nodes():
        opString1 = ""
        opString2 = " = Ints('"
        #print type(G.nodes[v]['ratio'])
        for (ratioVar,_) in G.nodes[v]['ratio']:
            opString1 += ratioVar + ", "
            opString2 += ratioVar + " "
        opString1 = opString1[:-2] + " "
        opString2 = opString2[:-1] + "')\n"
        opFile.write(opString1)
        opFile.write(opString2)
        
        opString1 = ""
        opString2 = " = Ints('"
        for (reagentVar,_) in G.nodes[v]['reagent']:
            opString1 += reagentVar + ", "
            opString2 += reagentVar + " " 
        
        opString1 = opString1[:-2] + ", s_"+ str(G.nodes[v]['level']) + "_" + str(G.nodes[v]['index']) + " "
        opString2 = opString2[:-1] + " s_"+ str(G.nodes[v]['level']) + "_" + str(G.nodes[v]['index']) + "')# Added reagent variables\n"
        opFile.write(opString1)
        opFile.write(opString2)
        
    # Add edge variables
    opString1 = ""
    if len(G.edges()) == 1:
        opString2 = " = Int('"
    else:
        opString2 = " = Ints('"
    
    for (u,v) in G.edges():
        opString1 += G[u][v]['edgeVar'][0] + ", "
        opString2 += G[u][v]['edgeVar'][0] + " "
        
    opString1 = opString1[:-2] + " "
    opString2 = opString2[:-1] + "')# Added edgeVariables\n\n"
    if len(G.edges()) > 0:
        opFile.write(opString1)
        opFile.write(opString2)
          
def ratioConsistencyConstraintsWithLinerarization(G,opFile,factorList,ratioList):
    numRatio = len(ratioList)
    newFactorList = factorList[:]
    newFactorList.reverse()
    print("Reversed: ", newFactorList)
    
    #For each node generate clauses
    for u in G.nodes(): 
        # calculate the multiplicative factor of input reagent
        reagentWeight = 1
        (l_u,i_u,h_u) = (G.nodes[u]['level'],G.nodes[u]['index'],G.nodes[u]['height'])
        for j in range(l_u,l_u+h_u-1):
            reagentWeight = reagentWeight * newFactorList[j]
            
        # calculate weight for each outgoing edges---(CHANGES REQUIRE for multilevel sharing)****
        edgeVarDict = dict()        #Each entry is of the form:  edgeVar : edgeWeight
        for e in G.out_edges(u):    # e = (u,v) i.e., u -> v, e[0] -> e[1]
            v = e[1]
            (l_v,i_v,h_v) = (G.nodes[v]['level'],G.nodes[v]['index'],G.nodes[v]['height'])
            edgeWeight = 1
            for j in range(l_u+h_v,l_u+h_u-1):
                edgeWeight = edgeWeight * newFactorList[j]
            edgeVar = "w_"+str(l_v)+"_"+str(i_v)+"_"+str(l_u)+"_"+str(i_u)
            edgeVarDict[edgeVar] = edgeWeight       

        # Generate clauses for each reagent in a mixing node 
        # tempVarDict stores new temporary variables generated during linearization  
        # Each entry is of the form -- t_i : (edgeVar, reagentVar, mixerSize(v)) ; u->v
        tempVarDict = dict()  
        opString = ""                  
        for i in range(numRatio):
            opString += "s.add(" + str(reagentWeight) + "*" + G.nodes[u]['reagent'][i][0] + " + "
            
            for e in G.out_edges(u):
                v = e[1]
                (l_v,i_v,h_v) = (G.nodes[v]['level'],G.nodes[v]['index'],G.nodes[v]['height'])
                edgeVar = "w_"+str(l_v)+"_"+str(i_v)+"_"+str(l_u)+"_"+str(i_u)
                edgeWeight = edgeVarDict[edgeVar]
                reagentVar = G.nodes[v]['ratio'][i][0]
                mixerSize = G.nodes[v]['mixerSize']
                t_i = getNewTempVar()
                tempVarDict[t_i] = (edgeVar,reagentVar,mixerSize)
                opString += str(edgeWeight) + "*" + t_i + " + "
                
            opString = opString[:-2] + " == " + G.nodes[u]['ratio'][i][0] +")\n"
            # write opString after declaring variables
            #opFile.write(opString)
                    
        # Generate linearization clauses
        for t_i in tempVarDict.keys():
            varDecStr = t_i + " = Int('" + t_i + "')\n"
            opFile.write(varDecStr) 
            
        opFile.write(opString)
        opFile.write("\n")
            
        for t_i in tempVarDict.keys():
            (edgeVar,reagentVar,mixerSize) = tempVarDict[t_i]
            opString = 's.add(Implies((' + edgeVar + ' == 0), (' + t_i + " == 0)))\n"
            opFile.write(opString)
            for loopVar in range(1,mixerSize):
                opString = 's.add(Implies((' + edgeVar + ' == ' + str(loopVar) + '), (' + t_i  \
                                                + ' == ' + str(loopVar) + '*' + reagentVar + ')))\n'
                opFile.write(opString)  
            opFile.write('\n')

        
def mixerConsistencyConstraints(G,opFile):   
    #For each node generate clauses --- CHANGE REQUIRE for multilevel sharing
    for u in G.nodes():     
        opString = ""
        reagentList = G.nodes[u]['reagent']
        for (reagentStr,_) in reagentList:
            opString += reagentStr + " + "
        # for each incoming edges
        for (x,y) in G.out_edges(u):
            opString += G[x][y]['edgeVar'][0] + " + "
        opString = opString[:-2] + " == "
        opStringNew = "s.add(Or(" + opString + str(G.nodes[u]['mixerSize']) + ", " + opString + "0))\n"
        opFile.write(opStringNew)
        
        if len(G.in_edges(u)) != 0:
            opString = "s.add("
            for (x,y) in G.in_edges(u):
                opString += G[x][y]['edgeVar'][0] + " + "
            opString = opString[:-2] + " <= " + str(G.nodes[u]['mixerSize']) + ")\n"
            opFile.write(opString) 
            
def nonNegativityConstraints(G,opFile):  
    #For each reagent variables set bound
    for u in G.nodes():     
        opString = "s.add(And("
        reagentList = G.nodes[u]['reagent']
        for (reagentStr,_) in reagentList:
            opString += reagentStr + " >= 0, " + reagentStr + " <= "+ str(G.nodes[u]['mixerSize']-1) + ", "
        opString = opString[:-2] + "))\n"
        opFile.write(opString)
    # for each segment sharing variables set bound
    opString = "s.add(And("
    for (x,y) in G.out_edges():
        edgeVar = G[x][y]['edgeVar'][0]
        opString += edgeVar + " >= 0, " + edgeVar + " <= " + str(G.nodes[y]['mixerSize']-1) + ", "
    opString = opString[:-2] + "))\n"
    if len(G.edges()) > 0:
        opFile.write(opString)

# getNewTempVarForStorage()    
def storageConstraint(G, opFile, k):
    for u in G.nodes():
        # storage for leaf nodes are 0
        if G.nodes[u]['height'] == 1:        # leaf node has height = 1
            opString = "s.add(s_" +  str(G.nodes[u]['level']) + "_" + str(G.nodes[u]['index']) + " == 0)\n"            
            opFile.write(opString)
        else:
            # storage constraint for internal node
            tempList = [] # Each entry is of the form (s?,s_?_?)
            # for each incoming edges - compute temporary storage variables
            for (x,y) in G.out_edges(u):
                newTempStorageVar = getNewTempVarForStorage()  
                opString = newTempStorageVar + " = Int('" + newTempStorageVar +"')\n"
                opFile.write(opString)
                
                edgeVar = G[x][y]['edgeVar'][0]
                storageVar = "s_" + str(G.nodes[y]['level']) + "_" + str(G.nodes[y]['index'])
                opString = "s.add(" + newTempStorageVar + " == If(" + edgeVar + " > 0, "
                opString += "If(" +  edgeVar + " > " + storageVar + ", " +  edgeVar + ", " + storageVar + "),0))\n"
                opFile.write(opString)
                tempList.append((newTempStorageVar,storageVar))
            # Now add storage constraint 
            print(tempList)
            opString = "s.add(Or("
            for i in range(len(tempList)):
                opString += "s_" + str(G.nodes[u]['level']) + "_" + str(G.nodes[u]['index']) + " == "
                for j in range(len(tempList)):
                    (newTempStorageVar,storageVar) = tempList[j]                    
                    if i == j:
                        opString += storageVar + " + "
                    else:
                        opString += newTempStorageVar + " + "
                opString = opString[:-2] + ", " 
            opString = opString[:-2] + "))\n\n"
            opFile.write(opString)
    # Add storage constraint for root
    opString = "s.add(s_1_1 <= " + str(k) + ")\n\n"
    opFile.write(opString) 

             
def limitEdges(opFile):
    opstring = "s.add(And("
    f = 0
    for key in moreThanOneChild:
        if len(moreThanOneChild[key]) > 1:
            for edgeWeight in moreThanOneChild[key]:
                opstring += edgeWeight + "< 3, "
                f = 1
    opstring = opstring[:-2]
    opstring += ')) # Added constraint to limit the edge weight weight\n\n'
    if f == 1:
        opFile.write(opstring)


def setTarget(G,opFile,ratioList):
    # Root node has id = 1
    rootRatioList = G.nodes[1]['ratio']
    opString = "s.add(And("
    for i in range(len(ratioList)):
        (ratioStr,_) = rootRatioList[i]
        opString += ratioStr + " == " + str(ratioList[i]) + ", "
    opString = opString[:-2] + "))\n\n\n"
    opFile.write(opString)
    
#-------------------------------------------------------------------------
#--------------------Printing tree----------------------------------------        
#-------------------------------------------------------------------------        
    
def annotateMixingTreeWithValue(G,ipFileName):
    # Put ratio, reagent, and segment sharing values into tree from SAT output
    fp = open(ipFileName,"r")
    varDict = dict()    #Stores variable assignments
    for line in fp:
        #print line
        [varName,_,value] = line.split()
        #print varName, value
        if varName[0] != 't':
            varDict[varName] = value
    
    # Annotate nodes of G
    for u in G.nodes():
        reagentList = G.nodes[u]['reagent']
        ratioList = G.nodes[u]['ratio'] 
        for i in range(len(reagentList)):
            reagentVar = reagentList[i][0]
            if reagentVar in varDict.keys():
                G.nodes[u]['reagent'][i][1] = varDict[reagentVar]
        
        for i in range(len(ratioList)):
            ratioVar = ratioList[i][0]
            if ratioVar in varDict.keys():
                G.nodes[u]['ratio'][i][1] = varDict[ratioVar]
                
    # Annotate edges of G
    for (x,y) in G.out_edges():
        edgeVar = G[x][y]['edgeVar'][0]
        if edgeVar in varDict.keys():
            G[x][y]['edgeVar'][1] = varDict[edgeVar]


def printTreeAfterAnnotation(G, filename):   
    # Generate dot file after annotating tree with SAT output 
    fp = open(filename,'w')
    string = 'digraph "DD" { \n' + "graph [ ordering = \"out\"];\n" 
    fp.write(string)
    numReagents = len(G.nodes[1]['ratio'])
    __tempId = 5000 # For reagent nodes in dot file
    for u in G.nodes():
        ratioList = []
        reagentList = []
        for i in range(numReagents):
            ratioList.append(G.nodes[u]['ratio'][i][1])
            reagentList.append(G.nodes[u]['reagent'][i][1])
                   
        fp.write(str(u)+ " [label = \"" + str(ratioList)+ "\\n" + str(G.nodes[u]['mixerSize']) + "\"];\n")
        
        # For each nonzero reagent print in the output file
        for i in range(numReagents):
            (_,reagentVal) = G.nodes[u]['reagent'][i]
            if reagentVal != str(0):
                fp.write(str(__tempId) + " [shape=\"box\",label = \"R%d\"];\n"%(i+1))
                fp.write(str(u)+ " -> "+str(__tempId)+ "[label =" + reagentVal +"];")
                __tempId = __tempId + 1
        
    for e in G.edges():
        (u,v) = e
        if G[u][v]['edgeVar'][1] != str(0):
            fp.write(str(u) + " -> " + str(v) +  "[label = " + str(G[u][v]['edgeVar'][1])+"];\n" )
    fp.write('}\n') 
    fp.close()
        

# <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<CHANGES MADE>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

def getInputRatio(ratioList):
    input_ratio = []
    for i, ratio in enumerate(ratioList):
        input_ratio.append((f'R{i}', ratio))
    
    return input_ratio

def getName(ratioList):
    name = ''
    for ratio in ratioList:
        name += str(ratio) + '_'
    
    return name[:-1]

def getMix(root):
    '''
        Returns a dictionary that contains all the mixtures and their ratio list
        Simple BFS will work
    '''
    queue = deque()
    queue.append(root)
    mixture = dict()

    while queue:
        s = len(queue)
        nodes = []
        while s:
            s -= 1
            node = queue.popleft()
            reags = []
            nodes += [child for child in node.children if child.children != []]
            for child in node.children:
                reags.extend([child.value]*child.volume)
            mixture[node.value] = reags

        for n in nodes:
            queue.append(n)
    return mixture

def boundingbox(assignments):
    uniqueCells = set()
    x_max, y_max, x_min, y_min = 0, 0, 15, 15
    for mix in assignments:
        for cell in assignments[mix]:
            uniqueCells.add(''.join(str(coord) for coord in cell))
            x_max = max(x_max, cell[0])
            x_min = min(x_min, cell[0])
            y_max = max(y_max, cell[1])
            y_min = min(y_min, cell[1])
    
    area = (x_max - x_min + 1) * (y_max - y_min + 1)
    return len(uniqueCells), area
            
def KBL(assignment, mixtures, timestamp):
    '''
        Returns KBL information of a mixing tree
    '''
    allFlow, allBendings, allLengths = 0, 0, 0
    row, col = 10, 10
    grid = []
    parent = dict() # Stores parent coordinates
    for mix in mixtures:
        for reagent in mixtures[mix]:
            if reagent[0] == 'M':
                if reagent not in parent:
                    parent[reagent] = assignment[mix][:]
    parent['M0'] = assignment['M0'][:]
    for _ in range(row):
        grid.append(['*']*col)
    # Get the parallel loading cells in each time stamp
    for t in timestamp:
        # Make the grid
        Mixtures = dict()
        loadingCells = dict() # Cells that participate in mixing at current timestamp
        reagentList = dict() # List of reagents used in mixture M1
        blockageList = dict() # List of intermediate fluids in each mixture
        units = dict() # Units of intermediate fluids needed in mixtures

        print("timestamp", t)
        for mix in timestamp[t]: # Mi Mj etc
            Mixtures[mix] = assignment[mix][:]
            loadingCells[mix] = assignment[mix][:]
            reagents = []
            blockage = dict() # Store blockage list for each mixture Mi
            unit = dict() # Store units of intermediate fluids required
            for reagent in mixtures[mix]:
                if reagent[0] == 'M': # indicates intermediate fluid (blockage)
                    if reagent not in blockage:
                        blockage[reagent] = []
                        unit[reagent] = 1
                        for cell in assignment[reagent]:
                            if cell in assignment[mix]:
                                blockage[reagent].append(cell)
                            else:
                                grid[cell[0]][cell[1]] = '*' # Washing
                    else:
                        unit[reagent] += 1
                else:
                    reagents.append(reagent)
            # Reagents are in reagents
            reagentList[mix] = reagents #list
            # Blockages are in blockage and their positions
            blockageList[mix] = blockage #dict
            # Intermediate fluid units are stored in units
            units[mix] = unit #dict

        loadingPaths = getPlacementAndLoading(Mixtures, parent, loadingCells, reagentList, blockageList, units, grid)
        totalPathLength, totalBendings = 0, 0
        for order in loadingPaths:
            totalBendings += order[1]
            totalPathLength += len(order[2])
            print(order[0], 'Bendings:', order[1], 'Path Length:', len(order[2]))
        
        print('Flow:', len(loadingPaths), ',Total Bendings:', totalBendings, ',Total Path Length:', totalPathLength)
        allFlow += len(loadingPaths)
        allBendings += totalBendings
        allLengths += totalPathLength
    
    print('K', allFlow, 'B', allBendings, 'L', allLengths)
    return allFlow, allBendings, allLengths

def getPlacementAndTimestamp(root):
    '''
        Generate the tree from the list provided
        Use NTM to get the placement of the tree and time stamp at which each mixture will execute
    '''
    ntmroot = listToTree(root)
    output_assignment_set = ntm(ntmroot, [5, 5], [1]) # returns [moduleID, timeStamp, Binding, WashSequence] for every sequence

    # Get the corrospondence mixture reagents and intermediate fluids
    mixture = getMix(ntmroot)

    # Assignment of all the internal node
    assignment = {}
    # timestamp at which particular mixture is going to execute
    timeStamp = {}
    for item in output_assignment_set:
        if item[0][0] == 'M':
            assignment[item[0]] = item[2]
            if item[1] not in timeStamp:
                timeStamp[item[1]] = [item[0]]
            else:
                timeStamp[item[1]].append(item[0])

    BB, area = boundingbox(assignment)
    print("area ", area)
    K, B, L = KBL(assignment, mixture, timeStamp)
    return BB, area, K, B, L


def parseZ3opFile(file, N):
    '''
        Returns waste, mixer and reagent usage by parsing z3output file
    '''
    waste = 0
    reagentUsage = [0]*N
    mixer = 1
    with open(file, 'r') as ipfile:
        line = ipfile.readline()
        if line == 'unsat':
            return -1, -1, reagentUsage
        while line:
            all = line.split(' = ')
            if all[0][0] == 'w':
                shared = int(all[1])
                # print(shared)
                if shared > 0:
                    waste += 4-shared
                    mixer += 1
            elif all[0][0] == 'r':
                reagentUsage[int(all[0][-1])-1] += int(all[1])
            line = ipfile.readline()
    return waste, mixer, reagentUsage


# To get KBL parameter
def getKBL(ratioList, z3fileName):
    input_ratio = getInputRatio(ratioList)
    root = genMix(input_ratio, 4)
    # Create skeleton tree
    G = createSkeletonTreeNew(root)
    putIndexInSkeletonTree(G)
    putHeightInSkeletonTree(G)
    printTreeAfterAdding_lih(G,"skeletonTreeAfterAdding_lih.dot")
    
    # Add floSPA constraints
    annotatePathWayTree(G, ratioList)
    annotateMixingTreeWithValue(G, z3fileName)
    printTreeAfterAnnotation(G, 'skeletonTreeAfterAnnotation.dot')
    newroot = getRoot("skeletonTreeAfterAnnotation.dot")
    A, BB, K, B, L = getPlacementAndTimestamp(newroot)

    return A, BB, K, B, L


def floSPA(root, ratioList, factorList, name):
    '''
        Use floSPA to generate the mixing tree.
    '''
    # Create skeleton tree
    G = createSkeletonTreeNew(root)
    putIndexInSkeletonTree(G)
    putHeightInSkeletonTree(G)
    printTreeAfterAdding_lih(G,"skeletonTreeAfterAdding_lih.dot")
    
    # Add floSPA constraints
    annotatePathWayTree(G, ratioList)
    opFile = open('z3clauses.py','w')
    initOPT(opFile)
    addvariables(G,opFile)
    ratioConsistencyConstraintsWithLinerarization(G, opFile, factorList, ratioList)

    mixerConsistencyConstraints(G,opFile)
    nonNegativityConstraints(G,opFile)
    setTarget(G,opFile,ratioList)
    finishOPT(G,opFile)
    subprocess.call(["python3","z3clauses.py"])
    # To get waste and reagent usage
    waste, mixer, reagentUsage = parseZ3opFile('z3opFile', len(ratioList))
    if waste != -1:
        annotateMixingTreeWithValue(G,'z3opFile')
        printTreeAfterAnnotation(G, 'skeletonTreeAfterAnnotation.dot')
        subprocess.check_call(['dot', '-Tpng', 'skeletonTreeAfterAnnotation.dot', '-o', name])
    moreThanOneChild.clear()

    return waste, mixer, reagentUsage


"""
    To create skeletonTree from from ratio list
"""
def skeletonTreeGeneration(ratioList, factorList, outputFilePath):
    input_ratio = getInputRatio(ratioList)
    root = genMix(input_ratio, 4)
    return floSPA(root, ratioList, factorList, outputFilePath)


if __name__ == '__main__':
    real = [
        [13, 29, 22]
    ]
    fact = [
        [4, 4, 4]
    ]
    for i in range(len(real)):
        print(real[i])
        name = getName(real[i])
        waste, mixer, reagentUsage = skeletonTreeGeneration(real[i], fact[i], f'./outputFloSPA/{name}.png')
        print(getKBL(real[i], 'z3opFile'))
