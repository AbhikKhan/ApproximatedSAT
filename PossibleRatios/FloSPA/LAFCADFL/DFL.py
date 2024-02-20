from collections import deque

row = 10
col = 10


def findStart(curr, grid, reagent, inlet):
    direction = [-1, 0, 1, 0, -1]
    queue = deque([[curr, [curr]], ]) #[[cell], [[path]]]

    while queue:
        left = queue.popleft()
        X, Y = left[0][0], left[0][1]
        path = left[1]

        grid[X][Y] = 'B'  # To represent a Blocked cell

        for i in range(4):
            nx, ny = X + direction[i], Y + direction[i + 1]
            if (0 <= nx < row) and (0 <= ny < col):
                if grid[nx][ny] == reagent:
                    return path + [[nx, ny]], 1  # Return the path to the cell with the reagent
                elif [nx, ny] == inlet:
                    return path + [[nx, ny]], 0  # Return the path to the inlet
                if grid[nx][ny] == '*':
                    queue.append([[nx, ny], path + [[nx, ny]]])

    return [], 0

def findLast(curr, grid, reagent, inlet):
    direction = [-1, 0, 1, 0, -1]
    queue = deque([[curr, 0, [curr]], ]) #[[cell], [[path]]]

    while queue:
        left = queue.popleft()
        X, Y = left[0][0], left[0][1]
        cR = left[1]
        path = left[2]

        grid[X][Y] = 'B'  # To represent a Blocked cell

        for i in range(4):
            nx, ny = X + direction[i], Y + direction[i + 1]
            if (0 <= nx < row) and (0 <= ny < col):
                if [nx, ny] == inlet:
                    return path + [[nx, ny]], 0  # Return the path to the inlet
                if grid[nx][ny] == '*':
                    queue.append([[nx, ny], cR, path + [[nx, ny]]])
                elif grid[nx][ny] == reagent:
                    queue.append([[nx, ny], cR+1, path + [[nx, ny]]])

    return [], 0

def bestFlow(grid, inlet, outlet, R):
    '''
        Find cellStart, a cell with reagent R which is closest to the outlet
    '''
    grid_copy = [r[:] for r in grid]

    path, rCount = findStart(outlet, grid_copy, R, inlet)
    if rCount == 0:
        return [], 0, 0

    cellWithReagents = []
    fromInOut = [path] # Act as stack to keep track of paths
    reagentCount = rCount

    while rCount != 0:
        for cell in fromInOut[-1]:
            grid[cell[0]][cell[1]] = 'B'
        cellWithReagents.append(fromInOut[-1][-1])

        grid_copy = [r[:] for r in grid]

        path, rCount = findStart(path[-1], grid_copy, R, inlet)

        # Need to make a change so that if the bfs stops we can backtrack the path is the current path have some reagent
        if (len(path) == 0) and (reagentCount != 0): # Implies BFS has stuck!!!!!!
            while(len(fromInOut)):
                lastPath = fromInOut[-1]
                grid_copy = [r[:] for r in grid]

                path, rCount = findLast(lastPath[-1], grid_copy, R, inlet)
                reagentCount += rCount
                if len(path) != 0: # We got a path from a cell with reagent to inlet
                    break

                fromInOut.pop()
                reagentCount -= 1
                
                for cell in lastPath:
                    if cell in cellWithReagents:
                        grid[cell[0]][cell[1]] = R
                    else:
                        grid[cell[0]][cell[1]] = '*'
    
        reagentCount += rCount
        fromInOut.append(path[:])

    finalPath = []

    for p in fromInOut:
        for cell in p[:-1]:
            grid[cell[0]][cell[1]] = '*'
            finalPath.append(cell)

    # Need to make the stack as a path
    finalPath.append(inlet)

    bendings = 0
    for i in range(2,len(finalPath)):
        if (finalPath[i][0] != finalPath[i-2][0]) and (finalPath[i][1] != finalPath[i-2][1]):
            bendings+=1

    return finalPath, reagentCount, bendings


def DFL(inlet, outlet, grid, reagents, loadingCells):
    loadingOrder = []
    
    while len(loadingCells) > 0:
        countR = 0 # to count number of reagents in the bestFlow path
        R = "" # reagent for which we get the bestFlow
        path = [] # bestFlow
        B = 40

        for reagent in reagents:
            grid_copy = [r[:] for r in grid]
            currPath, cR, cB = bestFlow(grid_copy, inlet, outlet, reagent)
            # Hardcoded values
            if (cR == 0) or (currPath[-2] != [0, 8] and currPath[-2] != [1, 9] and currPath[-2] != [0, 10]):
                continue
            if (countR < cR) or ((countR == cR) and (cB < B)) or ((countR == cR) and (cB == B) and (len(path) > len(currPath))):
                path = currPath[:]
                countR = cR
                R = reagent
                B = cB

        # We got the bestFlow for the current condition of the chip
        if len(path) == 0:
            break
        
        # for i in range(row):
        #     r = ""
        #     for j in range(col):
        #         if [i, j] in path:
        #             r += 'B '
        #         else:
        #             r += grid[i][j]+' '
        #     print(r)
        # print('-'*50)

        path.reverse()
        loadingOrder.append([R, B, path])
        # Make all the cells in the path non blocking, i.e '*'
        for cell in path:
            grid[cell[0]][cell[1]] = '*'
            if cell in loadingCells:
                loadingCells.remove(cell)

    loadingOrder.reverse()
    return loadingOrder


def main():
    grid = []
    for _ in range(row):
        grid.append(['*']*col)

    grid[4][4] = grid[4][5] = grid[5][4] = "R1"
    grid[5][5] = grid[6][6] = grid[6][7] = "R2"
    grid[6][4] = grid[6][5] = grid[7][4] = "R3"
    grid[7][5] = grid[7][6] = grid[7][7] = "R4"

    for r in grid:
        print(r)

    loadingCells = [
        [4,4],[4,5],[5,4],[5,5],
        [6,4],[6,5],[7,4],[7,5],
        [6,6],[6,7],[7,6],[7,7],
    ]
    reagents = ["R1", "R2", "R3", "R4"]
    inlet = [0,9]
    outlet = [9,0]
    
    loadingOrder = DFL(inlet, outlet, grid, reagents, loadingCells)
    loadingOrder.reverse()
    for order in loadingOrder:
        print(order[0], order[1])
        print(order[2])

 
if __name__ == "__main__":
    main()
