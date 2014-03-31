import itertools

def apriori(trs, st):
	li = generateFreqItemSets1(trs, st)
	li_cur = li
	while(len(li_cur) > 0):
		li = li_cur
		li_cur = generateFreqItemSets(trs, st, li_cur)
	return li

def generateFreqItemSets1(trs, st):
	# Collect support for each item (single-item itemset)
	freqs = dict()
	for tr in trs:
		for item in tr:
			item_t = tuple([item])
			if(item_t in freqs.keys()):
				freqs[item_t] = freqs[item_t] + 1
			else:
				freqs[item_t] = 1
	# Filter item sets lower than support threshold (st)
	freqs_st = filterInfrequent(freqs, st)
	return freqs_st

def countSupport(trs, its):
	freqs = dict()
	for itemset in its:
		for tr in trs:
			mismatch = False
			for item in itemset:
				if(not item in tr):
					mismatch = True
			if(not mismatch):
				if(itemset in freqs.keys()):
					freqs[itemset] = freqs[itemset] + 1
				else:
					freqs[itemset] = 1
	T = float(len(trs))
	pcts = dict()
	for freqkey in freqs.keys():
		pcts[freqkey] = freqs[freqkey] / T
	return pcts

# Return list of rows with a support higher than given threshold
def filterInfrequent(freqs, st):
	freqs_st = []
	for (iset, freq) in freqs.iteritems():
		if(freq >= st):
			freqs_st.append(iset)
	return freqs_st

def generateFreqItemSets(trs, st, li):
	# Determine k
	k = len(li[0])

	# Join step
	candidates = []
	for l1 in li:
		for l2 in li:
			fail = False
			for val in range(0, k-2):
				if(l1[val] != l2[val]):
					fail = True
					break
			if(not l1[k-1] < l2[k-1]):
				fail = True
			if(not fail):
				joined = []
				for i in l1:
					joined.append(i)
				joined.append(l2[k-1])
				candidates.append(tuple(joined))

	print("l{0} candidates: \n\t{1}".format(k+1, candidates))

	# Prune step
	c_pruned = []
	for itemset in candidates:
		invalid = False
		for subset in itertools.combinations(itemset, k):
			if(subset not in li):
				invalid = True
				break
		if(not invalid):
			c_pruned.append(itemset)
	print("l{0} candidates pruned: \n\t{1}".format(k+1, c_pruned))
	
	# Filter lower than threshold
	c_support = countSupport(trs, c_pruned)
	print("l{0} candidates support: \n\t{1}".format(k+1, c_support))
	c_filtered = filterInfrequent(c_support, st)

	return c_filtered