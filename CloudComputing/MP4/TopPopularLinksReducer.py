#!/usr/bin/env python3
import sys

pageDict = {}

# input comes from STDIN
for line in sys.stdin:
    line = line.strip()
    
    page, count = line.split()
    pageDict.update({page:int(count)})
    
#Sort dictionary by frequency and alphabetical if ties
sortedPageDict = sorted(pageDict.items(),key=lambda x:(x[1],x[0]))
outSorted = sorted(sortedPageDict[-10:], key=lambda x:(x[0]))
#Return just the last 10 words - remove the frequency count    
for i in range(10, 0, -1):
    key, value = outSorted[-i]
    print('%s\t%s' % (key, value)) #print as final output