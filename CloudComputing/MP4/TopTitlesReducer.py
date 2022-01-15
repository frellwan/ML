#!/usr/bin/env python3
import sys

wordDict = {}

# input comes from STDIN
for line in sys.stdin:
    line = line.strip()
    
    word, count = line.split()
    wordDict.update({word:int(count)})
    
#Sort dictionary by frequency and alphabetical if ties
sortedWordDict = sorted(wordDict.items(),key=lambda x:(x[1],x[0]))
outSorted = sorted(sortedWordDict[-10:], key=lambda x:(x[0]))
#Return just the last 10 words - remove the frequency count    
for i in range(10, 0, -1):
    key, value = outSorted[-i]
    print('%s\t%s' % (key, value)) #print as final output