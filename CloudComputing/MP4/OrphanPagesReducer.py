#!/usr/bin/env python3
import sys


linkDict = {}
pageList = []

for line in sys.stdin:
  line = line.strip()
  pageID, links = line.split('\t')
  
  #Get links into a list
  linksList = links.split()
  
  if pageID not in pageList:
      pageList.append(pageID)

  if pageID in linkDict:
      linkDict[pageID] += 1
  else:
      linkDict[pageID] = 1
  
  #Update Link Count
  for link in linksList:
      if link in linkDict:
          linkDict[link] += 1
      else:
          linkDict[link] = 1

pageList.sort()
for page in pageList:
    if (linkDict[page] == 1):
        print('%s' % (page))
#emptyKeys = [k for k, link in pageDict.items() if link == []]
#for key in pageDict.keys():
#    print('%s\t%s' % (key, pageDict[key])) #print as final output