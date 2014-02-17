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


k = 5
close = []
for i in range(2, len(df)):
	val = compare(df, 1, i)
	if(len(close) < k):
		close.append((val, i, df["class"][i]))
	else:
		close = sorted(close)
		if(val > close[0][0]):
			close[0] = (val, i, df["class"][i])


print("Closest rows are (dist,id,class):\n{0}".format(close))

edible_score = 0
for n in close:
	if(n[2] == "e"):
		edible_score = edible_score + 1

if(edible_score > k/2):
	print("Congratulations, the mushroom is edible!")
else:
	print("Dude, don't eat that..")
