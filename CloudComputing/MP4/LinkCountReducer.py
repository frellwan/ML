#!/usr/bin/env python3
import sys

linkDict = {}

# input comes from STDIN
for line in sys.stdin:
  line = line.strip()
  pageID, links = line.split('\t')
  
  #Get links into a list
  linksList = links.split()
  
  #Add PageId into link count
  if pageID in linkDict:
      linkDict[pageID] += 1
  else:
      linkDict[pageID] = 1
  
  #Update Link Count for 
  for link in linksList:
      if link in linkDict:
          linkDict[link] += 1
      else:
          linkDict[link] = 1

for page, count in linkDict.items():
    print('%s\t%s' % (page, count)) #print as final output