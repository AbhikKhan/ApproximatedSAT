from NTM import *
from LAFCADFL import *

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

def getPlacementAndTimestamp(root):
    '''
        @param: list of the tree
        @output: Generate the tree from the list provided and returns KBL parameters
        Use NTM to get the placement of the tree and time stamp at which each mixture will execute
    '''
    output_assignment_set = ntm(root, [5, 5], [1]) # returns [moduleID, timeStamp, Binding, WashSequence] for every sequence

    # Get the corrospondence mixture reagents and intermediate fluids
    mixture = getMix(root)

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


if __name__ == "__main__":
    getPlacementAndLoading([4,[3, 'r1', 'r2', 'r2', 'r4'], 'r3'])