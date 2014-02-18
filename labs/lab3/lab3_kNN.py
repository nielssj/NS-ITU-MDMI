import pandas
import Queue


# Calculate distance from every item in training set (Added as a new column)
def distance(data, a):
	data["distance"] = 0
	for col in data.columns:
		if (col != "distance"):
			col_score = data[col].apply(lambda x: 1 if (x == a[col][0]) else 0)
			data["distance"] = data["distance"] + col_score
	return data

# Classify a single item using k-nearest-neighbors algorithm
def kNN(data, cl, k, a):
	# Calculate distance
	data = distance(data, a)

	# Take k nearest neighbors
	data = data.sort("distance")
	neighbors = data.tail(k)

	# Determine highest represented class in neighbors
	gb = neighbors.groupby(cl)
	gb_s = gb.size()
	gb_s.order()
	return gb_s.head(1).keys()[0]


# Mushroom example run
f_in2 = open("agaricus-lepiotadata_wheader.txt", "r")
df = pandas.read_csv(f_in2, sep=",")
training = df[1:]
test = df[:1]
k = 5

result = kNN(training, "class", k, test.to_dict(outtype = "list"))

if(result == "e"):
	print("Congratulations, the mushroom is edible!")
else:
	print("Dude, don't eat that..")
