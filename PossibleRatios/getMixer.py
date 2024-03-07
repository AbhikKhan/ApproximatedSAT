import csv

def parseFile(fileName):
    mixer = 1
    try:
        with open(fileName, 'r') as fp:
            line = fp.readline()[:-1]
            while line:
                all = line.split(' = ')
                if all[0][0] == 'w' and all[1] != '0':
                    mixer+=1
                line = fp.readline()[:-1]
    except:
        print(f'{fileName} not exist')
    return mixer

if __name__ == "__main__":
    k = 3
    path = f"./z3for{k}/"
    opfile = f'mixer{k}.xls'
    for id in range(0, 2000):
        mixermin = parseFile(path+f'{id}min')
        mixermax = parseFile(path+f'{id}max')
        with open(opfile, 'a', newline='') as ofp:
            writer = csv.writer(ofp)
            values = [id,mixermin, mixermax]
            writer.writerow(values)