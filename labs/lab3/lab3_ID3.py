import pandas
import pydot
import numpy
import math


f_in2 = open("buys-computer.txt", "r")
df = pandas.read_csv(f_in2, sep=";")

# Calculate information needed for attribute
def info(part, col):
	c_j = float(len(part))
	cs_j = []
	for group in part.groupby(col):
		cs_j.append(float(len(group[1])))

	D = 0.0
	for c_i in cs_j:
		D = D - (c_i/c_j) * math.log(c_i/c_j, 2)
	return D

	return D

# Calculate information needed for partitioning a specific column
def infoA(df, cl, col):
	D = 0
	gb = df.groupby(col)
	for group in gb:
		# Get propability
		c_j = float(len(group[1]))

		# Get class entropy in partition
		inf_j = info(group[1], cl)
		
		# Add to overall sum
		D = D + c_j/len(df) * inf_j
	return D

# Calculate gain from partitioning a specific column
def gain(df, cl, col):
	# Get overall class entropy
	inf_j = info(df, cl)

	# Calculate information needed for specific attribute
	inf_col = infoA(df, cl, col)

	return inf_j - inf_col

def majority(df, cl):
	gb = df.groupby(cl)
	gr_len = 0
	gr_name = ""
	for group in gb:
		g = len(group[1])
		if(g > gr_len):
			gr_len = g
			gr_name = group[0]
	return gr_name

def attr_selection(df, cl, attrs):
	g_high_val = 0
	g_high_attr = ""
	for attr in attrs:
		if(attr != cl):
			g = gain(df, cl, attr)
			print ("Gain({0}) = {1}".format(attr, g))
			if(g > g_high_val):
				g_high_val = g
				g_high_attr = attr
	return g_high_attr


# Test calculations (depicted on lecture slides)
#print("Best attribute for splitting is \"{0}\"".format(attr_selection(df, "buys_computer", df.columns)))

class Node:
	def __init__(self, label):
		self.label = label
		self.children = []
	def addChild(self, child, label):
		self.children.append((label,child))
	def makeDotGraph(self, graph):
		node = pydot.Node(self.label)
		graph.add_node(node)
		for c in self.children:
			c_node = c[1].makeDotGraph(graph)
			c_edge = pydot.Edge(node, c_node, label=c[0])
			graph.add_edge(c_edge)
		return node


# Create decision tree (ID3)
def createDTree(df, cl, attrs):
	if(len(df.groupby(cl)) == 1):
		classcol = df["buys_computer"]
		domin = classcol[classcol.index[0]]
		print("All tuples are of the same class ({0}), returning leaf".format(domin))
		return Node(domin)
	if(len(attrs) == 0):
		major = majority(df, cl)
		print("No more attributes to select from, returning leaf with majority ({0})".format(major))
		return Node(major)
	split_attr = attr_selection(df, cl, attrs)
	attrs.remove(split_attr)
	node = Node(split_attr)
	print("Chose to split on attribute \"{0}\"".format(split_attr))
	for group in df.groupby(split_attr):
		print("Running recursively on partition \"{0}\"".format(group[0]))
		childnode = createDTree(group[1][list(attrs)], cl, attrs)
		node.addChild(childnode, group[0])
	return node


graph = pydot.Dot(graph_type='graph')
root = createDTree(df, "buys_computer", set(df.columns))
root.makeDotGraph(graph)
graph.write_png("example1.png")