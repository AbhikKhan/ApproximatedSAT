from NTM import *
from collections import deque  


def nodeCreationDemo():
    '''
        Demo example to create mixing node and children.
    '''
    root = node('M1')
    root.children = [node('M2', 1), node('M3', 3)]
    root.children[0].children = [node('R1', 2), node('R2', 1), node('R3', 1)]
    root.children[1].children = [node('R1', 1), node('R2', 3)]

    # save tree at given location
    saveTree(root, './demoFolder/nodeCreation.png')


def listToTreeDemo():
    '''
        Demo example to create tree from list.
    '''
    root = [4, 
            'R1', 'R1', [1, 'R2', 'R3', 'R4', 'R4'], 
            [1, [3, 'R2', 'R2', 'R4', 'R4'], [1, 'R3', [3, 'R2', 'R2', 'R3', 'R4']]]]
    output_tree = listToTree(root)
    saveTree(output_tree, './demoFolder/listToTree.png')
    return output_tree

def genmixDemo():
    '''
        Demo example for genMix 318:123:234:237:112
    '''
    input_ratio = [('r0', 318), ('r1', 123), ('r2', 234), ('r3', 237), ('r4', 112)]
    output_tree = genMix(input_ratio, 4)
    saveTree(output_tree, './demoFolder/genmix.png')
    return output_tree


def hdaDemo(root):
    '''
        Demo example for HDA
    '''
    output_tree = hda(root)
    saveTree(output_tree, './demoFolder/hda.png')
    return output_tree


def bfs(root):
    queue = deque()
    queue.append(root)

    while queue:
        s = len(queue)
        nodes = []
        reags = []
        while s:
            s -= 1
            node = queue.popleft()
            nodes += [child for child in node.children if child.children != []]
            reags += [child.value for child in node.children if child.children == []]

        for node in nodes:
            queue.append(node)
        for n in nodes:
            print(n.value, end=' ')
        print()

            

def ntmDemo(output_tree):
    '''
        Demo example for getting placement of all the cells
    '''
    output_assignment_set = ntm(output_tree, [5, 5], [1])

    # Assignment of all the internal node
    assignment = {}
    for item in output_assignment_set:
        # print(item)
        if item[0][0] == 'M':
            assignment[item[0]] = item[2]

    return assignment


def main():
    nodeCreationDemo()
    root = listToTreeDemo()
    root = genmixDemo()
    tree = hdaDemo(root)
    bfs(tree)
    assignment = ntmDemo(root)

    for key in assignment:
        print(key, assignment[key])

    # To get the children of a internal node.
    # print(*[child.value for child in tree.children])

    

if __name__ == "__main__":
    main()