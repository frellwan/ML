# -*- coding: utf-8 -*-
"""
Created on Sun Mar 10 08:38:47 2019

@author: frell
"""
import math
import os
from scipy.special import comb

class ClusterValidation():
    def __init__(self, T, C):
        self.T = T
        self.C = C
        self.N = 0
        self.vM = [[0 for x in range(len(set(self.T)))] for y in range(len(set(self.C)))]
        self.pM = [[0 for x in range(len(set(self.T)))] for y in range(len(set(self.C)))]
        self.Ctotal = [0 for x in range(len(set(self.C)))]
        self.Ttotal = [0 for x in range(len(set(self.T)))]
    
        self._calcM(self.C, self.T)
        
    def _calcM(self, C, T):
        '''Calculate the clustering-partition matrix '''
        values = [[0 for x in range(len(set(self.T)))] for y in range(len(set(self.C)))]
        
        #combine the Cluster and Ground Truth vectors
        Z = zip(self.C, self.T)
        for pair in Z:
            #The cluster partition matrix cell will be the C,T pair comnination
            #e.g. if C=1 and T=2 than it will go to the vM[1][2] cell
            values[pair[0]][pair[1]] += 1
        
        #Calculate the totals for each Cluster Ci-Cn
        totalC = [0 for x in range(len(set(self.C)))]
        for row in range(len(values)):
            totalC[row] = sum(values[row])
            
        #Calculate the totals for each ground truth Ti-Tn
        totalT = [0 for x in range(len(set(self.T)))]
        for col in range(len(values[0])):
            totalT[col] = sum(c[col] for c in values)
            
        #Calculate the normalized value matrix
        self.N = sum(totalC)
        for row in range(len(values)):
            for col in range(len(values[0])):
                self.vM[row][col]=values[row][col]/self.N
        
        #Calculate the normalized Cluster totals
        for i in range(len(set(self.C))):
            self.Ctotal[i] = totalC[i]/self.N
        
        #Calculate the normalized Ground Truth totals
        for i in range(len(set(self.T))):
            self.Ttotal[i] = totalT[i]/self.N
            
        #Calculate the normalized expected value matrix
        for row in range(len(values)):
            for col in range(len(values[0])):
                self.pM[row][col]=self.Ctotal[row]*self.Ttotal[col]
                

    def generateNMI(self):
        ICT = 0
        for x in range(len(self.Ctotal)):
            for y in range(len(self.Ttotal)):
                if ((self.vM[x][y]/self.pM[x][y]) == 0):
                    ICT += 0
                else:
                    ICT += self.vM[x][y]*math.log(self.vM[x][y]/self.pM[x][y], 2)
                
        HC = 0
        for c in range(len(self.Ctotal)):
            if (self.Ctotal[c] == 0):
                HC += 0
            else:
                HC += -1*self.Ctotal[c]*math.log(self.Ctotal[c], 2)

        HT = 0
        for t in range(len(self.Ttotal)):
            if(self.Ttotal[t] == 0):
                HT += 0
            else:
                HT += -1*self.Ttotal[t]*math.log(self.Ttotal[t], 2)
                
        NMI = ICT/math.sqrt(HC*HT)
        
        return NMI
    
    def generateJaccard(self):
        TP = 0
        FN = 0
        FP = 0
        
        for c in range(len(self.Ctotal)):
            for t in range(len(self.Ttotal)):
                if ((self.vM[c][t]*self.N) < 2):
                    TP += 0
                else:
                    TP += comb((self.vM[c][t]*self.N), 2)
    
        for c in range(len(self.Ctotal)):
            if ((self.Ctotal[c]*self.N) < 2):
                FP += 0
            else:
                FP += comb((self.Ctotal[c]*self.N), 2)
        FP = FP-TP
                
        for t in range(len(self.Ttotal)):
            if((self.Ttotal[t]*self.N) < 2):
                FN += 0
            else:
                FN += comb((self.Ttotal[t]*self.N), 2)
        FN = FN-TP
        
        return (TP/(TP+FN+FP))
    
    
    
    

C = []
T = []
newlines=[]
nmi = []
jaccard = []


file = os.path.join('\\','Users','frell','Documents','cs412','partitions.txt')
with open(file) as f:
    for line in f:
        line = line.split() # to deal with blank 
        if line:            # lines (ie skip them)
            line = [int(i) for i in line]
            T.append(line[1])
print(T)

for i in range(5):
    C = []
    textfile = 'clustering_'+str(i+1)+'.txt'
    file = os.path.join('\\','Users','frell','Documents','cs412',textfile)
    with open(file) as f:
        for line in f:
            line = line.split() # to deal with blank 
            if line:            # lines (ie skip them)
                line = [int(i) for i in line]
                C.append(line[1])     
    print(i)

    validation = ClusterValidation(T, C)
    nmi.append(validation.generateNMI())
    jaccard.append(validation.generateJaccard())
    
file = os.path.join('\\','Users','frell','Documents','cs412','scores.txt')
f = open(file, 'w+')
for i in range(5):
    nmiscore = "{:.7f}".format(nmi[i])
    jaccardscore = "{:.7f}".format(jaccard[i])
    writestring = nmiscore + ' ' + jaccardscore + '\n'
    print(writestring)
    f.write(writestring)
f.close()





        
        
            
        