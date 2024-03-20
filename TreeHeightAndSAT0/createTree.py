from NTM import *

def createNode(rootList, x, W, ind):
    """
        Create a rootList from the list data of reagents in each level and sharing of intermediate
        fluid data.
    """
    if ind == len(x):
        return []
    rootList.append(W[ind])
    for i, k in enumerate(x[ind]):
        if k != 0:
            rootList+=[f'R{i+1}']*k
    children = []
    createNode(children, x, W, ind+1)
    if len(children) != 0:
        rootList.append(children)
    return rootList

def createRoot(fileName, depth, r):
    R = []
    x = []
    W = [4]*(depth)
    for _ in range(depth):
        R.append([0]*r)
        x.append([0]*r)

    with open(fileName, "r+") as fp:
        lines = fp.read().split('\n')
        for line in lines[:-1]:
            var, val = line.split('=')
            vars = var.split('_')
            if vars[0] == 'R':
                R[int(vars[1])-1][int(vars[2])-1] = int(val)
            elif vars[0] == 'x':
                x[int(vars[1])-1][int(vars[2])-1] = int(val)
            else:
                W[int(vars[1])-1] = int(val)

    rootList = []
    createNode(rootList, x, W, 0)
    # Creating list to tree that is already implemented in NTM library
    print(rootList)
    root = listToTree(rootList)
    return root

def createTree(fileName, outputFileName, depth, r):
    root = createRoot(fileName, depth, r)
    saveTree(root, f'./OutputTree/{outputFileName}.png')

def getDepth(z3file):
    depth = 1
    with open(z3file, 'r') as fp:
        line = fp.readline()
        while line:
            if line[0] == 'W':
                depth+=1
            line = fp.readline()
    
    return depth


if __name__ == "__main__":
    getDepth('z3outputFile')