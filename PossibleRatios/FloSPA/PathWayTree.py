import networkx as nx
from collections import deque
from numpy import product
__ID = 1        # Unique ID for each node in the pathway tree


def createRemainderTable(inputRatio, primeFactors):
    ''' Creates remainder table'''
    # Check for input consistency
    if sum(inputRatio) != product(primeFactors):
        print('createRemainderTable: Invalid input')
        return None
    
    remainderTable = []     # List of remainders for each prime factors
    ipRatio = inputRatio[:]     # Copy input ratio
    # Create remainder list for each prime factors
    for f in range(len(primeFactors)):
        remainderList = []
        for i in range(len(ipRatio)):
            remainderList.append(ipRatio[i] % primeFactors[f])
            ipRatio[i] = ipRatio[i] / primeFactors[f]
        # Insert remainder list into a table
        remainderTable.append(remainderList[:])
    
    return remainderTable

class treeNode(object):
    def __init__(self):
        self.parentPtr = None           # Pointer to parent node. If root parent = None
        self.pathWayLen = 0             # For input droplets pathWayLen = 0
        self.reagentId = 0              # reagentId = 0 for intermediate node 
        self.dropletCount = 0           # No. of droplet
        self.childPtrList = []          # Pointer list for children 
        self.id = None

def createPathWayMixingTree(inputRatio, primeFactors):
    global __ID
    remainderTable = createRemainderTable(inputRatio, primeFactors)
    ptrList = []                        # Stores the pointers of the subtrees of each level
    for f in range(len(primeFactors)):
        factor = primeFactors[f]
        tmpPtrList = []                 # Stores the pointers of the intermediate subtrees 
        remainderList = remainderTable[f][:]
        
        #------------------------------------------------------------------
        count = sum(remainderList) // factor 
        while count > 0:
            intermediateNode = treeNode()
            intermediateNode.pathWayLen = factor
            intermediateNode.dropletCount = factor
            intermediateNode.id = __ID
            __ID = __ID + 1
            # Create subtree
            dropletCount = 0
            for i in range(len(remainderList)):
                if remainderList[i] > 0:
                    if (dropletCount + remainderList[i]) < factor:
                        # Create a leaf node
                        leafNode = treeNode()
                        leafNode.parentPtr = intermediateNode
                        leafNode.reagentId = i+1
                        leafNode.dropletCount = remainderList[i]
                        leafNode.id = __ID
                        __ID = __ID + 1
                        # Add leaf to intermediate Node
                        intermediateNode.childPtrList.append(leafNode)
                        
                        dropletCount = dropletCount + remainderList[i]
                        remainderList[i] = 0
                    elif (dropletCount + remainderList[i]) == factor:
                        # Create a leaf node
                        leafNode = treeNode()
                        leafNode.parentPtr = intermediateNode
                        leafNode.reagentId = i+1
                        leafNode.dropletCount = remainderList[i]
                        leafNode.id = __ID
                        __ID = __ID + 1
                        # Add leaf to intermediate Node
                        intermediateNode.childPtrList.append(leafNode)
                        
                        dropletCount = dropletCount + remainderList[i]
                        remainderList[i] = 0
                        break
                    elif (dropletCount + remainderList[i]) > factor:
                        # Create a leaf node
                        leafNode = treeNode()
                        leafNode.parentPtr = intermediateNode
                        leafNode.reagentId = i+1
                        leafNode.dropletCount = factor - dropletCount
                        leafNode.id = __ID
                        __ID = __ID + 1
                        # Add leaf to intermediate Node
                        intermediateNode.childPtrList.append(leafNode)
                        
                        remainderList[i] = remainderList[i] - (factor - dropletCount)
                        dropletCount = factor
                        break
                    else:
                        pass
            # Insert subtree for processing next prime factor
            tmpPtrList.append(intermediateNode)
            count = count - 1
        #------------------------------------------------------------------
            
        # Process remaining remainders and subtrees from previous prime factor
        n = len(ptrList) + sum(remainderList)   # len(ptrList) = no. of subtree from lower level
            
        #----------------------------------------------------------------------
        if n % factor != 0:
                print('createMixingTree: !!!!!!!!!!!!!!!!!!!!')
        #----------------------------------------------------------------------
            
            
            
        #------------------------------------------------------------------
        count = n // factor
        while count > 0:
            intermediateNode = treeNode()
            intermediateNode.pathWayLen = factor
            intermediateNode.dropletCount = factor
            intermediateNode.id = __ID
            __ID = __ID + 1
            dropletCount = 0
            # Create subtree
            while sum(remainderList) != 0:
                # Find the non-zero remainder
                for i in range(len(remainderList)):
                    if remainderList[i] != 0:
                        break
                leafNode = treeNode()
                leafNode.parentPtr = intermediateNode
                leafNode.reagentId = i+1
                leafNode.dropletCount = remainderList[i]
                leafNode.id = __ID
                __ID = __ID + 1
                # Add leaf to intermediate Node
                intermediateNode.childPtrList.append(leafNode)
                        
                dropletCount = dropletCount + remainderList[i]
                remainderList[i] = 0
                
            while dropletCount != factor:
                nodePtr = ptrList.pop()
                nodePtr.parentPtr = intermediateNode
                intermediateNode.childPtrList.append(nodePtr)
                dropletCount = dropletCount + 1
                    
            # Insert subtree for processing next prime factor
            tmpPtrList.append(intermediateNode)
            count = count - 1
        #------------------------------------------------------------------ 
        
        ptrList = tmpPtrList[:]
        
    # print('createMixingTree: len(ptrList)=%d' % len(ptrList))
    return ptrList[0]   

#-----------------------------Generates dot file for dilution forest--------------------
def dotedge(root,fp):
    if root != None:
        if root.reagentId != 0:
            fp.write(str(root.id)+' [shape = \"box\",label = "R%d\\n  id = %d"];\n'\
                                %(root.reagentId,root.id))
        else:
            fp.write(str(root.id)+' [ label = "len = %d\\n id = %d"];\n'\
                                %(root.pathWayLen,root.id))
            
        for child in root.childPtrList:
            if root.reagentId == 0 and child.reagentId == 0:    #only one unit shared
                fp.write(str(root.id)+' -- '+str(child.id)+'[label = 1]\n')
            else:
                fp.write(str(root.id)+' -- '+str(child.id)+'[label = %d]\n'%child.dropletCount)
            
        for child in root.childPtrList:
            dotedge(child,fp)


def tree2dot(root,filename):
    fp = open(filename,'w')
    string = 'graph "DD" { \n' 
    fp.write(string)
    dotedge(root,fp)
    fp.write('}\n') 
    fp.close()
    
#-----------------------------Parameter calculations------------------------------------
def computeParameters(root,dicMix,dicReagents):   # waste must be initialised to 0
    waste = 0
    if root!= None:
        if root.pathWayLen != 0:        # Intermediate node
            # Calculate mixing
            if root.pathWayLen not in dicMix:
                dicMix[root.pathWayLen] = 1
            else:
                dicMix[root.pathWayLen] = dicMix[root.pathWayLen] + 1
        # Calculate Waste
        if root.parentPtr == None:
            waste = waste + root.pathWayLen - 1
        elif root.pathWayLen != 0:
            waste = waste + root.pathWayLen - 1
        # Calculate reagent consumption
        if root.reagentId != 0:
            if root.reagentId not in dicReagents:
                dicReagents[root.reagentId] = root.dropletCount
            else:
                dicReagents[root.reagentId] = dicReagents[root.reagentId] + root.dropletCount
                
        for child in root.childPtrList:
            waste = waste + computeParameters(child,dicMix,dicReagents)        
        
        return waste  
    

#----------------------Special processing for optimization--------------------------    
def createSkeletonTree(root):
    # Takes mixing tree and returns a Networkx graph having only mixing nodes
    # Each node has level and mixerSize attribute 
    __id = 1
    Q = deque([(root,1,__id)])   # (pointer,level,id)
    G = nx.DiGraph()
    G.add_node(__id, level = 1, mixerSize = root.pathWayLen)   #Add root node at level 1
    __id = __id + 1
    while len(Q) > 0:
        (currNodePtr,l,nodeId,) = Q.popleft()
        for childPtr in currNodePtr.childPtrList:
            if childPtr.pathWayLen != 0:
                G.add_node(__id, level = l + 1, mixerSize = childPtr.pathWayLen)
                G.add_edge(nodeId,__id)
                Q.append((childPtr,l+1,__id))
                __id = __id + 1
    return G

def createSkeletonTreeNew(root):
    # Takes mixing tree and returns a Networkx graph having only mixing nodes
    # Each node has level and mixerSize attribute 
    __id = 1
    Q = deque([(root,1,__id)])   # (pointer,level,id)
    G = nx.DiGraph()
    G.add_node(__id, level = 1, mixerSize = 4)   #Add root node at level 1
    __id = __id + 1
    while len(Q) > 0:
        (node,l,nodeId,) = Q.popleft()
        for child in node.children:
            if child.children != []:
                G.add_node(__id, level = l + 1, mixerSize = 4)
                G.add_edge(nodeId,__id)
                Q.append((child,l+1,__id))
                __id = __id + 1
    return G

def putIndexInSkeletonTree(G):
    #Put index value in each node as an attribute
    indexDict = dict()
    for v in G.nodes():
        if G.nodes[v]['level'] in indexDict:
            indexDict[G.nodes[v]['level']] = indexDict[G.nodes[v]['level']] + 1   #Increment existing index value
            index = indexDict[G.nodes[v]['level']]
            G.nodes[v]['index'] = index
        else:
            index = 1
            G.nodes[v]['index'] = index
            indexDict[G.nodes[v]['level']] = index   #Add new entry in hash table for new level

def height(G,v):
    # Calculate the height of the node v in G
    # Leaf node has height 0
    if len(G.out_edges(v)) == 0:    #leaf node
        return 1
    else:
        maximum = -5000
        for (_,y) in G.out_edges(v):
            h = height(G,y)
            if h > maximum:
                maximum = h
        return 1+maximum
                
def putHeightInSkeletonTree(G):
    # Put height in each node as an attribute. Leaf node has height 0
    for v in G.nodes():
        G.nodes[v]['height'] = height(G,v)


def printTreeAfterAdding_lih(G,filename):
    fp = open(filename,'w')
    string = 'digraph "DD" { \n' + "graph [ ordering = \"out\"];\n" 
    fp.write(string)
    for v in G.nodes():
        fp.write(str(v) + " " + "[label = \"id = %d\\n mixerLen = %d \\n (l,i,h) = (%d,%d,%d)\"] \n"\
                 %(v,G.nodes[v]['mixerSize'],G.nodes[v]['level'],G.nodes[v]['index'],G.nodes[v]['height']))
    for e in G.edges():
        fp.write(str(e[0]) + " -> " + str(e[1]) + ";\n" )
    fp.write('}\n') 
    fp.close()