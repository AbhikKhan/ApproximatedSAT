from NTM import *
def createTree(fileName, depth, N):
    R = []
    x = []
    W = [0]*depth
    for _ in range(depth):
        R.append([0]*N)
        x.append([0]*N)

    with open(fileName, "r+") as fp:
        lines = fp.read().split('\n')
        for line in lines[:-1]:
            var, val = line.split('=')
            print(var, val)
            vars = var.split('_')
            if vars[0] == 'R':
                R[int(vars[1])-1][int(vars[2])-1] = int(val)
            elif vars[0] == 'x':
                x[int(vars[1])-1][int(vars[2])-1] = int(val)
            else:
                W[int(vars[1])-1] = int(val)


if __name__ == "__main__":
    createTree('z3outputFile', 4, 4)