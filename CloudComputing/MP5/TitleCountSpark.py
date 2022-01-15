#!/usr/bin/env python

'''Exectuion Command: spark-submit TitleCountSpark.py stopwords.txt delimiters.txt dataset/titles/ dataset/output'''

import sys
from pyspark import SparkConf, SparkContext

def tokenize(line, delimitersList):
    line = line.strip()
    tokens = []
    tokenWord = []

    #Build tokens letter by letter since we can not use re module
    for letter in line:
        if letter in delimitersList:
            if (len(tokenWord) > 0):
                token =  "".join(tokenWord).lower()
                tokens.append(token)
            
                #Reset tokenWord to empty list to get a new word
                tokenWord = []
        else:
            tokenWord.append(letter)
                
    #Get last word on line
    if (len(tokenWord) > 0):
        token = "".join(tokenWord).lower()
        tokens.append(token)
    
    return tokens


stopWordsPath = sys.argv[1]
delimitersPath = sys.argv[2]

with open(stopWordsPath) as f:
    stopWordsList = f.read().split()	#TODO

with open(delimitersPath) as f:
    delimitersList = list(f.read())
    
conf = SparkConf().setMaster("local").setAppName("TitleCount")
conf.set("spark.driver.bindAddress", "127.0.0.1")
sc = SparkContext(conf = conf)



lines = sc.textFile(sys.argv[3],1)

#TODO


tokenCount = lines.flatMap(lambda line: tokenize(line, delimitersList)).filter(lambda word: word not in stopWordsList).map(lambda word: (word, 1))
wordFreq = tokenCount.reduceByKey(lambda x, y: x+y).sortBy(lambda x: x[1], False).take(10)

wordFreq.sort(key=lambda x: x[0])

            

outputFile = open(sys.argv[4],"w")

for item in wordFreq:
    buffer = ('%s\t%s\n' % (item[0], item[1]))
    outputFile.write(buffer)
#TODO
#write results to output file. Foramt for each line: (line +"\n")
#for item in wordFreq:
#    buffer = ('%s\t%s\n'%(item[0], item[1]))
#outputFile.write(wordFreq.map(lambda row: str(row[0]) + "\t" + str(row[1])))
#for item in wordFreq.collect():
#    buffer = ('%s\t%s\n' % (item[0], item[1]))
#    outputFile.write(buffer)
