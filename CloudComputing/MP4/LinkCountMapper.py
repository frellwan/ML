#!/usr/bin/env python3
import sys


for line in sys.stdin:
    line = line.strip()
    
    #Get pageID and links
    pageID, links = line.split(':')
    linkList = links.split()
    
    print('%s\t%s' % (pageID, links))