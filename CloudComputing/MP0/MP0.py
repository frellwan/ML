import random 
import os
import string
import sys
import codecs
import re
import operator

stopWordsList = ["i", "me", "my", "myself", "we", "our", "ours", "ourselves", "you", "your", "yours",
            "yourself", "yourselves", "he", "him", "his", "himself", "she", "her", "hers", "herself", "it", "its",
            "itself", "they", "them", "their", "theirs", "themselves", "what", "which", "who", "whom", "this", "that",
            "these", "those", "am", "is", "are", "was", "were", "be", "been", "being", "have", "has", "had", "having",
            "do", "does", "did", "doing", "a", "an", "the", "and", "but", "if", "or", "because", "as", "until", "while",
            "of", "at", "by", "for", "with", "about", "against", "between", "into", "through", "during", "before",
            "after", "above", "below", "to", "from", "up", "down", "in", "out", "on", "off", "over", "under", "again",
            "further", "then", "once", "here", "there", "when", "where", "why", "how", "all", "any", "both", "each",
            "few", "more", "most", "other", "some", "such", "no", "nor", "not", "only", "own", "same", "so", "than",
            "too", "very", "s", "t", "can", "will", "just", "don", "should", "now"]

delimiters = "[ \t,;.?!\-:@\[\](){}_\*/\n]"

def getIndexes(seed):
    random.seed(seed)
    n = 10000
    number_of_lines = 50000
    ret = []
    for i in range(0,n):
        ret.append(random.randint(0, 50000-1))
    return ret

def process(userID):
    indexes = getIndexes(userID)
    ret = []
    # TODO
    newlines = []
    codecs.getreader('utf-8')(sys.stdin)
    #Read in data
    lines = sys.stdin.readlines()
    
    indexedLines = [lines[i] for i in indexes]
    #Condition data for processing   
    for line in indexedLines:
        #Make words in the line lower case and remove leading and trainling white space
        l = line.lower().strip()
         
        #Split words based on delimiters list
        a = re.split(delimiters, l)

        #remove blank words due to multiple delimiters in a row
        while ("" in a):
            a.remove("")
       
        #Remove any of the stop words
        b = [x for x in a if x not in stopWordsList]
                
        newlines.append(b)
  
    #Create empty dictionary to hold word:wordcount values
    index={}
        
    #Loop through all the list of words to get word counts
    for line in newlines:            
        #Loop through each word of each line
        for word in line:
            if (word in index):
                index[word] += 1
            else:
                index[word] = 1

    #Sort dictionary by frequency and alphabetical if ties
    sorted_x = sorted(index.items(),key=lambda x:(-x[1],x[0]))
    
	#Return just the first 20 words - remove the frequency count
    ret = [x[0] for x in sorted_x[0:20]]
	
    for word in ret:
        print word
	
    
process(sys.argv[1])
