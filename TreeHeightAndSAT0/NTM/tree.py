import random

class node(object):
    def __init__(self, value, vol=1, children = []):
        self.value = value
        self.volume = vol
        self.children = children or []
        self.hash = random.randint(1, 100000001)

    def __str__(self, level=0):
        ret = "\t"*level+repr(self.value)+"\n"
        for child in self.children:
            ret += child.__str__(level+1)
        return ret

    def __repr__(self):
        return '<{}>'.format(self.value)


######################################################################################
from copy import deepcopy

def leftistTree(node):
    nodeCopy = deepcopy(node)
    _leftistTree(nodeCopy)
    return nodeCopy

def _leftistTree(node):
#     node = deepcopy(nodeReal)
    if node.children == []:
        return
    reagentIdx = [idx for idx, child in enumerate(node.children) if child.children == []]
    vols = sorted([(idx, child.volume) for idx, child in enumerate(node.children) if child.children != []], key = lambda x: x[1], reverse = True)
    temp = []
    for item in vols:
        temp.append(node.children[item[0]])
    for item in reagentIdx:
        temp.append(node.children[item])
    node.children = temp
    
    for child in node.children:
        _leftistTree(child)
        
    return


######################################################################################
def isSkewed(root):
    '''
    check if a tree in NODE data structure is skewed or not
    '''
    if root is None:
        return True
    if len(root.children) == 0:
        return True
    else:
        next_root = []
        for child in root.children:
            if len(child.children) > 0:
                next_root.append(child)
        if len(next_root) == 0:
            return True
        elif len(next_root) > 1:
            return False
        else:
            return isSkewed(next_root[0])



######################################################################################    
def _getNodesEdges(node):
    '''
    returns list of nodes and edges of a tree from NODE data structure
    '''
    nodelist = [(node.hash, node.value)]
    edgelist = []
    for child in node.children:
        edgelist.append(((node.hash, node.value, node.volume), (child.hash, child.value, child.volume)))
        temp_nodelist, temp_edgelist = _getNodesEdges(child)
        nodelist += temp_nodelist
        edgelist += temp_edgelist
    
    return nodelist, edgelist

import pydot
def _createTree(root, label=None):
    '''
    convert a tree from NODE data structure to Pydot Graph for visualisation
    '''
    P = pydot.Dot(graph_type='digraph', label=label, labelloc='top', labeljust='left')#, nodesep="1", ranksep="1")
    
    nodelist, edgelist = _getNodesEdges(root)
    # Nodes
    for node in nodelist:
        n = pydot.Node(node[0], label=node[1])
        P.add_node(n)
    
    # Edges
    for edge in edgelist:
        e = pydot.Edge(*(edge[0][0], edge[1][0]), label=edge[1][2], dir='back')
        P.add_edge(e)
    return P


from IPython.display import Image, display
def _viewPydot(pydot):
    '''
    generates a visual plot of Pydot Graph
    '''
    plt = Image(pydot.create_png(prog='dot'))
    display(plt)
    
    
def viewTree(root):
    _viewPydot(_createTree(root))

import os
from .utility import create_directory
def saveTree(root, save):
    save = save.split('/')
    dir_name = '/'.join(save[:-1])
    if not save[-1].endswith('.png'):
        file_name = save[-1] + '.png'
    else:
        file_name = save[-1]
    create_directory(dir_name)
        
    # plt.savefig(os.path.join(dir_name, file_name), #dpi = 128,
    #             bbox_inches = 'tight', pad_inches = 0)

    _createTree(root).write_png(os.path.join(dir_name, file_name))

######################################################################################
def listToSkewTree(combination):
    root = node('root')
    root.volume = len(combination[-1])
    temp = root
    for idx, item in enumerate(combination):
        for x in item:
            temp.children.append(node(str(x)))
        temp.value = 'M{}'.format(idx)
        
        if idx < len(combination)-1:
            temp.children.append(node('mixxx'))
            temp = temp.children[-1]
            temp.volume = len(combination[-1]) - len(item)
    return root


######################################################################################
MIX_COUNTER = 0
def _listToTree(l):
    if type(l) != list:
#         print (l)
        return node(str(l))
    else:
        global MIX_COUNTER
        root = node('M{}'.format(MIX_COUNTER))
        MIX_COUNTER += 1
        root.volume = l[0] #if type(l[0]) == tuple else 1
        for item in l[1:]:
            root.children.append(_listToTree(item))
        return root
    
def listToTree(l):
    global MIX_COUNTER
    MIX_COUNTER = 0
    return _listToTree(l)

######################################################################################
