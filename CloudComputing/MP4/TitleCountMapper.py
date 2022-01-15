#!/usr/bin/env python3

import sys
import string

stopWordsPath = sys.argv[1]
delimitersPath = sys.argv[2]


with open(stopWordsPath) as f:
    #Read StopWords into a list
    stopWordsList = f.read().split()


with open(delimitersPath) as f:
    #Read delimiters into a list
    delimitersList = list(f.read())

for line in sys.stdin:
  
    line = line.strip()
    
    tokens = []
    tokenWord = []
    
    #Build tokens letter by letter since we can not use re module
    for letter in line:
        if letter in delimitersList:
            if (len(tokenWord) > 0):
                token =  "".join(tokenWord).lower()
                
                #Only add to token list if the word is not a stopword
                if (token not in stopWordsList):
                    tokens.append(token)
                
                #Reset tokenWord to empty list to get a new word
                tokenWord = []
        else:
            tokenWord.append(letter)
    
    #Get last word on line
    if (len(tokenWord) > 0):
        token = "".join(tokenWord).lower()
        
        #Only add to token list if the word is not a stopword
        if (token not in stopWordsList):
            tokens.append(token)
            
                
    #Pass this output to the reducer
    for word in tokens:
        print('%s\t%s' % (word, 1))