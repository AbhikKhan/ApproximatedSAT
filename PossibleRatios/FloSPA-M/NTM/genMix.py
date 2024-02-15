from math import log
from random import shuffle
import random
from .tree import *

def convert(value, base):
    add = value % base
    if value <= 1:
        return str(value)
    else:
        return str(convert(value//base,base)) + str(add)

   
def genMixHelper(bins, power, N):
    global COUNTER_MIX
    temp_node = node('M{}'.format(COUNTER_MIX))
    if not len(bins[power]):
        COUNTER_MIX += 1
        for i in range(N):
            temp_node.children.append(genMixHelper(bins, power-1, N))
    else:
        temp_node.value = bins[power].pop()
    return temp_node

COUNTER_MIX = None     
def genMix(mixture, N):
    global COUNTER_MIX
    COUNTER_MIX = 1
    depth = int(log(sum([p for (s, p) in mixture]),N))
    bins = []
    for i in range(depth+1):
        bins.append([])
    
    for (s,p) in mixture:
        baseN = convert(p, N)[::-1]
        for j in range(len(baseN)):
            for i in range(int(baseN[j])):
                bins[j].append(s)
    
    return genMixHelper(bins, depth, N)
