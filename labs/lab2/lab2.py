import csv
import re


f_in = open("Data_Mining_Student_DataSet_Spring_2013_Fixed.csv", "r")
reader = csv.reader(f_in, delimiter = ";")

# Read header
headers = reader.next()
headers[0] = headers[0].strip("\xef\xbb\xbf") 
column = {}
for h in headers:
	if(h != ""):
		column[h] = []

hlen = len(headers)-1 # The minus 1 is because the header for some reason has an extra semicolon
for row in reader:
	# Correct number of values? (Otherwise discard)
	if (len(row) != hlen):
		continue
	# Add to respective columns
	for h, v in zip(headers, row):
		column[h].append(v)

# Clean "age"
age_clean = []
for val in column["age"]:
	# Is it a real value?
	match_c = re.search("\d\d", val)
	if (match_c != None):
		age_clean.append(int(float(match_c.group(0))))
		continue
	age_clean.append(-1)
column["age"] = age_clean
print("\nCleaned age values:")
print(age_clean)

# Clean "prog_skill"
prog_clean = []
for val in column["prog_skill"]:
	# Is it a real value?
	match_c = re.search("\d", val)
	if (match_c != None):
		prog_clean.append(float(match_c.group(0)))
		continue
	# Is it a range?
	match_c = re.search("(\d)-(\d)", val)
	if (match_c != None):
		f = float(match_c.group(1))
		t = float(match_c.group(2))
		prog_clean.append((f+t)/2)
		continue
	prog_clean.append(-1)
column["prog_skill"] = prog_clean
print("\nCleaned programming skill values:")
print(prog_clean)

# Clean "english_level"
english_clean = []
for val in column["english_level"]:

	# Is it a real value?
	match_c = re.search("^(\d+)$", val)
	if (match_c != None):
		english_clean.append(float(match_c.group(0)))
		continue

	# Is it a range?
	match_c = re.search("(\d)-(\d)", val)
	if (match_c != None):
		f = float(match_c.group(1))
		t = float(match_c.group(2))
		english_clean.append((f+t)/2)
		continue

	# Is it a punctuation float? (e.g. 61.5)
	match_c = re.search("(\d+\.\d+)", val)
	if (match_c != None):
		english_clean.append(float(match_c.group(0)))
		continue

	# Is it a comma float? (e.g. 61,5)
	match_c = re.search("(\d+,\d+)", val)
	if (match_c != None):
		valf = match_c.group(0)
		english_clean.append(float(valf.replace(",", ".")))

	english_clean.append(-1)
column["english_level"] = english_clean

print("\nCleaned english levels:")
print(english_clean)


# Clean "animal"
animal_clean = []
for val in column["animal"]:
	lower = val.lower()
	match_c = re.search("(elephant|zebra|asparagus)", lower)
	if (match_c != None):
		animal_clean.append(match_c.group(0))
		continue
	animal_clean.append("")
column["animal"] = animal_clean

print("\nCleaned animal value:")
print(animal_clean)


# "Min-max normalize" programming skill
prog_skill = column["prog_skill"]
prog_normal = []
prog_min = min(prog_skill)
prog_max = max(prog_skill)
for val in prog_skill:
	v_normal = ( (val - prog_min ) / (prog_max - prog_min) ) * (1 - 0) + 0  # Yes, I know the last bit is pointless for 0-1 min, but just for personal notes
	prog_normal.append(v_normal)

print("\nMin-max normalized programming skill values:")
print(prog_normal)


# "Decimal scaling" english level
english_scaled = []
for val in column["english_level"]:
	english_scaled.append(val/100)
column["english_level"] = english_scaled

print("\nDecimal scaled english levels:")
print(column["english_level"])



# Central tendencies of prog_skill (Mean/Median/Mode)
prog_sum = 0
for val in prog_skill:
	prog_sum += val
prog_mean = prog_sum / len(prog_skill)			# Mean

prog_sorted = sorted(prog_skill)
prog_median = prog_sorted[len(prog_sorted)/2] 	# Median

prog_freq = dict()
for val in prog_skill:
	if(val in prog_freq):
		prog_freq[val] = prog_freq[val] + 1
	else:
		prog_freq[val] = 1
freqk = -1
freqm = 0
for key, val in enumerate(prog_freq):
	if(val > freqm):
		freqk = key
		freqm = val
prog_mode = freqk								# Mode

print("\nCentral tendencies of programming skills")
print("Mean\tMedian\tMode")
print("{0:.3f}\t{1:.3f}\t{2:.3f}".format(prog_mean, prog_median, prog_mode))


# Five-number summary
N = len(prog_sorted)
print("\nFive-number summary of programming skills")
fn_min = prog_sorted[0]						# Minimum
fn_q1 = prog_sorted[N/4]					# Q1
fn_med = prog_sorted[len(prog_sorted)/2]	# Median
fn_q3 = prog_sorted[N/4 * 3]				# Q3
fn_max = prog_sorted[N-1]					# Maximum
print("Min\t\tQ1\t\tMedian\tQ3\t\tMax")
print("{0:.3f}\t{1:.3f}\t{2:.3f}\t{3:.3f}\t{4:.3f}".format(fn_min, fn_q1, fn_med, fn_q3, fn_max))