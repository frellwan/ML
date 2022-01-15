#!/usr/bin/env python
import sys
from pyspark import SparkConf, SparkContext
from pyspark.sql import SQLContext, Row

conf = SparkConf().setMaster("local").setAppName("OrphanPages")
conf.set("spark.driver.bindAddress", "127.0.0.1")
sc = SparkContext(conf = conf)
sqlContext = SQLContext(sc) 

linkDict = {}
pageList = []

def splitPageID(line):
    line = line.strip()
    pageID, links = line.split(':')
        
    return str(pageID)

def splitLinks(line):
    line = line.strip()
    pageID, links = line.split(':')
    
    #Get links into a list
    linksList = links.split()
    
    return linksList

def processToDF(line):
    return(Row(pageID=line))

def findOrphans(line):
    global pageList
    global linkDict
    
    pageID, links = line
    linkList = links.split()
    
    if pageID not in pageList:
        pageList.append(pageID)
        
    if pageID in linkDict:
        linkDict[pageID] += 1
    else:
        linkDict[pageID] = 1
        
    for link in linkList:
        if link in linkDict:
            linkDict[link] += 1
        else:
            linkDict[link] = 1

lines = sc.textFile(sys.argv[1], 1) 

#TODO
tokenCount = lines.flatMap(lambda line: splitLinks(line))
#tokenCount.foreach(findOrphans)
pageIDs = lines.map(lambda line: splitPageID(line))
linkList = lines.flatMap(lambda line: splitLinks(line))

orphans = pageIDs.subtract(linkList).collect()
#orphanLinks = links.filter
  #Get links into a list

print("LENGTH\t", len(linkDict))
#print("TYPE\t", type(linkList))

#linkDict = {}
#pageList = []
#for page in pageID[0]:
#    if page not in pageList:
#        pageList.append(page)
#        
#    if page in linkDict:
#        linkDict[page] += 1
#    else:
#        linkDict[page] = 1
 
#Update Link Count
#for link in linksList:
#    if link in linkDict:
#        linkDict[link] += 1
#    else:
#        linkDict[link] = 1

#pageList.sort()
        
#pageIDs = pageID.map(map(processToDF))
#links = link.map(map(processToDF))
#DF1 = sqlContext.createDataFrame(pageIDs)
#DF2 = sqlContext.createDataFrame(links)

orphans.sort()
for i in range(10):
    print(orphans[i])
    
output = open(sys.argv[2], "w")
for page in pageList:
    if (linkDict[page] == 1):
        print(page)
#TODO
#write results to output file. Foramt for each line: (line+"\n")

sc.stop()

