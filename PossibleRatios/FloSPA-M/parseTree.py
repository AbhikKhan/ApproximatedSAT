import pydot

NodeList = {}

class Node:
    def __init__(self, label):
        self.label = label # M1 or R1
        self.children = [] #[[node1, weight1], [node2, weight2]]
        
    def addChild(self, child, weight):
        self.children.append([child, weight])


def createGraphFromDotFile(dot_file):
    graph = pydot.graph_from_dot_file(dot_file)

    if len(graph) > 0:
        graph = graph[0]            
        node_labels = {}
        edge_weights = {}
        i = 0
        for node in graph.get_node_list():
            node_name = node.get_name()
            label = node.get_attributes().get('label')
            
            if label is not None:
                label = label.strip('"')
                if label[0] == "R":
                    node_labels[node_name] = label
                else:
                    node_labels[node_name] = f"M{i}"
                    i+=1
                # print(f"Node: {node_name}, Label: {node_labels[node_name]}")
            
        for edge in graph.get_edge_list():
            source = edge.get_source()
            destination = edge.get_destination()
            label = edge.get_attributes().get('label')
            
            if label is not None:
                weight = int(label)
                edge_weights[(source, destination)] = weight
                # print(f"Edge: {source} -> {destination}, Weight: {weight}")
        
        return node_labels, edge_weights
    else:
        print("No graph found.")
        return None, None

def getList(node):
    subTree = []
    for (child, weight) in node.children:
        if len(child.children) == 0:
            subTree.extend(weight * [child.label])
        else:
            childList = [weight]
            childList.extend(getList(child))
            subTree.append(childList)

    return subTree

def getRoot(file):
    nodeLabels, edgeList = createGraphFromDotFile(file)
    for node in nodeLabels:
        treeNode = Node(nodeLabels[node])
        NodeList[int(node)] = treeNode

    # Adding child of a node
    for (u, v) in edgeList:
        NodeList[int(u)].addChild(NodeList[int(v)], edgeList[(u, v)]) # name and weight
    
    # Get the rootlist that we need to create a tree using NTM listtotree
    startNode = 1
    root = [4]
    root.extend(getList(NodeList[startNode]))
    
    # Getting all the reagent information of mixing node
    NodeList.clear()
    return root

if __name__ == "__main__":
    file = "skeletonTreeAfterAnnotation.dot"
    root = getRoot(file)
    print(root)