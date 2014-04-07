import itertools
import numpy as np
import pandas as pd
from pandas import *

#trs = [ [1, 2, 3, 4, 5 ], [ 1, 3, 5 ], [ 2, 3, 5 ], [ 1, 5 ], [ 1, 3, 4 ], [ 2, 3, 5 ], [ 2, 3, 5 ], [ 3, 4, 5 ], [ 4, 5 ], [ 2 ], [ 2, 3 ], [ 2, 3, 4 ], [ 3, 4, 5 ] ];

def cartesian(arrays, out=None):
    """
    Generate a cartesian product of input arrays.

    Parameters
    ----------
    arrays : list of array-like
        1-D arrays to form the cartesian product of.
    out : ndarray
        Array to place the cartesian product in.

    Returns
    -------
    out : ndarray
        2-D array of shape (M, len(arrays)) containing cartesian products
        formed of input arrays.

    Examples
    --------
    >>> cartesian(([1, 2, 3], [4, 5], [6, 7]))
    array([[1, 4, 6],
           [1, 4, 7],
           [1, 5, 6],
           [1, 5, 7],
           [2, 4, 6],
           [2, 4, 7],
           [2, 5, 6],
           [2, 5, 7],
           [3, 4, 6],
           [3, 4, 7],
           [3, 5, 6],
           [3, 5, 7]])

    """

    arrays = [np.asarray(x) for x in arrays]
    dtype = arrays[0].dtype

    n = np.prod([x.size for x in arrays])
    if out is None:
        out = np.zeros([n, len(arrays)], dtype=dtype)

    m = n / arrays[0].size
    out[:,0] = np.repeat(arrays[0], m)
    if arrays[1:]:
        cartesian(arrays[1:], out=out[0:m,1:])
        for j in xrange(1, arrays[0].size):
            out[j*m:(j+1)*m,1:] = out[0:m,1:]
    return out

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
	return freqs

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

#result = apriori(trs, 2)
#print("result: {0}".format(resultP))

trs = [[1, 2, 5], [2, 4], [2, 3], [1, 2, 4], [1, 3], [2, 3], [1, 3], [1, 2, 3, 5], [1, 2, 3]]
trs_list = []
for tr in trs:
	trs_list.append(Series(tr))
trsS = Series(trs_list)

def freqApply(x):
	freqs = dict()
	for item in x:
		freqs[item] = 1
	return pd.Series(freqs)

def apriori2(trs):
	# Calculate initial frequency at k = 1
	freq_matrix = trsS.apply(freqApply)
	print("Frequency matrix: \n{0}".format(freq_matrix))
	freqs = freq_matrix.count()  
	print("Frequencies: \n{0}".format(freqs))

	# Filter lower than threshold
	st = 2
	freqs_st = freqs[freqs >= st]
	print("Frequencies filtered: \n{0}".format(freqs_st))

	# Determine k
	k = 2
	#print("k = {0}".format(k))

	#f_keys = np.array([[1, 2, 3], [1, 2, 5], [2, 3, 4]])
	f_keys = np.array([[2, 5], [2, 3], [2, 4], [3, 5], [3, 4], [1, 2], [1, 5], [1, 3], [1, 4], [4, 5]])
	# Create matrix of all combinations
	f_rep = np.repeat(f_keys, k, axis=0)
	f_tile = np.tile(f_keys, (k, 1))
	f_comb = np.hstack((f_tile, f_rep))
	#print(f_comb)

	# Filter to unique pairs
	if(k > 2):
		f_vcomb = np.array(filter(lambda x : x[0:k-2] == x[k:2*k-2] and x[k-1] < x[2*k-1], f_comb))
	else:
		f_vcomb = np.array(filter(lambda x : x[0] == x[2] and x[1] < x[3], f_comb))
	#print(f_vcomb)

	# Remove excess columns (only take right-most value of right join)
	f_cand = np.delete(f_vcomb, range(k,2*k-1), 1)
	#print(f_cand)


	# Generate candidates
	# Join
	#f_keys = freqs_st.keys()
	#f_len = len(f_keys)
	#cs = np.transpose([np.tile(f_keys, f_len), np.repeat(f_keys, f_len)])
	#cs = np.dstack(np.meshgrid(f_keys, f_keys)).reshape(-1, 2)
	#cs_f = np.array(filter(lambda x : x[k-1] < x[k], cs))
	#print("Candidates: \n {0}".format(cs_f))
	
	#cs_test = [[1, 2, 3], [1, 2, 5], [2, 3, 4]]
	# Prune
	#for itemset in cs_test:
	#	cs_test_perm = np.transpose([np.tile(itemset, len(itemset)), np.repeat(itemset, len(itemset))])

	#print("Transposed: {0}".format(cs_test_perm))
	#print(np.array(filter(lambda x : x[k-1] < x[k], cs_test_perm)))
	#print(cs_test_perm[cs_test_perm[k-1] < cs_test_perm[k]]) 	

	#ps = np.transpose([np.tile(cs, len(cs)), np.repeat(trs, len(trs))])
	#print(ps)

apriori2(trsS)
#apriori(trs, 2)