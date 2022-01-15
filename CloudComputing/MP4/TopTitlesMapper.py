#!/usr/bin/env python3
import sys

wordDict = {}

for line in sys.stdin:
    line = line.strip()
    
    word, count = line.split()
    wordDict.update({word:int(count)})

sortedWordDict = sorted(wordDict.items(),key=lambda x:(x[1], x[0]))
outSorted = sorted(sortedWordDict[-10:], key=lambda x:(x[0]))

for i in range(10,0, -1):
    key, value = outSorted[-i]
    print('%s\t%s' % (key, value)) #pass this output to reducer