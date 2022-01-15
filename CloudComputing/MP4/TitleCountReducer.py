#!/usr/bin/env python3
from operator import itemgetter
import sys

wordDict = {}

# input comes from STDIN
for line in sys.stdin:
    line = line.strip()
    
    #Get the word and value
    word, count = line.split()

    try:
        count = int(count)
    except ValueError:
        # count was not a number, so silently
        # ignore/discard this line
        continue
    
    if (word in wordDict):
        wordDict[word] += count
    else:
        wordDict[word] = count

# do not forget to output the last word if needed!
for key in wordDict.keys():
    print ('%s\t%s' % (key, wordDict[key]))