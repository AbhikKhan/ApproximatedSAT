from NTM import *

def createRoot(rootList, x, W, ind):
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
    createRoot(children, x, W, ind+1)
    if len(children) != 0:
        rootList.append(children)
    return rootList

def createTree(fileName, outputFileName, depth, N):
    R = []
    x = []
    W = [4]*(depth-1)
    for _ in range(depth-1):
        R.append([0]*N)
        x.append([0]*N)

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
    print(R)
    print(x)
    print(W)

    rootList = []
    createRoot(rootList, x, W, 0)
    # Creating list to tree that is already implemented in NTM library
    root = listToTree(rootList)

    saveTree(root, f'./OutputTree/{outputFileName}.png')


if __name__ == "__main__":
    createTree('z3outputFile1', 'OutputTree1', 4, 4)