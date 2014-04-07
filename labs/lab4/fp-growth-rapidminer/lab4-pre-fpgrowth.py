# Provided set of transactions (Pasted from provided Java-files)
trs = [ [1, 2, 3, 4, 5 ], [ 1, 3, 5 ], [ 2, 3, 5 ], [ 1, 5 ], [ 1, 3, 4 ], [ 2, 3, 5 ], [ 2, 3, 5 ], [ 3, 4, 5 ], [ 4, 5 ], [ 2 ], [ 2, 3 ], [ 2, 3, 4 ], [ 3, 4, 5 ] ];

out = ""

# Headers
for i in range(5):
	out += "item{0};".format(i)
out = out.strip(";")

for tr in trs:
	out += "\n"
	st = [False, False, False, False, False]
	for item in tr:
		st[item-1] = True
	for item in st:
		if(item):
			out += "1;"
		else:
			out += "0;"
	out = out.strip(";")

print(out)