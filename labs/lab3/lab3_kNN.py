import pandas
import Queue


# Calculate distance from every item in training set (Added as a new column)
def distance(data, a, cl):
	data["distance"] = 0
	for col in data.columns:
		if (col != "distance" and col != cl):
			col_score = data[col].apply(lambda x: 1 if (x == a[col]) else 0)
			data["distance"] = data["distance"] + col_score
	return data

# Classify a single item using k-nearest-neighbors algorithm
def kNN(data, cl, k, a):
	# Calculate distance
	data = distance(data, a, cl)

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
T = 2950
training = df[:T]	# Use first T records for training
test = df[T:]		# Use the rest for testing
k = 10

# Calculate confusion matrix for test run
tp = 0
fn = 0
fp = 0
tn = 0
for i, val in test.iterrows():
	correct = val["class"]
	result = kNN(training, "class", k, val)
	if(result == "e"):
		if(result == correct):
			tp = tp + 1
		else:
			fp = fp + 1
	else:
		if(result == correct):
			tn = tn + 1
		else:
			fn = fn + 1

pos_rec = 100-(100*fn/float(tp))
neg_rec = 100-(100*fp/float(tn))
total_rec = 100-(100*(fn+fp)/float(tp+tn))

print("classes\t\tedible\tposinous\ttotal\trecognition(%)")
print("edible\t\t{0}\t\t{1}\t\t\t{2}\t\t{3:.2f}".format(tp, fn,tp+fn,pos_rec))
print("posinous\t{0}\t\t{1}\t\t\t{2}\t\t{3:.2f}".format(fp, tn, fp+tn,neg_rec))
print("total\t\t{0}\t\t{1}\t\t\t{2}\t\t{3:.2f}".format(tp+fp, fn+tn, tp+fp+fn+tn, total_rec))