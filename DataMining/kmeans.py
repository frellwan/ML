# -*- coding: utf-8 -*-
"""
Created on Fri Feb 22 10:24:53 2019

@author: ellwanger
"""
#%matplotlib inline
import os
import random
import math
from copy import deepcopy
import numpy as np
import pandas as pd
import csv
from matplotlib import pyplot as plt
plt.rcParams['figure.figsize'] = (16, 9)
plt.style.use('ggplot')

class Kmeans(object):
    def __init__(self, Db, k):
        self.k=k
        self.Data = Db

    # Euclidean Distance Caculator
    def _dist(self, x, Y):
        distance = []
        for i in range(self.k):
            distance.append(math.sqrt(abs((x[0]-Y[i][0])**2+(x[1]-Y[i][1])**2)))
        return distance.index(min(distance))
    
    def _error(self, X, Y):
        error = []
        for i in range(len(X)):
            error.append(math.sqrt(abs((X[i][0]-Y[i][0])**2+(X[i][1]-Y[i][1])**2)))
        return max(error)            
    
    def _print(self):
        file1 = os.path.join('\\','Users','frell','Documents','clusters.txt')
        f1 = open(file1,'w+')

        for i in range(len(self.Data)):
            a = str(i) + " " + str(self.Data[i][2]) + '\n'
            f1.write(a)
        f1.close()
 
    
    def generate(self):
        C = []
        #Generate starting centroids for k clusters
        for i in range(self.k):
            C.append(random.choice(self.Data))
                    
        # To store the value of centroids when it updates
        C_old = [(0,)*2 for _ in range(len(C))]
        # Error func. - Distance between new centroids and old centroids
        error = self._error(C, C_old)
        
        # Loop will run till the error becomes zero
        while error != 0.00:
            clusters = [[] for _ in range(self.k)]
            # Assigning each value to its closest cluster
            for i in range(len(self.Data)):
                index = self._dist(self.Data[i],C)
                clusters[index].append(self.Data[i])
                self.Data[i][2]=index
                
        
                # Storing the old centroid values
            C_old = deepcopy(C)
    
            # Finding the new centroids by taking the average value
            for i in range(self.k):
                #points = [self.Data[j] for j in range(len(self.Data)) if clusters[j] == i]
                #print(clusters[i], len(clusters[i]))
                a = sum([i[0] for i in clusters[i]])/len(clusters[i])
                b = sum([i[1] for i in clusters[i]])/len(clusters[i])
                C[i] = ((a,b))
            
            error = self._error(C, C_old)

            
                
    #print(self.Data.sample(n=3))
    # X coordinates of random centroids
    #C_x = np.random.randint(0, np.max(X)-20, size=k)
    # Y coordinates of random centroids
    #C_y = np.random.randint(0, np.max(X)-20, size=k)
    #C = np.array(list(zip(C_x, C_y)), dtype=np.float32)
    #print(C)

if __name__ == "__main__":

    lines = []
    locations=[]
    freqDict = dict()
    goods = dict()

    file = os.path.join('\\','Users','frell','Documents','Python Scripts','places.txt')
    # Importing the dataset
    with open(file, 'r') as csvFile:
        reader = csv.reader(csvFile)
        for row in reader:
            d = [float(i) for i in row]
            d.append(0)
            locations.append(d)
                
    csvFile.close()
    
    for i in range(3):
        print(random.choice(locations))
    
    #data = pd.read_csv(file, header=None, names=['long', 'lat'])
    #print(data.shape)
    #print(data[0:10])
    #a = data.sample(n=3)
    #print("length", len(data))

    #with open(file) as f:
    #    lines = f.readlines()
        
    #for line in lines:
    #    locations.append(line.split())
  
    #else:
    #    print 'No dataset filename specified, system with exit\n'
    #    sys.exit('System will exit')

    #L1=[['I1'],['I2'],['I3'],['I4'],['I5']]
    #print(newlines[0:5])
    A = Kmeans(locations,3)
    A.generate()
    A._print()
    #minSupport = options.minS
    #minConfidence = options.minC
    #runApriori()
    #printFrequentItemsets()
    #printRules()
