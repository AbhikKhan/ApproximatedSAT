def getTimeCount(A):
	res = -1
	for item in A:
		res = max(res, item[1])
	return res

def getCellCount(A):
	usedCells = set()
	for el in A:
		if (len(el) == 3):
			usedCells.add(tuple(el[2]))
	return len(usedCells)

def getValveCount(A):
	CONSTANT = 1
	valveSet = {}
	
	for el in A:
		if (len(el) == 4):
			mix = el[2]
			for i in range(4):
				x = mix[(i+1)%4][0] + mix[i][0]
				x = x/2.0
				y = mix[(i+1)%4][1] + mix[i][1]
				y = y/2.0
				if (x,y) in valveSet:
					valveSet[(x,y)] += CONSTANT
				else:
					valveSet[(x, y)] = CONSTANT
					
	actuationCount = 0
	for valve, actuation in valveSet.items():
		actuationCount += actuation
	uniqueValveCount = len(valveSet)
	
	return valveSet, uniqueValveCount, actuationCount


###############################################################################################
import os
from tqdm import tqdm
import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator, FormatStrFormatter
from matplotlib.markers import MarkerStyle
plt.ioff()
from .utility import create_directory

# plotting the matplotlib axes/grid
def plot_grid(H, axis, pos, edgelist, nodelist, nodesizes, nodecolors, nodelabels, 
			  mixnodelist=None, mixnodesizes=None, mixnodelabels=None, mixnodecolors=None,
			  title=None, save=False, show=True):    
	scale = 1.9
	xlen = abs(axis[0][0] - axis[0][1])
	ylen = abs(axis[1][0] - axis[1][1])
	fig = plt.figure(figsize=(xlen*scale, ylen*scale)) 
#     ax = plt.axes()
	plt.axis('off')

	m = MarkerStyle(marker="P", fillstyle='none')
	m._transform.scale(0.85)
	nodeCollection = nx.draw_networkx_nodes(H, pos, nodelist=nodelist, node_size=6400,node_color=nodecolors, 
											node_shape=m, alpha=1, linewidths=2, label='Cell', edgecolors='gray')
	nodeLabelCollection = nx.draw_networkx_labels(H, pos, labels=nodelabels, font_size=38)

	if mixnodelist:
		m = MarkerStyle(marker='s')
		m._transform.scale(3.8)
		mixNodeCollection = nx.draw_networkx_nodes(H, pos, nodelist=mixnodelist, node_size=256, node_color=mixnodecolors,
												node_shape=m, alpha=0.50, linewidths=2, label='mixNode', edgecolors='gray')
		mixNodeLabelCollection = nx.draw_networkx_labels(H, pos, labels=mixnodelabels, font_size=42, font_weight='heavy')

	v = MarkerStyle(marker="s")
	v._transform.scale(1,1.5)
	horizontalEdges = edgelist[0]
#     edgesCollection = nx.draw_networkx_edges(H, pos, edgelist=edgelist, width=1, arrows=True)
	edgesCollection = nx.draw_networkx_nodes(H, pos, nodelist=horizontalEdges, node_size=400, node_color='green',
											 node_shape=v, alpha=0.40, linewidths=2, label='Valve')
	
	v = MarkerStyle(marker="s")
	v._transform.scale(1.5,1)
	verticalEdges = edgelist[1]
#     edgesCollection = nx.draw_networkx_edges(H, pos, edgelist=edgelist, width=1, arrows=True)
	edgesCollection = nx.draw_networkx_nodes(H, pos, nodelist=verticalEdges, node_size=400, node_color='green',
											 node_shape=v, alpha=0.40, linewidths=2, label='Valve')


#     ax.set_yticks(range(axis[1][0], axis[1][1]+1))
#     ax.set_xticks(range(axis[0][0], axis[0][1]+1))
#     ax.xaxis.set_minor_locator(MultipleLocator(1))
#     ax.yaxis.set_minor_locator(MultipleLocator(1))
#     ax.xaxis.grid(True,'minor',linewidth=1, linestyle='dotted')
#     ax.yaxis.grid(True,'minor',linewidth=1, linestyle='dotted')
	
#     ax = plt.gca()
#     ax.grid(True)
#     ax.spines['left'].set_position('zero')
#     ax.spines['right'].set_color('none')
#     ax.spines['bottom'].set_position('zero')
#     ax.spines['top'].set_color('none')

#     minor_grid_lines = [tick.gridline for tick in ax.xaxis.get_minor_ticks()]
#     for idx,loc in enumerate(ax.xaxis.get_minorticklocs()):
#         minor_grid_lines[idx].set_c( 'b' )

	if False:#title:
		plt.title(title, fontsize=24)
#     plt.legend(loc='upper left', markerscale=0.5, shadow=True)#(bbox_to_anchor=(0.1, 0.9))
	if save:
		save = save.split('/')
		dir_name = '/'.join(save[:-1])
		if not save[-1].endswith('.png'):
			file_name = save[-1] + '.png'
		else:
			file_name = save[-1]
		create_directory(dir_name)
			
		plt.savefig(os.path.join(dir_name, file_name), #dpi = 128,
					bbox_inches = 'tight', pad_inches = 0)
	if show:
		plt.show(fig)
		
	plt.clf()
	plt.close(fig)
	return


def visualize_placement(info, axis = [[-5,5], [-5,5]], save_dir='frames'):
	H = nx.DiGraph()
	pos = {}
	nodelist = []
	horizontalEdgelist = []
	verticalEdgelist = []
	edgelist = []
	nodecolors = []
	nodesizes = []
	nodelabels = {}
	
	EMPTY_NODE_COLOR = '#ffffff'
	FILLED_NODE_COLOR = '#fbd2a7'#'#fccc98'
	WASH_NODE_COLOR = '#fbead7'#'#ffeedb'
	MIX_NODE_COLOR = '#9e9c9c'

	tempX, tempY = 0, 0
	for y in range(axis[1][0], axis[1][1]+1):
		for x in range(axis[0][0], axis[0][1]+1):
			coord = [x, y]

			H.add_node(str(coord))
			if (x>0):
				H.add_edge(str([x-1, y]), str(coord))
			if (y>0):
				H.add_edge(str([x, y-1]), str(coord))

			
			if (x-1 >= axis[0][0]):
				horizontalEdgelist.append(str([(x-1+x)/2.0, y]))#((str([x-1, y]), str([x, y])))
				pos[str([(x-1+x)/2.0, y])] = [(x-1+x)/2.0, y]
			if (y-1 >= axis[1][0]):
				verticalEdgelist.append(str([x, (y-1+y)/2.0]))#((str([x, y-1]), str([x, y])))
				pos[str([x, (y-1+y)/2.0])] = [x, (y-1+y)/2.0]

			pos[str(coord)] = coord
			nodelist.append(str(coord))
			nodecolors.append(EMPTY_NODE_COLOR)
			nodesizes.append(500)
			tempX += 1
		tempY += 1
	edgelist = [horizontalEdgelist, verticalEdgelist]

	MAX_TIME = info[-1][1]
	for timestamp in tqdm(range(1, MAX_TIME+1)):
		currTimeOps = []
		mixnodelist = []
		mixnodesizes = []
		mixnodelabels = {}
		mixnodecolors = []
		for item in info:
			if item[1] == timestamp:
				currTimeOps.append(item)

		for item in currTimeOps:
			# load
			if (len(item) == 3):
				coord = item[2]
				idx = nodelist.index(str(coord))
				nodecolors[idx] = FILLED_NODE_COLOR
				nodesizes[idx] = 1000
				# print (item, type(item))
				nodelabels[str(coord)] = item[0] #r'$'+item[0][0]+'_{'+item[0][1:]+'}$'
		plot_grid(H, axis, pos, edgelist, nodelist, nodesizes, nodecolors, nodelabels,
				  title='TimeStamp={}_1'.format(timestamp), save='./{}/{}_1'.format(save_dir, timestamp), show=False)


		for item in currTimeOps:
			# mix
			if (len(item) == 4):
				coord = [(x+y+w+z)/4.0 for x,y,z,w in zip(*item[2])]
				pos[str(coord)] = coord
				mixnodelist.append(str(coord))
				mixnodesizes.append(500)
				mixnodelabels[str(coord)] = r'$'+item[0][0]+'_{'+item[0][1:]+'}$'
				mixnodecolors.append(MIX_NODE_COLOR)

		plot_grid(H, axis, pos, edgelist, nodelist, nodesizes, nodecolors, nodelabels,
				  mixnodelist, mixnodesizes, mixnodelabels, mixnodecolors,
				  title='TimeStamp={}_2'.format(timestamp), save='./{}/{}_2'.format(save_dir, timestamp), show=False)


		for item in currTimeOps:
			# wash
			if (len(item) == 4):
				for washNode in item[3]:
					coord = washNode
					idx = nodelist.index(str(coord))
					nodecolors[idx] = WASH_NODE_COLOR
				for mixNode in item[2]:
					coord = mixNode
					idx = nodelist.index(str(coord))
					nodelabels[str(coord)] = r'$'+item[0][0]+'_{'+item[0][1:]+'}$'
					

		plot_grid(H, axis, pos, edgelist, nodelist, nodesizes, nodecolors, nodelabels,
				  mixnodelist, mixnodesizes, mixnodelabels, mixnodecolors,
				  title=r'Time, $t='+str(timestamp)+'$', save='./{}/{}_3'.format(save_dir, timestamp), show=False)

		for item in currTimeOps:
			# remove mix nodes and wash nodes
			if (len(item) == 4):
				coord = item[2][0]
				idx = nodelist.index(str(coord))
				nodecolors[idx] = FILLED_NODE_COLOR
				nodesizes[idx] = 500
				nodelabels[str(coord)] = r'$'+item[0][0]+'_{'+item[0][1:]+'}$'
				for washNode in item[3]:
					coord = washNode
					idx = nodelist.index(str(coord))
					nodecolors[idx] = EMPTY_NODE_COLOR
					nodesizes[idx] = 500
					nodelabels[str(coord)] = ''
		plot_grid(H, axis, pos, edgelist, nodelist, nodesizes, nodecolors, nodelabels,
				  title='TimeStamp={}_4'.format(timestamp), save='./{}/{}_4'.format(save_dir, timestamp), show=False)            
	
	return
