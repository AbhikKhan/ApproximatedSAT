from copy import deepcopy
from .tree import *

def hda(root):
    mixList = []
    reagentList = []
    temp = [root]
    
    while len(temp) > 0:
        auxMix = []
        auxReagent = []
        for el in temp:
            for child in el.children:
                if(len(child.children) != 0): #mix node
                    auxMix.append(child)
                else : #reagent node
                    auxReagent.append(child)


        mixList.append(auxMix)
        reagentList.append(auxReagent)
        temp = auxMix

    mixList = [[item.value for item in x] for x in mixList]
    reagentList = [[item.value for item in x] for x in reagentList]
    
    MAX = 1
    for level in mixList:
        MAX = max(MAX, len(level))
    MAX = min(4, MAX)
    
    mix_counter = 0
    for idx, _ in enumerate(mixList[:-1]):
        while len(mixList[idx]) < MAX:
            if len(reagentList[idx]) > 0:
                temp = reagentList[idx].pop(0)
                reagentList[idx+1] += [temp, temp, temp, temp]
                mixList[idx].append('m{}'.format(mix_counter))
                mix_counter += 1
            else:
                print ("ERROR: no reagent found")
            
    newRoot = node(root.value)
    
    newMixList = []
    for idx, _ in enumerate(mixList):
        level = mixList[idx]+reagentList[idx]
        temp = [[] for i in range(MAX)]
        i = 0
        for mix in level:
            temp[i].append(node(mix))
            i = (i+1)%len(temp)
        newMixList.append(temp)
    
    for idx, _ in enumerate(newMixList):
        if idx == 0:
            for item in newMixList[idx]:
                for newItem in item:
                    newRoot.children.append(newItem)
        else:
            for jdx, item in enumerate(newMixList[idx]):
                for newItem in item:
                    if len(newMixList[idx-1][jdx][0].children) >= 4:
                        newMixList[idx-1][jdx].pop(0)
                    newMixList[idx-1][jdx][0].children.append(newItem)
        
    return newRoot
