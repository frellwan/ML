# -*- coding: utf-8 -*-
"""
Created on Tue Feb 26 11:52:20 2019

@author: ellwanger
"""

import math


class HiearchicalCluster(Object):
    def __init__(self):
        self.S = []
        self.L = []
        self.L1 = []
        self.minDist = []
        self.nNeighbor = []
        self.size = []
        self.d = []
        self.points = []
        self.Q = []
        self.N = 0  # Number data points
        self.K = 0  # Number clusters
        self.M = 0  # Linkage method (0=Single, 1=Complete, 2=Average)

        self._getData()

    def _euclidean(self, p, q):
        # Computes the Euclidean distance between two 2-D arrays.
        # The Euclidean distance between 2-D arrays `p` and `q`, is defined as
        #
        #   sum(|pi-qi|^2)
        distance = math.sqrt((p[0] - q[0]) ** 2 + (p[1] - q[1]) ** 2)
        return distance

    def _calcNeighbor(self, x, y):
        distance = math.inf
        for i in range(x + 1, y):
            d = self.d[x][i]
            if (d < distance):
                nN = i
                mD = d
                distance = d
        return (nN, mD)

    def _calcDistance(self, a, b, x):
        if (self.M == 0):
            return (min(self.d[a][x], self.d[b][x]))
        elif (self.M == 1):
            return (max(self.d[a][x], self.d[b][x]))
        else:
            return (sum((self.size[a] * self.d[a][x]) + (self.size[b] * self.d[b][x])) / (self.size[a] + self.size[b]))

    def findMinDist(self):
        # Find min value in distance matrix excluding the 0's
        # v = min([min([i for i in group if i != 0]) for group in self.d])
        v = math.inf
        for i in range(len(self.d)):
            for j in range(i + 1, len(self.d)):
                dist = self.d[i][j]
                if dist < v:
                    v = dist

        # Find the neighbors for the min point
        for i, x in enumerate(self.d):
            if v in x:
                return (i, x.index(v))

    def _getData(self):
        # Read first line of input whick contains:
        #       N - number of data points(lines) following the first line
        #       K - number of output clusters
        #       M - cluster similarity measure (0=Single, 1=Complete, 2=Average)
        #    self.N, self.K, self.M = [int(x) for x in input().split()]
        self.N = 5
        self.K = 2
        self.M = 0
        self.nNeighbor = [0] * (self.N - 1)
        self.minDist = [math.inf] * (self.N - 1)
        self.size = [1] * self.N
        self.L1 = [0 for x in range(self.N)]
        self.d = [[0 for x in range(self.N)] for y in range(self.N)]

        # Read input data and add cluster number (initially each point is a cluster)
        # for i in range(self.N):
        #    self.points.append([float(x) for x in input().split()])
        #    self.S.append(i)
        #    self.L.append({i})
        self.points = [(51.5217, 30.1140), (27.9698, 27.0568), (10.6233, 52.4207), (122.1483, 6.9586),
                       (146.4236, -41.3457)]
        self.S = [0, 1, 2, 3, 4]
        self.L = [{0}, {1}, {2}, {3}, {4}]

        # Create initial dissimilarity Matrix based on euclidean distance
        for i in range(self.N):
            for j in range(i + 1, self.N):
                self.d[i][j] = self._euclidean(self.points[i], self.points[j])
                self.d[j][i] = self.d[i][j]

        # Create nearest neighbor index and minDist to nearest neighbor
        for i in range(self.N - 1):
            self.nNeighbor[i], self.minDist[i] = self._calcNeighbor(i, self.N)

        self.Q = dict(zip(self.S, self.minDist))

    def generate(self):
        while (len(self.L) > self.K):
            G1, G2 = self.findMinDist()

            # Remove G1 and G2 from L. Add (G1 U G2) to L
            link = []
            for item in range(len(self.L)):
                if (self.L[item].intersection({G1, G2})):
                    link.append(item)

            newL = [self.L[index] for index in link]
            self.L = [x for x in self.L if x not in newL]
            self.L.append(set.union(*newL).union({G1, G2}))

            # calculate new distance matrix
            for x in self.S:
                if (x == G1):
                    self.d[x][G1] = math.inf
                elif (x == G2):
                    self.d[x][G2] = 0
                    self.d[G1][G2] = math.inf
                    self.d[G2][G1] = math.inf
                else:
                    self.d[x][G2] = self._calcDistance(G1, G2, x)
                    self.d[G2][x] = self.d[x][G2]
                    self.d[x][G1] = math.inf
                    self.d[G1][x] = math.inf

            self.S.remove(G1)

        for i in range(len(self.L)):
            for j in self.L[i]:
                self.L1[j] = i
        return self.L1


hc = HiearchicalCluster()
L = hc.generate()
for i in range(len(L)):
    print(L[i])
