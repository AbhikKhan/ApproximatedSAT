from .LAFCA import *
from .DFL import *
import itertools

maxDeg = -1
blockagePlacement = []
intermediateFluid = []

def dfs(cell, cells, placement, units, blockage, index, blockedPos, fluidPos):
    if units[index] == 0:
        if index+1 == len(cells):
            global maxDeg, blockagePlacement, intermediateFluid
            deg=0
            d = [-1, 0, 1, 0, -1]
            for [x, y] in blockedPos:
                for i in range(4):
                    if [x+d[i], y+d[i+1]] in blockedPos:
                        deg+=1
            deg = deg //2
            if maxDeg< deg:
                maxDeg=deg
                blockagePlacement = blockedPos[:]
                intermediateFluid = fluidPos[:]
            return
        dfs(cells[index+1], cells, placement, units, blockage, index+1, blockedPos, fluidPos)
    
    dir = [0, 0, -1, 0, 1, 0]
    for i in range(5):
        x, y = cell[0]+dir[i], cell[1]+dir[i+1]
        if ([x, y] in placement[index]) & ([x, y] not in blockedPos):
            blockedPos.append([x, y])
            units[index]-=1
            fluidPos.append(blockage[index])
            dfs([x, y], cells, placement, units, blockage, index, blockedPos, fluidPos)
            units[index]+=1
            fluidPos.pop()
            blockedPos.pop()

def findBlockages(loadingCells, units, blockages):
    for element in itertools.product(*loadingCells):
        dfs(element[0], element, loadingCells, units, blockages, 0, [], [])


def getPlacementAndLoading(Mixtures, parentMix, loadingCells, reagentList, blockageList, units, grid):
    '''
        Intermediate fluids are considered as blockages
    '''
    # Make all the blockings adjacent
    '''
        Structure of blockageList is:
        blockageList["M1"] = {"M4": {"M1": [[1,2], [1,3], [2,2]], "M2": [[2,2]]} },
                    {"M5": {"M3": [[2,4]]} },
                    {"M6": {}
        }
        units["M4"] = [
            {"M1":2, "M2":1},
            {"M3":1},
            {},
        ]
    '''
    # If the intermediate fluid required and allocated space is equal then there's no choice but put
    # the intermediate fluids in that allocated space only.
    for _ in range(0, 2):
        for mixture in loadingCells:
            removeMix = []
            for mix in blockageList[mixture]:
                if units[mixture][mix] == len(blockageList[mixture][mix]):
                    removeMix.append(mix)
                    for x, y in blockageList[mixture][mix]:
                        # Fix the intermediate cell pos in grid and remove it from loading cells
                        grid[x][y] = mix
                        loadingCells[mixture].remove([x, y])
                        # remove [x, y] in other blockages also
                        for mix1 in blockageList[mixture]:
                            if (mix != mix1) & ([x, y] in blockageList[mixture][mix1]):
                                blockageList[mixture][mix1].remove([x, y])
            for mix in removeMix:
                del blockageList[mixture][mix]
                del units[mixture][mix]

    # Generate all possible combination and choose best out of it
    ind = 0
    parent = dict()
    blockageLoad = []
    blockageUnits = []
    blockageNames = []
    for mix in blockageList:
        ind+=1
        for child in blockageList[mix]:
            parent[child] = mix 
            blockageLoad.append(blockageList[mix][child][:])
            blockageUnits.append(units[mix][child])
            blockageNames.append(child)

    global maxDeg, blockagePlacement, intermediateFluid
    if len(blockageNames)> 0:
        findBlockages(blockageLoad, blockageUnits, blockageNames)
        print(blockagePlacement)
        print(intermediateFluid)

    for i in range(len(blockagePlacement)):
        loadingCells[parent[intermediateFluid[i]]].remove(blockagePlacement[i])
        grid[blockagePlacement[i][0]][blockagePlacement[i][1]] = intermediateFluid[i]

    maxDeg = -1
    blockagePlacement = []
    intermediateFluid = []

    # All the cells that need to load
    cellsToLoad = []
    for mixture in loadingCells:
        for cell in loadingCells[mixture]:
            cellsToLoad.append(cell)

    # List of all the reagents
    allReagents = []
    for mix in reagentList:
        for reagent in reagentList[mix]:
            allReagents.append(reagent)

    # Check wheather z3 call is necessary or not , i.e if only one cell is empty then no need 
    # or all reagents are same
    toDel = []
    for mixture in reagentList:
        reagents = set()
        for reagent in reagentList[mixture]:
            reagents.add(reagent)
        if len(reagents) <= 1:
            if len(reagents) == 1:
                for cell in loadingCells[mixture]:
                    grid[cell[0]][cell[1]] = reagentList[mixture][0]
            toDel.append(mixture)
    
    for mixture in toDel:
        del reagentList[mixture]
        del loadingCells[mixture]

    toDel = []
    for mixture in loadingCells:
        if len(loadingCells[mixture]) == 0:
            toDel.append(mixture)
    
    for mix in toDel:
        del loadingCells[mixture]

    # Used LAFCA to place the reagents in each cell
    i = 0
    for mix in loadingCells:
        assignment = createFile(reagentList[mix], loadingCells[mix], 'z3File.py', 'output'+str(i)+'.txt')
        i += 1
        for reagent in assignment:
            for j in range(len(assignment[reagent])):
                # Updating the grid
                x = assignment[reagent][j][0]
                y = assignment[reagent][j][1]
                grid[x][y] = reagent

    for r in grid:
        print(r)
    print()
    print(Mixtures)
    # Need to make row and col as local variable that can be passed in DFL
    loadingPaths = DFL([0,9],[9,0],grid,allReagents,cellsToLoad)
    for mix in Mixtures:
        for x, y in Mixtures[mix]:
            if [x, y] in parentMix[mix]:
                grid[x][y] = mix

    for r in grid:
        print(r)
    print()

    global v
    v = -1

    return loadingPaths
