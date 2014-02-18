import pandas
import Queue


f_in2 = open("agaricus-lepiotadata_wheader.txt", "r")
df = pandas.read_csv(f_in2, sep=",")

def compare(df, a, b):
	score = 0
	for col in df.columns:
		if(df[col][a] == df[col][b]):
			score = score + 1
	return score


def kNN(df, cl, k):
	close = []
	for i in range(2, len(df)):
		val = compare(df, 1, i)
		if(len(close) < k):
			close.append((val, i, df[cl][i]))
		else:
			close = sorted(close)
			if(val > close[0][0]):
				close[0] = (val, i, df[cl][i])
	return close

def classify(df, cl, k):
	closest = kNN(df, cl, k)
	score = 0
	for n in closest:
		if(n[2] == "e"):
			score = score + 1
	return score

k = 5
score = classify(df, "class", k)

if(score > k/2):
	print("Congratulations, the mushroom is edible!")
else:
	print("Dude, don't eat that..")
