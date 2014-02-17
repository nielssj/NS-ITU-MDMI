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
			if(g > g_high_val):
				g_high_val = g
				g_high_attr = attr
	return g_high_attr


# Test calculations (depicted on lecture slides)
#print("Best attribute for splitting is \"{0}\"".format(attr_selection(df, "buys_computer", df.columns)))

class Node:
	def __init__(self, label):
		self.label = label
		self.children = dict()
	def addChild(self, child, label):
		self.children[label] = child
	def makeDotGraph(self, graph):
		node = pydot.Node(self.label)
		graph.add_node(node)
		for edge in self.children:
			c_node = self.children[edge].makeDotGraph(graph)
			c_edge = pydot.Edge(node, c_node, label=edge)
			graph.add_edge(c_edge)
		return node


# Create decision tree (ID3)
def createDTree(df, cl):
	attrs = set(df.columns)
	if(len(df.groupby(cl)) == 1):
		# All tuples are the same class, returning leaf
		classcol = df["buys_computer"]
		domin = classcol[classcol.index[0]]
		return Node(domin)
	if(len(attrs) == 0):
		# No more attributes to select from, returning leaf with majority
		major = majority(df, cl)
		return Node(major)
	# Splitting on attribute, running recursively on resulting partitions
	split_attr = attr_selection(df, cl, attrs)	# Pick attribute with highest gain
	attrs.remove(split_attr)
	node = Node(split_attr)
	for group in df.groupby(split_attr):
		childnode = createDTree(group[1][list(attrs)], cl)
		node.addChild(childnode, group[0])
	return node


# Classify one or more records
def classify(rcs, cl, root):
	res = dict()
	for i in range(0, len(rcs[root.label])):
		n_cur = root
		while(len(n_cur.children) > 0):
			n_cur = n_cur.children[rcs[n_cur.label][i]]
		res[i] = n_cur.label
	return res


training = df[2:]

attrs = set(df.columns)
attrs.remove("buys_computer")
test = df[list(attrs)][:2]
test = test.to_dict()

graph = pydot.Dot(graph_type='graph')
root = createDTree(training, "buys_computer")
root.makeDotGraph(graph)
graph.write_png("example1.png")

classifcations = classify(test, "buys_computer", root)
test["buys_computer"] = classifcations
print(test)