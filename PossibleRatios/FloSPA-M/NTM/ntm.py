from copy import deepcopy
from .tree import *

def getCoordinates(quadrant, coordinate, rotation=None):
    if rotation is None:
        rotation = 'clockwise'
        
    x, y = coordinate
    if rotation == 'clockwise':
        if(quadrant == 0):
            coordinate1 = [ x+0, y+0 ]
            coordinate2 = [ x+0, y-1 ]
            coordinate3 = [ x-1, y-1 ]
            coordinate4 = [ x-1, y+0 ]
        elif(quadrant == 1):
            coordinate1 = [ x , y ]
            coordinate2 = [ x , y+1 ]
            coordinate3 = [ x+1 , y ]
            coordinate4 = [ x+1 , y+1 ]
        elif(quadrant == 2):
            coordinate1 = [ x , y ]
            coordinate2 = [ x-1 , y ]
            coordinate3 = [ x , y+1 ]
            coordinate4 = [ x-1 , y+1 ]
        elif(quadrant == 3):
            coordinate1 = [ x , y ]
            coordinate2 = [ x , y-1 ]
            coordinate3 = [ x-1 , y ]
            coordinate4 = [ x-1 , y-1 ]
        elif(quadrant == 4):
            coordinate1 = [ x , y ]
            coordinate2 = [ x+1 , y ]
            coordinate3 = [ x , y-1 ]
            coordinate4 = [ x+1 , y-1 ]
    elif rotation == 'anticlockwise':
        if(quadrant == 0):
            coordinate1 = [ x+0, y+0 ]
            coordinate2 = [ x-1, y+0 ]
            coordinate3 = [ x-1, y-1 ]
            coordinate4 = [ x+0, y-1 ]
        elif(quadrant == 1):
            coordinate1 = [ x , y ]
            coordinate2 = [ x+1 , y ]
            coordinate3 = [ x , y+1 ]
            coordinate4 = [ x+1 , y+1 ]
        elif(quadrant == 2):
            coordinate1 = [ x , y ]
            coordinate2 = [ x , y+1 ]
            coordinate3 = [ x-1 , y ]
            coordinate4 = [ x-1 , y+1 ]
        elif(quadrant == 3):
            coordinate1 = [ x , y ]
            coordinate2 = [ x-1 , y ]
            coordinate3 = [ x , y-1 ]
            coordinate4 = [ x-1 , y-1 ]
        elif(quadrant == 4):
            coordinate1 = [ x , y ]
            coordinate2 = [ x , y-1 ]
            coordinate3 = [ x+1 , y ]
            coordinate4 = [ x+1 , y-1 ]
            
    return [coordinate1, coordinate2, coordinate3, coordinate4]


def place360(node, coordinate, t):
    global PlacementInfo
    coordinate1, coordinate2, coordinate3, coordinate4 = getCoordinates(0, coordinate)
    
    vols = [child.volume for child in node.children if child.children != []]
    reags = [child for child in node.children if child.children == []]
    
    t1 = deepcopy(t)
    t2 = deepcopy(t)
    t3 = deepcopy(t)
    t4 = deepcopy(t)
        
    if len(vols) == 4:
        place90(1, node.children[0], coordinate1, t1)
        place90(4, node.children[1], coordinate2, t2)
        place90(3, node.children[2], coordinate3, t3)
        place90(2, node.children[3], coordinate4, t4)
        #no-reagent
        
    elif len(vols) == 3:
        place180(2, node.children[0], coordinate1, t1)
        place90(4, node.children[1], coordinate2, t2)
        place90(3, node.children[2], coordinate3, t3)
        # place reagent on coordinate2
        timeStamp = max(t1[0], t2[0], t3[0])
        coordinateList = [coordinate4]
        for idx, child in enumerate(reags):
            PlacementInfo.append([child.value, timeStamp, coordinateList[len(reags)-1-idx]])
        
    elif len(vols) == 2:
        if node.children[0].volume == 3:
            place360(node.children[0], coordinate1, t1)
            place90(2, node.children[1], coordinate4, t1)
            #no-reagent
        else:
            place180(2, node.children[0], coordinate1, t1)
            place180(4, node.children[1], coordinate3, t2)
            # place reagent  on coordinate4 ,2 
            timeStamp = max(t1[0] , t2[0])
            coordinateList = [coordinate2, coordinate4]
            for idx, child in enumerate(reags):
                PlacementInfo.append([child.value, timeStamp, coordinateList[len(reags)-1-idx]])
        
    elif len(vols) == 1:
        place360(node.children[0], coordinate1, t1)
        # place reagent  on coordinate2 ,3,4 
        timeStamp = t1[0]
        coordinateList = [coordinate4, coordinate3, coordinate2]
        for idx, child in enumerate(reags):
            PlacementInfo.append([child.value, timeStamp, coordinateList[len(reags)-1-idx]])
        
    elif len(vols) == 0:
        # place reagent  on coordinate1,2,3,4 
        timeStamp = t[0]
        coordinateList = [coordinate4, coordinate3, coordinate2, coordinate1]
        for idx, child in enumerate(reags):
            PlacementInfo.append([child.value, timeStamp, coordinateList[len(reags)-1-idx]])

    #mix 
    #wash as per vol
    mixModuleId = node.value
    timeStamp = max(t1[0], t2[0], t3[0],t4[0])
    mixSequence = [coordinate1, coordinate2, coordinate3, coordinate4]
    
    washSequence = []
    if node.volume == 0:
        print ("WARNING: You are washing whole mixer i.e. remaining volume = 0 units.")
        washSequence = [coordinate4, coordinate3, coordinate2, coordinate1]
    if node.volume == 1:
        washSequence = [coordinate4, coordinate3, coordinate2]
    elif node.volume == 2:
        washSequence = [coordinate4, coordinate3]
    elif node.volume == 3:
        washSequence = [coordinate4]
        
    PlacementInfo.append([mixModuleId, timeStamp, mixSequence, washSequence])
    
    t[0] = timeStamp + 1
    
    return PlacementInfo


#######Start

def place180(quadrant, node, coordinate, t, rotation=None):
    global PlacementInfo
    coordinate1, coordinate2, coordinate3, coordinate4 = getCoordinates(quadrant, coordinate)
    
    vols = [child.volume for child in node.children if child.children != []]
    reags = [child for child in node.children if child.children == []]
    
    t1 = deepcopy(t)
    t2 = deepcopy(t)
        
    if len(vols) == 4:
        place90(quadrant-1 if quadrant > 1 else 4  , node.children[0], coordinate1, t1)
        place90(quadrant, node.children[1], coordinate2, t2)
        place90(quadrant-1 if quadrant > 1 else 4, node.children[2], coordinate3, t1)
        place90(quadrant, node.children[3], coordinate4, t2)
        #no-reagent
        
    elif len(vols) == 3:
        place90(quadrant-1 if quadrant > 1 else 4, node.children[0], coordinate1, t1)
        place90(quadrant, node.children[1], coordinate2, t2)
        place90(quadrant, node.children[2], coordinate4, t2)
        # place reagent on coordinate3
        timeStamp = max(t1[0], t2[0])
        coordinateList = [coordinate3]
        for idx, child in enumerate(reags):
            PlacementInfo.append([child.value, timeStamp, coordinateList[len(reags)-1-idx]])
        
    elif len(vols) == 2:
        if node.children[0].volume == 3:
            place180(quadrant, node.children[0], coordinate1, t1)
            place90(quadrant, node.children[1], coordinate4, t1)
            #no-reagent
        else:
            place90(quadrant-1 if quadrant > 1 else 4, node.children[0], coordinate1, t1)
            place90(quadrant, node.children[1], coordinate2, t2, 'anticlockwise')
            # place reagent  on coordinate4 ,3
            timeStamp = max(t1[0] , t2[0])
            coordinateList = [coordinate4, coordinate3]
            for idx, child in enumerate(reags):
                PlacementInfo.append([child.value, timeStamp, coordinateList[len(reags)-1-idx]])
        
    elif len(vols) == 1:
        place180(quadrant, node.children[0], coordinate1, t1)
        # place reagent  on coordinate2 ,3,4 
        timeStamp = t1[0]
        coordinateList = [coordinate4, coordinate3, coordinate2]
        for idx, child in enumerate(reags):
            PlacementInfo.append([child.value, timeStamp, coordinateList[len(reags)-1-idx]])
        
    elif len(vols) == 0:
        # place reagent  on coordinate1,2,3,4 
        timeStamp = t[0]
        coordinateList = [coordinate4, coordinate3, coordinate2, coordinate1]
        for idx, child in enumerate(reags):
            PlacementInfo.append([child.value, timeStamp, coordinateList[len(reags)-1-idx]])

    #mix 
    #wash as per vol
    mixModuleId = node.value
    timeStamp = max(t1[0], t2[0])
    mixSequence = [coordinate1, coordinate2, coordinate4, coordinate3]
    
    if node.volume == 0:
        print ("WARNING: You are washing whole mixer i.e. remaining volume = 0 units.")
        washSequence = [coordinate4, coordinate3, coordinate2, coordinate1]
    if node.volume == 1:
        washSequence = [coordinate4, coordinate3, coordinate2]
    elif node.volume == 2:
        washSequence = [coordinate4, coordinate3]
    elif node.volume == 3:
        washSequence = [coordinate4]
        
    PlacementInfo.append([mixModuleId, timeStamp, mixSequence, washSequence])
    
    t[0] = timeStamp + 1
######    

def place90(quadrant, node, coordinate, t, rotation=None):
    global PlacementInfo
    coords = getCoordinates(quadrant, coordinate, rotation)
    
    vols = [child.volume for child in node.children if child.children != []]
    reags = [child for child in node.children if child.children == []]
    
    
    if len(vols) == 4:
        place90(quadrant, node.children[0], coords[0], t)
        place90(quadrant, node.children[1], coords[1], t)
        place90(quadrant, node.children[2], coords[2], t)
        place90(quadrant, node.children[3], coords[3], t)
        #no-reagent
    
    elif len(vols) == 3:
        place90(quadrant, node.children[0], coords[0], t)
        nextPos = 0+node.children[0].volume
        place90(quadrant, node.children[1], coords[nextPos], t)
        nextPos += node.children[1].volume
        place90(quadrant, node.children[2], coords[nextPos], t)
        # place reagent on coordinate2
        timeStamp = t[0]
        coordinateList = [coords[3]]
        for idx, child in enumerate(reags):
            PlacementInfo.append([child.value, timeStamp, coordinateList[len(reags)-1-idx]])
    
    elif len(vols) == 2:
        place90(quadrant, node.children[0], coords[0], t)
        nextPos = 0+node.children[0].volume
        place90(quadrant, node.children[1], coords[nextPos], t)
        # place reagent on coordinate3,4
        timeStamp = t[0]
        coordinateList = [coords[3], coords[2]]
        for idx, child in enumerate(reags):
            PlacementInfo.append([child.value, timeStamp, coordinateList[len(reags)-1-idx]])
    
    elif len(vols) == 1:
        place90(quadrant, node.children[0], coords[0], t)
        # place reagent on coordinate2,3,4
        timeStamp = t[0]
        coordinateList = [coords[3], coords[2], coords[1]]
        for idx, child in enumerate(reags):
            PlacementInfo.append([child.value, timeStamp, coordinateList[len(reags)-1-idx]])
    
    elif len(vols) == 0:
        # place reagent  on coordinate1,2,3,4 
        timeStamp = t[0]
        coordinateList = [coords[3], coords[2], coords[1], coords[0]]
        for idx, child in enumerate(reags):
            PlacementInfo.append([child.value, timeStamp, coordinateList[len(reags)-1-idx]])
        
#     print( coordinate , ':' , t ,':' , node.value, ':wash:', [coordinate2, coordinate4, coordinate3])
    mixModuleId = node.value
    timeStamp = t[0]
    mixSequence = [coords[0], coords[1], coords[3], coords[2]]
    
    if node.volume == 0:
        print ("WARNING: You are washing whole mixer i.e. remaining volume = 0 units.")
        washSequence = [coords[3], coords[2], coords[1], coords[0]]
    if node.volume == 1:
        washSequence = [coords[3], coords[2], coords[1]]
    elif node.volume == 2:
        washSequence = [coords[3], coords[2]]
    elif node.volume == 3:
        washSequence = [coords[3]]
        
    PlacementInfo.append([mixModuleId, timeStamp, mixSequence, washSequence])
    
    t[0] += 1
    
    return

PlacementInfo = []
def ntm(node, coordinate=[0,0], t=None):
    '''
        Returns coordinates of each module and wash coordinates.
    '''
    if t is None:
        t = [1]

    global PlacementInfo
    PlacementInfo = []
    #Converts given tree to left-factored tree before placement 
    leftFactoredTree = leftistTree(node)
    place360(leftFactoredTree, coordinate, t)
    return PlacementInfo
