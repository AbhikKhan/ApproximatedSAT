
def createList(W, reagents, level, childID, weight, tree):
    print(level, childID)
    child = [weight]
    for r in reagents[level][childID]:
        child += [f'r{r}']*reagents[level][childID][r]
    
    if level in W:
        if childID in W[level]:
            for level_to in W[level][childID]:
                for child_to in W[level][childID][level_to]:
                    createList(W, reagents, level_to, child_to, W[level][childID][level_to][child_to], child)
    tree.append(child)

    return tree

def createTree():
    file = "z3for5/1006max"
    W = dict()
    reagents = dict()
    with open(file, 'r') as fp:
        line = fp.readline()
        while line:
            line = line.split(' = ')
            vals = [int(val) for val in line[0].split('_')[1:]]
            weight = int(line[1])
            
            if line[0][0]=='w':
                # W_levelFrom_childFrom_levelTo_childeTo
                level_from, child_from, level_to, child_to = vals
                if level_to not in W:
                    W[level_to] = dict()
                if child_to not in W[level_to]:
                    W[level_to][child_to] = dict()
                if level_from not in W[level_to][child_to]:
                    W[level_to][child_to][level_from] = dict()
                if child_from not in W[level_to][child_to][level_from]:
                    W[level_to][child_to][level_from][child_from] = weight
            elif line[0][0]=='r':
                # r_level_child_reagents
                level, child, r = vals
                if level not in reagents:
                    reagents[level] = dict()
                if child not in reagents[level]:
                    reagents[level][child] = dict()
                if r not in reagents[level][child]:
                    reagents[level][child][r] = weight
            line = fp.readline()
    print(W)
    # print(reagents)
    root = createList(W, reagents, 1, 1, 4, [])       
    print(root)

if __name__ == "__main__":
    createTree()