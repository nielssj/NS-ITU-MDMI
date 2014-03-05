import numpy as np
import math

def distances(tup, centroids):
	dists = []
	for c in centroids:
		dist = math.pow(tup[0] - c[0], 2) + math.pow(tup[1] - c[1], 2)
		dists.append(dist)
	return dists


def clusterize(points, centroids):
	clusters = dict()
	for p in points:
		dists = distances(p, centroids)
		closest = np.argmin(dists)
		if(closest in clusters.keys()):
			clusters[closest].append(p)
		else:
			clusters[closest] = [p]
	return clusters

def computeCentroids(clusters, m):
	means = []
	for cluster in clusters.items():
		sums = dict()
		for point in cluster[1]:
			for i in range(0, m):
				if(i in sums):
					sums[i] = sums[i] + point[i]
				else:
					sums[i] = point[i]
		
		ms = dict()
		for val in sums.items():
			ms[val[0]] = val[1] / len(cluster[1])

		means.append(ms)

	return means

def compareCentroids(cent1, cent2):
	I = len(cent1)
	J = len(cent1[0])
	if(len(cent1) != len(cent2)):
		return False
	for i in range(0, I):
		for j in range(0, J):
			if(cent1[i][j] != cent2[i][j]):
				return False
	return True

def kmeans(points, seeds):
	m = len(points[0])

	# Compute initial cluster using seeds
	clusters = clusterize(points, seeds)
	print(clusters)

	# Compute new means
	means_prev = []
	means = computeCentroids(clusters, m)
	print(means_prev)

	# Continue clusterize and compute means till the centroids don't change
	while(not compareCentroids(means, means_prev)):
		means_prev = means
		clusters = clusterize(points, means)
		means = computeCentroids(clusters, m)
		print(clusters)
		print(means)
	

# Example from slides
seeds = [(2,10), (5,8), (4,9)]
points = [(2,10),(2,5),(8,4),(5,8),(7,5),(6,4),(4,9),(1,2)]

# Example from web
#seeds = [(1.0,1.0), (5.0,7.0)]
#points = [(1.0,1.0), (1.5,2.0), (3.0,4.0), (5.0,7.0), (3.5,5.0), (4.5,5.0), (3.5,4.5)]

kmeans(points,seeds)