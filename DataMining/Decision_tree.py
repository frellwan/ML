# -*- coding: utf-8 -*-
"""
Created on Fri Apr  5 13:55:35 2019

@author: ellwanger
"""

# Run this program on your local python 
# interpreter, provided you have installed 
# the required libraries. 
  
# Importing the required packages 
import os
import numpy as np 
import pandas as pd 
from sklearn.metrics import confusion_matrix 
from sklearn.model_selection import train_test_split 
from sklearn.tree import DecisionTreeClassifier 
from sklearn.metrics import accuracy_score 
from sklearn.metrics import classification_report 
  
# Function importing Dataset 
def importdata(): 
    newlines = []
    labels = []
    attributes = []
    values = []
    
    attributes = [str(x) for x in list(range(128))]
    
    file = os.path.join('\\','Users','frell','Documents','Python Scripts','training.txt')
    # Importing the dataset
    with open(file) as f:
        lines = f.readlines()
        
    for line in lines:
        newlines.append(line.split())

    for line in newlines:
        vals = []
        labels.append(int(line.pop(0)))
        for item in line:
            attr, val = item.split(':')
            vals.append(val)
        values.append(vals)
    
            
    X_train = pd.DataFrame(values, columns = attributes)
    y_train = pd.DataFrame(labels)
        #for item in line:
            #attr, val = (int(x) for x in item.split(':'))
    file = os.path.join('\\','Users','frell','Documents','Python Scripts','testing.txt')
    # Importing the dataset
    newlines = []
    labels = []
    values = []

    with open(file) as f:
        lines = f.readlines()
        
    for line in lines:
        newlines.append(line.split())

    for line in newlines:
        vals = []
        for item in line:
            attr, val = item.split(':')
            vals.append(val)
        values.append(vals)
    
            
    X_test = pd.DataFrame(values, columns = attributes)

    return X_train, y_train, X_test
  
# Function to split the dataset 
def splitdataset(balance_data): 
  
    # Seperating the target variable 
    X = balance_data.values[:, 1:5] 
    Y = balance_data.values[:, 0] 
      
    # Spliting the dataset into train and test 
    X_train, X_test, y_train, y_test = train_test_split(  
    X, Y, test_size = 0.3, random_state = 100) 
      
    return X, Y, X_train, X_test, y_train, y_test 
      
# Function to perform training with giniIndex. 
def train_using_gini(X_train, X_test, y_train): 
  
    # Creating the classifier object 
    clf_gini = DecisionTreeClassifier(criterion = "gini", splitter="best", min_samples_leaf=3) 
  
    # Performing training 
    clf_gini.fit(X_train, y_train) 
    return clf_gini 
      
# Function to perform training with entropy. 
def tarin_using_entropy(X_train, X_test, y_train): 
  
    # Decision tree with entropy 
    clf_entropy = DecisionTreeClassifier( 
            criterion = "entropy", random_state = 100, 
            max_depth = 3, min_samples_leaf = 5) 
  
    # Performing training 
    clf_entropy.fit(X_train, y_train) 
    return clf_entropy 
  
  
# Function to make predictions 
def prediction(X_test, clf_object): 
  
    # Predicton on test with giniIndex 
    y_pred = clf_object.predict(X_test) 
    print("Predicted values:")
    print(y_pred) 
    return y_pred 
      
# Function to calculate accuracy 
def cal_accuracy(y_test, y_pred): 
      
    print("Confusion Matrix: ", 
        confusion_matrix(y_test, y_pred)) 
      
    print ("Accuracy : ", 
    accuracy_score(y_test,y_pred)*100) 
      
    print("Report : ", 
    classification_report(y_test, y_pred)) 
  
# Driver code 
def main(): 
      
    # Building Phase 
    #data = importdata() 
    X_train, y_train, X_test = importdata() 
    clf_gini = train_using_gini(X_train, X_test, y_train) 
    #clf_entropy = tarin_using_entropy(X_train, X_test, y_train) 
      
    # Operational Phase 
    print("Results Using Gini Index:") 
      
    # Prediction using gini 
    y_pred_gini = prediction(X_test, clf_gini) 
    #cal_accuracy(y_test, y_pred_gini) 
      
    print("Results Using Entropy:") 
    # Prediction using entropy 
    #y_pred_entropy = prediction(X_test, clf_entropy) 
    #cal_accuracy(y_test, y_pred_entropy) 
    file = os.path.join('\\','Users','frell','Documents','Python Scripts','result.txt')
    f = open(file, "w")
    for i in range(len(y_pred_gini)):
        s = str(y_pred_gini[i]) + '\n'
        f.write(s)
    f.close()      
      
# Calling main function 
if __name__=="__main__": 
    main() 
    