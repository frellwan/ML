#!/usr/bin/env python
import sys
from pyspark import SparkConf, SparkContext

conf = SparkConf().setMaster("local").setAppName("TopPopularLinks")
conf.set("spark.driver.bindAddress", "127.0.0.1")
sc = SparkContext(conf = conf)

lines = sc.textFile(sys.argv[1], 1) 

#TODO
def splitLinks(line):
    line = line.strip()
    pageID, links = line.split(':')
    
    #Get links into a list
    linksList = links.split()
    
    return linksList


linkList = lines.flatMap(lambda line: splitLinks(line)).map(lambda page: (page, 1)).reduceByKey(lambda x,y: x+y).sortBy(lambda x: x[1], False).take(10)

linkList.sort()

output = open(sys.argv[2], "w")
for i in range(10):
    line = linkList[i][0] + '\t' + str(linkList[i][1]) + '\n'
    output.write(line)
    
#TODO
#write results to output file. Foramt for each line: (key + \t + value +"\n")

sc.stop()