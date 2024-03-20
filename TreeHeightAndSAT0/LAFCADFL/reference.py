import LAFCA
import DFL
import itertools

blockagesPos = []
v = -1


def demo(loadingCells):
    for element in itertools.product(*loadingCells):
        print(element)



def goAndFind(ind, blockageSpecificCells, cells, p):
    '''
        Finds the list of cells that have maximum adjacent cell connection
    '''
    if ind == len(blockageSpecificCells):
        global v
        if p> v:
            v = p
            global blockagesPos
            blockagesPos = cells
        return
    
    dir = [-1, 0, 1, 0, -1]
    for c in blockageSpecificCells[ind]:
        cells.append(c)
        t = p
        for i in range(4):
            x, y = c[0]+dir[i], c[1]+dir[i+1]
            if [x, y] in cells:
                t+=1

        goAndFind(ind+1, blockageSpecificCells, cells[:], t)
        cells.pop()


def getPlacementAndLoading(loadingCells, blockageCoordinates, reagentList):
    '''
        Intermediate fluids are considered as blockages
    '''
    row, col = 15, 15
    grid = []
    # Make the grid
    for _ in range(row):
        grid.append(['*']*col)

    # Make all the blockings adjacent
    '''
        Structure of blockageList is:
        blockageList = [
                    ["M2"],
                    ["M3", "M4"],
                    [],
        ]
    '''
    blockageList = []
    for i, reagents in enumerate(reagentList):
        blockages = []
        for reagent in reagents:
            if reagent[0] != 'R':
                blockages.append(reagent)
        for blockage in blockages:
            reagents.remove(blockage)
        blockageList.append(blockages)


    # Remove all the blockages that only have one position
    blockageSpecificCells = [] # contains blockage cells
    blockageOrder = [] # contains blockage order and the mixture index
    for i, blockages in enumerate(blockageList):
        for blockage in blockages:
            if len(blockageCoordinates[i][blockage]) == 1:
                # Place the blockage in the corrosponding cell and remove the cell from loading cell and blockageList
                cell = blockageCoordinates[i][blockage][0]
                grid[cell[0]][cell[1]] = blockage

                loadingCells[i].remove(cell)
            
            else:
                blockageSpecificCells.append(blockageCoordinates[i][blockage])
                blockageOrder.append([blockage, i]) 


    goAndFind(0, blockageSpecificCells, [], 0)

    for i, cell in enumerate(blockagesPos):
        grid[cell[0]][cell[1]] = blockageOrder[i][0]
        loadingCells[blockageOrder[i][1]].remove(cell)

    # All the cells that need to load
    cellsToLoad = []
    for mixture in loadingCells:
        for cell in mixture:
            cellsToLoad.append(cell)

    # List of all the reagents
    allReagents = []
    for i in range(len(reagentList)):
        for reagent in reagentList[i]:
            allReagents.append(reagent)

    # Check wheather z3 call is necessary or not , i.e if only one cell is empty then no need or all reagents are same
    for i, mixture in enumerate(reagentList):
        reagents = set()
        for reagent in mixture:
            reagents.add(reagent)
        if len(reagents) <= 1:
            if len(reagents) == 1:
                for cell in loadingCells[i]:
                    grid[cell[0]][cell[1]] = mixture[0]
            reagentList.remove(mixture)
            loadingCells.remove(loadingCells[i])

    for mixture in loadingCells:
        if len(mixture) == 0:
            loadingCells.remove(mixture)

    # # Used LAFCA to place the reagents in each cell
    for i in range(len(loadingCells)):
        assignment = LAFCA.createFile(reagentList[i], loadingCells[i], 'z3File.py', 'output'+str(i)+'.txt')
        for reagent in assignment:
            for j in range(len(assignment[reagent])):
                # Updating the grid
                x = assignment[reagent][j][0]
                y = assignment[reagent][j][1]
                grid[x][y] = reagent

    for r in grid:
        print(r)
    print()

    # Need to make row and col as local variable that can be passed in DFL
    loadingPaths = DFL.DFL([0,9],[9,0],grid,allReagents,cellsToLoad)
    
    global v
    v = -1
    global blockagesPos
    blockagesPos = []

    return loadingPaths

def main():
    # Required cells that can be load in parallel
    loadingCells = [
        [[5,5],[5,6],[6,5],[6,6]],
    ]
    # Reagents in each mixtures
    reagentList = [
        ["M6", "M5", "M7", "M5"],
    ]
    getPlacementAndLoading(loadingCells, reagentList)


if __name__ == '__main__':
    main()