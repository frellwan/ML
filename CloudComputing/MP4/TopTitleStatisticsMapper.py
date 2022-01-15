#!/usr/bin/env python3
import sys


for line in sys.stdin:
    line = line.strip()
    word, value = line.split()
    
    print('%s\t%s' % (word, value)) #pass this output to reducer