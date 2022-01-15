#!/usr/bin/env python
import sys
from pyspark import SparkConf, SparkContext


conf = SparkConf().setMaster("local").setAppName("TopTitleStatistics")
conf.set("spark.driver.bindAddress", "127.0.0.1")
sc = SparkContext(conf = conf)
                  
lines = sc.textFile(sys.argv[1],1)

wordList = lines.flatMap(lambda line: line.split("\t")).collect()
values = wordList[1::2]
values = [int(i) for i in values] 

sumValue = sum(values)
minValue = min(values)
maxValue = max(values)
     
meanValue = int(sumValue/len(values))
sqerrors = [(x - meanValue)**2 for x in values]
varianceValue = int(sum(sqerrors)/len(sqerrors))

outputFile = open(sys.argv[2],"w")
#TODO write your output here
#write results to output file. Format
outputFile.write('Mean\t%s\n' % meanValue)
outputFile.write('Sum\t%s\n' % sumValue)
outputFile.write('Min\t%s\n' % minValue)
outputFile.write('Max\t%s\n' % maxValue)
outputFile.write('Var\t%s\n' % varianceValue)

sc.stop()

