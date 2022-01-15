#!/usr/bin/env python

#Execution Command: spark-submit PopularityLeagueSpark.py dataset/links/ dataset/league.txt
import sys
from pyspark import SparkConf, SparkContext

conf = SparkConf().setMaster("local").setAppName("PopularityLeague")
conf.set("spark.driver.bindAddress", "127.0.0.1")
sc = SparkContext(conf = conf)

def splitLinks(line):
    line = line.strip()
    pageID, links = line.split(':')
    
    #Get links into a list
    linksList = links.split()
    
    return linksList

lines = sc.textFile(sys.argv[1], 1) 
#TODO
linkList = lines.flatMap(lambda line: splitLinks(line)).map(lambda page: (page, 1))


leagueIds = sc.textFile(sys.argv[2], 1)
#TODO
leagueList = leagueIds.map(lambda line: (line, 1))

unwantedRows = linkList.subtractByKey(leagueList)
wantedRows = linkList.subtractByKey(unwantedRows).reduceByKey(lambda x,y: x+y).collect()
    
output = open(sys.argv[3], "w")
counts = [x[1] for x in wantedRows]
for page, count in wantedRows:
    index = sum([x<count for x in counts])
    line = (page + '\t' + str(index) + '\n')
    output.write(line)
#TODO
#write results to output file. Foramt for each line: (key + \t + value +"\n")

sc.stop()