import itertools
maxDeg = 0
blockageList = []
intermediateFluid = []
def dfs(cell, cells, placement, units, blockage, index, blockedPos, fluidPos):
    if units[index] == 0:
        if index+1 == len(cells):
            global maxDeg, blockageList, intermediateFluid
            deg=0
            d = [-1, 0, 1, 0, -1]
            for [x, y] in blockedPos:
                for i in range(4):
                    if [x+d[i], y+d[i+1]] in blockedPos:
                        deg+=1
            deg = deg //2
            if maxDeg< deg:
                maxDeg=deg
                blockageList = blockedPos[:]
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

def demo(loadingCells, units, blockages):
    for element in itertools.product(*loadingCells):
        dfs(element[0], element, loadingCells, units, blockages, 0, [], [])

if __name__ == "__main__":
    placement = [
        [[1, 2], [1, 3], [2, 2]],
        [[1, 4], [1, 5], [2, 4], [2, 5]],
        [[3, 2], [3, 3]],
    ]
    units = [2, 1, 1]
    blockages = ['m1', 'm2', 'm3']
    demo(placement, units, blockages)
    print(blockageList)
    print(intermediateFluid)