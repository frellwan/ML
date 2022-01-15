#!/usr/bin/env python3
import sys
import math

values = []

for line in sys.stdin:
    line = line.strip()
    word, value = line.split()
    values.append(int(value))
    
sumValue = sum(values)
minValue = min(values)
maxValue = max(values)
     
meanValue = int(sumValue/len(values))
sqerrors = [(x - meanValue)**2 for x in values]
varianceValue = int(sum(sqerrors)/len(sqerrors))

print('%s\t%s' % ('Mean', int(meanValue)))
print('%s\t%s' % ('Sum', int(sumValue)))
print('%s\t%s' % ('Min', int(minValue)))
print('%s\t%s' % ('Max', int(maxValue)))
print('%s\t%s' % ('Var', int(varianceValue)))