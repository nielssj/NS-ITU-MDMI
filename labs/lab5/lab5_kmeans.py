import numpy as np
import math
import random

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

def manhattenDistance(a, b):
	return math.fabs(a[0] - b[0]) + math.fabs(a[1] - b[1])

def eucledianDistance(a, b):
	return math.pow(a[0] - b[0], 2) + math.pow(a[1] - b[1], 2)
	
def medoidsClusterize(points, medoids):
	clusters = dict()
	for point in points:
		c_medoid = None
		c_dist = float("inf")
		for medoid in medoids:
			if(point == medoid):
				c_medoid = medoid
				c_dist = 0.0
				break
			dist = manhattenDistance(point, medoid)
			if(dist < c_dist):
				c_medoid = medoid
				c_dist = dist
		if(c_medoid in clusters.keys()):
			clusters[c_medoid].append(point)
		else:
			clusters[c_medoid] = [point]
		print("{0} is closest to {1} with distance {2}".format(point, c_medoid, c_dist))
	return clusters

def medoidCost(clusters):
	cost = 0
	for medoid, cluster in clusters.iteritems():
		for member in cluster:
			cost += manhattenDistance(medoid, member)
	return cost

def kmedoids(points, k):
	#medoids = random.sample(points, k)
	medoids = [(3.0,4.0), (7.0,4.0)]
	print("Initial medoids: {0}".format(medoids))
	clusters = medoidsClusterize(points, medoids)
	print("Initial clusters: {0}".format(clusters))
	cost = medoidCost(clusters)
	print("Initial cost: {0}".format(cost))
	newmedoids = None
	candclusters = None
	candcost = None
	while(not compareCentroids):
		medoids = newmedoids
		clusters = candclusters
		cost = candcost
		# TODO: Do for each medoid
		for candMedoid in points:
			if(candMedoid not in medoids):
				newmedoid = candMedoid
				candMedoids = [medoids[0], newmedoid]
				print("New candidate medoids: {0}".format(candMedoids))
				candclusters = medoidsClusterize(points, candMedoids)
				candcost = medoidCost(candclusters)
				print("candidate cost: {0}".format(candcost))
				if(candcost < cost):
					break # TODO: Continue outer loop intead..

# Example from slides
#seeds = [(2,10), (5,8), (4,9)]
#points = [(2,10),(2,5),(8,4),(5,8),(7,5),(6,4),(4,9),(1,2)]

# Example from web
#seeds = [(1.0,1.0), (5.0,7.0)]
#points = [(1.0,1.0), (1.5,2.0), (3.0,4.0), (5.0,7.0), (3.5,5.0), (4.5,5.0), (3.5,4.5)]

# Example from wiki
points = [(2.0,6.0), (3.0,4.0), (3.0,8.0), (4.0,7.0), (6.0,2.0), (6.0,4.0), (7.0,3.0), (7.0,4.0), (8.0,5.0), (7.0,6.0)]

#kmeans(points,seeds)
kmedoids(points, 2)