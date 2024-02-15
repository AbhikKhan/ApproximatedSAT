'''
Created on 26-Jul-2017
@author: sukanta
'''

import subprocess
import networkx as nx
import PathWayTree as PWT
__Id = 1
__IdStorage = 1

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
        reagentList = G.node[u]['reagent']
        for (reagentStr,_) in reagentList:
            opString += reagentStr + " + "
    opString = opString[:-2] + ")\n"
    opFile.write(opString)
      
    opFile.write("startTime = time.time()\n")
    opFile.write("print s.check()\n")
    #opFile.write("while s.check() == sat:\n")
    #opFile.write("    print \"sample = \", sample.value(), \"buffer = \", buff.value()\n")
    opFile.write("print \"Total reagents = \", totalReagents.value() \n")
    opFile.write('endTime = time.time()\n')
    opFile.write('executionTime = endTime - startTime\n')
    opFile.write("print \"Execution Time = \",executionTime\n")
    #For printing SAT assignments 
    opFile.write("fp = open(\'op\',\'w\')\n")
    opFile.write("lst = s.model()\n")
    opFile.write("for i in lst:\n")
    opFile.write("    fp.write(str(i) + \" = \" + str(s.model()[i]) + '\\n')\n")    
     
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
        l = G.node[v]['level']
        i = G.node[v]['index']
        for reagentNumber in range(1,numReagents+1):
            ratioVar = 'R_' + str(l) + "_" + str(i) + "_" + str(reagentNumber)
            reagentVar = 'r_' + str(l) + "_" + str(i) + "_" + str(reagentNumber)
            ratioList.append([ratioVar,0])
            reagentList.append([reagentVar,0])
        #Add variables to node
        G.node[v]['ratio'] = ratioList[:]
        G.node[v]['reagent'] = reagentList[:]
    
    # Add edge attributes
    for (u,v) in G.edges():
        (l_u,i_u) = (G.node[u]['level'], G.node[u]['index'])
        (l_v,i_v) = (G.node[v]['level'], G.node[v]['index'])
        
        edgeVar = "w_" + str(l_v) + "_" + str(i_v) + "_" + str(l_u) + "_" + str(i_u)
        G[u][v]['edgeVar'] = [edgeVar,0]
        

def addvariables(G,opFile):
    for v in G.nodes():
        opString1 = ""
        opString2 = " = Reals('"
        #print type(G.node[v]['ratio'])
        for (ratioVar,_) in G.node[v]['ratio']:
            opString1 += ratioVar + ", "
            opString2 += ratioVar + " "
        opString1 = opString1[:-2] + " "
        opString2 = opString2[:-1] + "')\n"
        opFile.write(opString1)
        opFile.write(opString2)
        
        opString1 = ""
        opString2 = " = Ints('"
        for (reagentVar,_) in G.node[v]['reagent']:
            opString1 += reagentVar + ", "
            opString2 += reagentVar + " " 
        
        opString1 = opString1[:-2] + ", s_"+ str(G.node[v]['level']) + "_" + str(G.node[v]['index']) + " "
        opString2 = opString2[:-1] + " s_"+ str(G.node[v]['level']) + "_" + str(G.node[v]['index']) + "')\n"
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
    opString2 = opString2[:-1] + "')\n\n"
    opFile.write(opString1)
    opFile.write(opString2)
    
        
def ratioConsistencyConstraintsWithLinerarization(G,opFile,factorList,ratioList):
    numRatio = len(ratioList)
    newFactorList = factorList[:]
    newFactorList.reverse()
    #print "Reversed: ", newFactorList
    
    #For each node generate clauses
    for u in G.nodes(): 
        (l_u,i_u) = (G.node[u]['level'],G.node[u]['index'])
        #--------------------New constraint-------------------------
        # sum(R_?_?_i) = 1
        '''
        opString = ""                  
        for i in range(numRatio):
            opString += G.node[u]['ratio'][i][0] + " + "
        opString = "s.add(Or(" +opString[:-2] + "== 1," + opString[:-2] + "== 0))\n"
        opFile.write(opString)
        '''
        
        opString = ""                  
        for i in range(numRatio):
            opString += G.node[u]['ratio'][i][0] + " + "
        opString = "s.add(" +opString[:-2] + "<= 1)\n"
        opFile.write(opString)
        
        
        # Generate clauses for each reagent in a mixing node 
        # tempVarDict stores new temporary variables generated during linearization  
        # Each entry is of the form -- t_i : (edgeVar, reagentVar, mixerSize(v)) ; u->v
        tempVarDict = dict()  
        opString = ""                  
        for i in range(numRatio):
            opString += "s.add(" + G.node[u]['reagent'][i][0] + " + "
            
            for e in G.out_edges(u):
                v = e[1]
                (l_v,i_v) = (G.node[v]['level'],G.node[v]['index'])
                edgeVar = "w_"+str(l_v)+"_"+str(i_v)+"_"+str(l_u)+"_"+str(i_u)
                #edgeWeight = edgeVarDict[edgeVar]
                reagentVar = G.node[v]['ratio'][i][0]
                mixerSize = G.node[v]['mixerSize']
                t_i = getNewTempVar()
                tempVarDict[t_i] = (edgeVar,reagentVar,mixerSize)
                opString += t_i + " + "
                
            opString = opString[:-2] + " == " + str(G.node[u]['mixerSize']) + "*" + G.node[u]['ratio'][i][0] +")\n"
            # write opString after declaring variables
                    
        # Generate linearization clauses
        for t_i in sorted(tempVarDict.keys()):
            varDecStr = t_i + " = Real('" + t_i + "')\n"
            opFile.write(varDecStr) 
            
        opFile.write(opString)
        opFile.write("\n")
            
        for t_i in sorted(tempVarDict.keys()):
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
        reagentList = G.node[u]['reagent']
        for (reagentStr,_) in reagentList:
            opString += reagentStr + " + "
        # for each incoming edges
        for (x,y) in G.out_edges(u):
            opString += G[x][y]['edgeVar'][0] + " + "
        opString = opString[:-2] + " == "
        opStringNew = "s.add(Or(" + opString + str(G.node[u]['mixerSize']) + ", " + opString + "0))\n"
        opFile.write(opStringNew)
        
        if len(G.in_edges(u)) != 0:
            opString = "s.add("
            for (x,y) in G.in_edges(u):
                opString += G[x][y]['edgeVar'][0] + " + "
            opString = opString[:-2] + " <= " + str(G.node[u]['mixerSize']) + ")\n"
            opFile.write(opString) 
            
def nonNegativityConstraints(G,opFile):  
    #For each reagent variables set bound
    for u in G.nodes():     
        opString = "s.add(And("
        reagentList = G.node[u]['reagent']
        for (reagentStr,_) in reagentList:
            opString += reagentStr + " >= 0, " + reagentStr + " <= "+ str(G.node[u]['mixerSize']-1) + ", "
        opString = opString[:-2] + "))\n"
        opFile.write(opString)
    # for each segment sharing variables set bound
    opString = "s.add(And("
    for (x,y) in G.out_edges():
        edgeVar = G[x][y]['edgeVar'][0]
        opString += edgeVar + " >= 0, " + edgeVar + " <= " + str(G.node[y]['mixerSize']-1) + ", "
    opString = opString[:-2] + "))\n"
    opFile.write(opString)

# getNewTempVarForStorage()    
def storageConstraint(G, opFile, k):
    for u in G.nodes():
        # storage for leaf nodes are 0
        if G.node[u]['height'] == 1:        # leaf node has height = 1
            opString = "s.add(s_" +  str(G.node[u]['level']) + "_" + str(G.node[u]['index']) + " == 0)\n"            
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
                storageVar = "s_" + str(G.node[y]['level']) + "_" + str(G.node[y]['index'])
                opString = "s.add(" + newTempStorageVar + " == If(" + edgeVar + " > 0, "
                opString += "If(" +  edgeVar + " > " + storageVar + ", " +  edgeVar + ", " + storageVar + "),0))\n"
                opFile.write(opString)
                tempList.append((newTempStorageVar,storageVar))
            # Now add storage constraint 
            print(tempList)
            opString = "s.add(Or("
            for i in range(len(tempList)):
                opString += "s_" + str(G.node[u]['level']) + "_" + str(G.node[u]['index']) + " == "
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
    opString = "s.add(s_1_1 <= " + str(k) + ")\n"
    opFile.write(opString) 
             
    
    
def setTarget(G,opFile,ratioList):
    # Root node has id = 1
    rootRatioList = G.node[1]['ratio']
    opString = "s.add(And("
    for i in range(len(ratioList)):
        (ratioStr,_) = rootRatioList[i]
        opString += ratioStr + " == (1.0*" + str(ratioList[i]) +")/"+str(sum(ratioList)) + ", "
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
        reagentList = G.node[u]['reagent']
        ratioList = G.node[u]['ratio'] 
        for i in range(len(reagentList)):
            reagentVar = reagentList[i][0]
            if reagentVar in varDict.keys():
                G.node[u]['reagent'][i][1] = varDict[reagentVar]
        
        for i in range(len(ratioList)):
            ratioVar = ratioList[i][0]
            if ratioVar in varDict.keys():
                G.node[u]['ratio'][i][1] = varDict[ratioVar]
                
    # Annotate edges of G
    for (x,y) in G.out_edges():
        edgeVar = G[x][y]['edgeVar'][0]
        if edgeVar in varDict.keys():
            G[x][y]['edgeVar'][1] = varDict[edgeVar]
            
        
def printTreeAfterAnnotation(G,filename):   
    # Generate dot file after annotating tree with SAT output 
    fp = open(filename,'w')
    string = 'digraph "DD" { \n' + "graph [ ordering = \"out\"];\n" 
    fp.write(string)
    numReagents = len(G.node[1]['ratio'])
    __tempId = 5000 # For reagent nodes in dot file
    for u in G.nodes():
        ratioList = []
        reagentList = []
        for i in range(numReagents):
            ratioList.append(G.node[u]['ratio'][i][1])
            reagentList.append(G.node[u]['reagent'][i][1])
                   
        fp.write(str(u)+ " [label = \"" + str(ratioList)+ "\\n" + str(G.node[u]['mixerSize']) + "\"];\n")
        
        # For each nonzero reagent print in the output file
        for i in range(numReagents):
            (_,reagentVal) = G.node[u]['reagent'][i]
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
        


# ratioList = [22,14,14,14]
# factorList = [4,4,4]

# ratioList = [102,26,2,2,124]
# factorList = [4,4,4,4]
 
# ratioList = [19,15,15,15]
# factorList = [4,4,4]

# ratioList = [300,499,225]
# factorList = [4,4,4,4,4]
 
 
# ratioList = [9,26,29]
# factorList = [4,4,4]

# ratioList = [56,113,87]
# factorList = [4,4,4,4]

# ratioList = [25, 123, 108]
# factorList = [4,4,4,4]
 
ratioList = [27,25,57,69,78]
factorList = [4,4,4,4]
k = 2

root = PWT.createPathWayMixingTree(ratioList,factorList)
# Compute parameters for pathway mixing tree
dicMix = dict()
dicReagents = dict()
waste = PWT.computeParameters(root,dicMix,dicReagents)
print('Reagents: ' + str(dicReagents) + '\n' + 'Mix: ' + str(dicMix) + '\n'+ 'Waste: ' + str(waste))
#-----------------------------------------------------------
PWT.tree2dot(root,'PMA.dot')
# Create skeleton Tree and add attributes (level,index,height) and mixerLen
G = PWT.createSkeletonTree(root)
PWT.putIndexInSkeletonTree(G)
PWT.putHeightInSkeletonTree(G)
PWT.printTreeAfterAdding_lih(G,"skeletonTreeAfterAdding_lih.dot")
#----------------------------------------------------------

#addExtraEdgesForEnhancedMixing(G)
annotatePathWayTree(G,ratioList)
#PWT.printTreeAfterAdding_lih(G,"skeletonTreeAfterAddingExtraEdges.dot")
opFile = open('clausesNewModeling.py','w')
initOPT(opFile)
addvariables(G,opFile)
ratioConsistencyConstraintsWithLinerarization(G,opFile,factorList,ratioList)

mixerConsistencyConstraints(G,opFile)
nonNegativityConstraints(G,opFile)
storageConstraint(G, opFile, k)
setTarget(G,opFile,ratioList)
#preserveMixingTreeHeight(G,opFile)
finishOPT(G,opFile)
# Run 'clauses.py'
subprocess.call(["python","clausesNewModeling.py"])
annotateMixingTreeWithValue(G,'op')
printTreeAfterAnnotation(G,'skeletonTreeAfterAnnotation.dot')

