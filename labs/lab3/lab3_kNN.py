import pandas
import numpy
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

def testRun(train, test, k):
	results = []
	for i, val in test.iterrows():
		correct = val["class"]
		result = kNN(train, "class", k, val)
		results.append((val["class"],result))
		print("Prediction: {0} (actual: {1})".format(result, correct))
	return results


# Conduct test using holdout method (single partition split into training/test data)
def holdoutTest(data, split, k):
	test_i = numpy.random.choice(data.index, split, replace=False)
	test = data.ix[test_i]		# Use T random records for test
	train = data.drop(test_i)	# Use the rest for training
	return testRun(train, test, k)

# Conduct test using cross-validation method  (Randomly partition and rotate which one is test set)
def crossValidation(data, p, k):
	# Divide into random partitions
	parts = []
	rs = len(data)/p
	for i in range(0, p):
		ri = numpy.random.choice(data.index, size=rs, replace=False)
		parts.append(data.ix[ri])
		data = data.drop(ri)
	# Perform test rotating which partition is the test set
	results = []
	for i, part in enumerate(parts):
		train = pandas.concat(parts[:i] + parts[(i+1):])
		test = parts[i]
		p_results = testRun(train, test, k)
		results.append(p_results)
	return numpy.concatenate(results)


# Calculate and print confusion matrix
def confusionMatrix(results):
	tp = 0
	fn = 0
	fp = 0
	tn = 0
	for (result, correct) in results:
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
	pos = tp + fp
	neg = tn + fn
	total_rec = 100-(100*(fn+fp)/float(tp+tn))
	sens = 100 * float(tp)/pos
	spec = 100 * float(tn)/neg
	prec = 100 * float(tp)/(tp + fp)
	acc = sens * pos / (pos + neg) + spec * neg / (pos + neg)
	print("\nclasses\t\tedible\tposinous\ttotal\trecognition(%)")
	print("edible\t\t{0}\t\t{1}\t\t\t{2}\t\t{3:.2f}".format(tp, fn,tp+fn,sens))
	print("posinous\t{0}\t\t{1}\t\t\t{2}\t\t{3:.2f}".format(fp, tn, fp+tn,spec))
	print("total\t\t{0}\t\t{1}\t\t\t{2}\t\t{3:.2f}".format(tp+fp, fn+tn, tp+fp+fn+tn, total_rec))
	print("------------------------------------------------")
	print("sensivity:\t\t{0:.2f}".format(sens))
	print("specificity:\t{0:.2f}".format(spec))
	print("precision:\t\t{0:.2f}".format(prec))
	print("accuracy:\t\t{0:.2f}".format(acc))

# Mushroom example run
f_in2 = open("agaricus-lepiotadata_wheader.txt", "r")
df = pandas.read_csv(f_in2, sep=",")
results = crossValidation(df[:100], 10, 10)
#results = holdoutTest(df[:100], 33, 10)
confusionMatrix(results)