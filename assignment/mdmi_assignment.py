import csv
import codecs
import re
import exceptions
import matplotlib.pyplot as plt
import apriori

f_in = open("data_mining_2014_dataset.csv", "r")
reader = csv.reader(f_in, delimiter=';')

header = reader.next()
header[0] = header[0].lstrip("\xef\xbb\xbf") # Strip BOM
print(header)

columns = dict()
for row in reader:
	for i, value in enumerate(row):
		key = header[i]
		if(key not in columns.keys()):
			columns[key] = [value]
		else:
			columns[key].append(value)


#for key in columns.keys():
#	print("{0}: {1}".format(key, columns[key]))

# Clean the OS column
oss = []
for val in columns["OS"]:
	if(re.search("win", val, re.IGNORECASE) != None):
		oss.append("win")
	elif(re.search("linux|debian|ubuntu", val, re.IGNORECASE)):
		oss.append("linux")
	elif (re.search("osx|os x|mac", val, re.IGNORECASE)):
		oss.append("osx")
	else:
		oss.append("-")

# Clean the Age column
age = []
for val in columns["age"]:
	try:
		age.append(int(float(val)))
	except exceptions.ValueError:
		age.append(-1)

# Clean english skill column
eng = []
for val in columns["EngSkill"]:
	try:
		eng.append(int(float(val)))
	except exceptions.ValueError:
		eng.append(-1)

# Clean programming skill column
prog = []
for val in columns["prog_skill"]:
	try:
		prog.append(float(val))
	except exceptions.ValueError:
		prog.append(-1)

# Clean uni years column
uni = []
for val in columns["uni_yrs"]:
	try:
		uni.append(float(val))
	except exceptions.ValueError:
		uni.append(-1)

# Plot english skill vs. age
xaxis = []
yaxis = []
for i, val in enumerate(age):
	if(uni[i] > 0 and eng[i] > 0):
		xaxis.append(val)
		#xaxis.append(eng[i])
		#yaxis.append(eng[i])
		#yaxis.append(prog[i])
		yaxis.append(uni[i])
plt.plot(xaxis, yaxis, "ro")
#plt.axis([15,50,40,80])
plt.ylabel('Programming skill')
plt.xlabel('Age')
plt.show()

print(columns["progLangs"])

# Count language frequencies
langfreq = dict()
for val in columns["progLangs"]:
	for lang in val.split(','):
		langl = lang.lower().lstrip()
		if(langl in langfreq.keys()):
			langfreq[langl] = langfreq[langl] + 1
		else:
			langfreq[langl] = 1

# List language frequencies of languages appearing more than once
langfreqc = dict()
langfreqkey = []
langfreqindex = dict()
index = 0
for lang in langfreq.keys():
	freq = langfreq[lang]
	if(freq > 1 and lang != ""):
		langfreqc[lang] = freq
		langfreqkey.append(lang)
		langfreqindex[lang] = index
		print("{0}: {1}".format(lang, langfreq[lang]))
		index = index + 1

print(langfreqc)

# Create boolean table for languages
boolLang = []
for val in columns["progLangs"]:
	row = [False] * len(langfreqindex)
	for lang in val.split(','):
		langl = lang.lower().lstrip()
		if(langl in langfreqkey):
			row[langfreqindex[langl]] = True
	boolLang.append(row)

# Create list of sets for languages
setLang = []
for i, val in enumerate(columns["progLangs"]):
	row = []
	# Add languages
	for lang in val.split(','):
		langl = lang.lower().lstrip()
		if(langl in langfreqkey):
			row.append(langl)
	# Add OS
	if (not oss[i] == "-"):
		row.append(oss[i])
	# Add if all data good
	if(len(row) > 0):
		setLang.append(row)

print(langfreqkey)
for row in setLang:
	print(row)

apriori.apriori(setLang, 20)

# Verification (compute lift)
A = 0
B = 0
AB = 0
count = float(len(setLang))
for row in setLang:
	Abool = "c#" in row
	Bbool = "win" in row
	if(Abool):
		A = A + 1
	if(Bbool):
		B = B + 1
	if(Abool and Bbool):
		AB = AB + 1

lift = (AB / count) / ((A/count) * (B/count))
print("A: {0}, B: {1}, AB: {2}".format(A, B, AB))
print("lift(A,B) = {0}".format(lift))