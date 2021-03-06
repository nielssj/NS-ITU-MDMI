import csv
import re
import pandas


f_in2 = open("Data_Mining_Student_DataSet_Spring_2013_Fixed.csv", "r")
df = pandas.read_csv(f_in2, sep=";")
col_old = df.columns.values
col_old[0] = "age"
df.columns = col_old

# Clean "age"
age_clean = []
for val in df["age"]:
	# Is it a real value?
	match_c = re.search("\d\d", val)
	if (match_c != None):
		age_clean.append(int(float(match_c.group(0))))
		continue
	age_clean.append(-1)
df["age"] = age_clean
print("\nCleaned age values:")
print(df["age"].values)

# Clean "prog_skill"
prog_clean = []
for val in df["prog_skill"]:
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
df["prog_skill"] = prog_clean
print("\nCleaned programming skill values:")
print(df["prog_skill"].values)

# Clean "english_level"
english_clean = []
for val in df["english_level"]:

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
		continue

	english_clean.append(-1)
df["english_level"] = english_clean

print("\nCleaned english levels:")
print(df["english_level"].values)


# Clean "animal"
animal_clean = []
for val in df["animal"]:
	lower = val.lower()
	match_c = re.search("(elephant|zebra|asparagus)", lower)
	if (match_c != None):
		animal_clean.append(match_c.group(0))
		continue
	animal_clean.append("")
df["animal"] = animal_clean

print("\nCleaned animal value:")
print(df["animal"].values)


# Clean "winter_tired"
winter_clean = []
for val in df["winter_tired"]:
	lower = val.lower()
	if ("yes" in lower):
		winter_clean.append(True)
	elif ("no" in lower):
		winter_clean.append(False)
	else:
		winter_clean.append(None)
df["winter_tired"] = winter_clean

print("\nCleaned winter_tired values:")
print(df["winter_tired"].values)


# Clean "more_dk_mnts"
mnts_clean = []
for val in df["more_dk_mnts"]:
	lower = val.lower()
	if ("yes" in lower):
		mnts_clean.append(True)
	elif ("no" in lower):
		mnts_clean.append(False)
	else:
		mnts_clean.append(None)
df["more_dk_mnts"] = mnts_clean

print("\nCleaned more_dk_mnts values:")
print(df["more_dk_mnts"].values)


# "Min-max normalize" programming skill
prs = df["prog_skill"]
prog_normal = ( (prs - prs.min()) / (prs.max() - prs.min()) ) * (1 - 0) + 0 # Yes, I know the last bit is pointless for 0-1 min, but just for personal notes
print("\nMin-max normalized programming skill values:")
print(prog_normal.values)


# "Decimal scaling" english level
df["english_level"] = df["english_level"]/100
print("\nDecimal scaled english levels:")
print(df["english_level"].values)


# Central tendencies of prog_skill (Mean/Median/Mode)
prs = df["prog_skill"]
prs_freq = dict()
for val in prs:
	if(val in prs_freq):
		prs_freq[val] = prs_freq[val] + 1
	else:
		prs_freq[val] = 1
freqk = -1
freqm = 0
for key, val in enumerate(prs_freq):
	if(val > freqm):
		freqk = key
		freqm = val
prs_mode = freqk								# Mode (Note: Pandas series and data frames got a mode function in feb 2014)

print("\nCentral tendencies of programming skills")
print("Mean\tMedian\tMode")
print("{0:.3f}\t{1:.3f}\t{2:.3f}".format(prs.mean(), prs.median(), prs_mode))


# Five-number summary
prsd = df["prog_skill"].describe()
print("\nFive-number summary of programming skills")
print("Min\t\tQ1\t\tMedian\tQ3\t\tMax")
print("{0:.3f}\t{1:.3f}\t{2:.3f}\t{3:.3f}\t{4:.3f}".format(prsd["min"], prsd["25%"], prsd["50%"], prsd["75%"], prsd["max"]))


# Correlation analysis (Numerical data)

# Correlation between age and programming skill
age = df["age"]
prs = df["prog_skill"]
var_sum = ((age - age.mean()) * (prs - prs.mean())).sum()
corr = var_sum / (len(age) * age.std() * prs.std())
print("\nCorrelation between age and programming skill")
print("Manual Pearson: {0:.5f}".format(corr))
print("Pandas Pearson: {0:.5f}".format(age.corr(prs, method="pearson")))
print("Kendall:\t\t{0:.5f}".format(age.corr(prs, method="kendall")))
print("Spearman:\t\t{0:.5f}".format(age.corr(prs, method="spearman")))

# Correlation between age and english level
age = df["age"]
englvl = df["english_level"]
print("\nCorrelation between age and english level")
print("Pandas Pearson: {0:.5f}".format(age.corr(englvl, method="pearson")))

# Correlation between programming skill and english level
prs = df["prog_skill"]
englvl = df["english_level"]
print("\nCorrelation between programming skill and english level")
print("Pandas Pearson: {0:.5f}".format(prs.corr(englvl, method="pearson")))


# Correlation analysis (Nominal data)

# Correlation between wanting more mountains and disliking winther
print("\nCorrelation between wanting more mountains and disliking winther")

# Filter down to rows with valid values in both attributes
df2 = df[(df["more_dk_mnts"] == True) | (df["more_dk_mnts"] == False)]
df2 = df2[(df2["winter_tired"] == True) | (df2["winter_tired"] == False)]
N = df2["more_dk_mnts"].count()

# Compute "contingency table"
ctd = [[0, 0], [0, 0]]
s_mnts = df2["more_dk_mnts"]
s_wnt = df2["winter_tired"]
for (i, mnts) in s_mnts.iteritems():
	if(mnts == True):
		if(s_wnt[i] == True):
			cur = ctd[0][0]
			ctd[0][0] = cur + 1
		else:
			cur = ctd[0][1]
			ctd[0][1] = cur + 1
	else:
		if(s_wnt[i] == True):
			cur = ctd[1][0]
			ctd[1][0] = cur + 1
		else:
			cur = ctd[1][1]
			ctd[1][1] = cur + 1
print("Contingency table: {0}".format(ctd))
print(df2.apply(lambda x: x["more_dk_mnts"] == True and x["winter_tired"] == True, axis=1))

# Compute expectancy table
E_11 = (ctd[0][0] + ctd[0][1]) * (ctd[0][0] + ctd[1][0]) / N
E_12 = (ctd[0][1] + ctd[1][1]) * (ctd[0][1] + ctd[0][0]) / N
E_21 = (ctd[1][0] + ctd[1][1]) * (ctd[1][0] + ctd[0][0]) / N
E_22 = (ctd[1][1] + ctd[1][0]) * (ctd[1][1] + ctd[0][1]) / N
exp = [[E_11, E_12], [E_21, E_22]]
print("Expectancy table: {0}".format(exp))

# Compute chi-squared
X2 = 0
for i in range(0, 2):
	for j in range(0, 2):
		X2 += ((ctd[i][j] - exp[i][j]) ^ 2) / exp[i][j]
print("Chi-squared: {0}".format(X2))