import os
import copy

class Itemset(object):
    def __init__(self,items):
        self.items = items
        self.maximal = True
        self.support = 0

    def __eq__(self,other):
        if not isinstance(other,Itemset):
            return False
        return self.items == other.items
    def __len__(self):
        return len(self.items)
    def __getitem__(self,key):
        return self.items[key]
    def __iter__(self):
        self.begin = 0
        return self
    def next(self):
        if self.begin >=  len(self.items):
            raise StopIteration
        self.begin = self.begin+1
        return self.items[self.begin-1]

class Apriori(object):
    def __init__(self, Db, minsup=50):
        self.minsup = minsup
        self.f={}
        self.index={}
        self.Db = Db

    def _firstPass(self):
        """Generate 1-itemset candidates"""
    
        for line in self.Db:
            line_dict = {}
            for word in line:
                if (word in self.index):
                    if (word not in line_dict):
                        self.index[word] += 1
                        line_dict[word] = 1
                else:
                    self.index[word] = 1
                    line_dict[word] = 1
                

    def _addWord(self, key, indexPrime):
        """Add additional word to current phrase and determine if it is Frequent"""
        if (type(key) is str):
            key = [key]
        else:
            key = list(key)
            
        for line in self.Db:
            line_dict = {}
            """ Check to see if phrase appears in a review """
            #print(key)
            #print((line[i:i+len(list(key))]) for i in range(len(line)-1))
            if(any(key == line[i:i+len(key)] for i in range(len(line) - 1))):
                #print("True")
                """ find the last item of phrase and see if it is part of phrase """
                """ find the indexes and add the next word """
                """ Enumerate over all occurences in list """
                """ TODO - CHECK FOR LAST ITEM IN LINE """
                occurances = [i for i, n in enumerate(line) if n == key[-1]]
                for index in occurances:
                    """ Is it the correct phrase """
                    if (line[index-(len(key)-1):index+1] == key):
                        newphrase = tuple(line[index-(len(key)-1):index+2])
                        if (newphrase in indexPrime):
                            if (newphrase not in line_dict):
                                indexPrime[newphrase] += 1
                                line_dict[newphrase] = 1
                            else:
                                pass
                        else:
                            indexPrime[newphrase] = 1
                            line_dict[newphrase] = 1

    def generate(self):
        
        self._firstPass()
        
        while(len(self.index)):
            indexPrime = {}
            for key,value in self.index.items():
                if value >= int(self.minsup):
                    self.f.update({key:value})
                    self._addWord(key, indexPrime)
                        
            self.index = copy.deepcopy(indexPrime)   

        file1 = os.path.join('\\','Users','frell','Documents','patterns.txt')
        f1 = open(file1,'w+')

        for key, value in self.f.items():
            a1 = str(value)
            if (type(key) is str):
                a2 = str(key)
            else:
                a2 = ';'.join(key)
            a = str(a1)+':'+str(a2)+'\n'
 
            f1.write(a)
        f1.close()
        
                        

       


if __name__ == "__main__":

    lines = []
    newlines=[]
    freqDict = dict()
    goods = dict()

    #optparser = OptionParser()
    #optparser.add_option('-i', '--inputDatabase', dest = 'input', help = 'the filename which contains the comma separated values',default = None)
    #optparser.add_option('-g', '--goods', dest = 'good', help = 'the file specifying the goods',default = None)
    #optparser.add_option('-s', '--minSupport', dest='minS', help = 'minimum support value(default=0.15)', default=0.03, type='float')
    #optparser.add_option('-c','--minConfidence', dest='minC', help = 'minimum confidence value(default = 0.6)', default = 0.5, type='float')

    #(options, args) = optparser.parse_args()

    #if options.input is not None:
    file = os.path.join('\\','Users','frell','Documents','Python Scripts','reviews.txt')
    with open(file) as f:
        lines = f.readlines()
        
    for line in lines:
        newlines.append(line.split())
  
    #else:
    #    print 'No dataset filename specified, system with exit\n'
    #    sys.exit('System will exit')

    #L1=[['I1'],['I2'],['I3'],['I4'],['I5']]
    #print(newlines[0:5])
    A = Apriori(newlines,100)
    A.generate()
    #minSupport = options.minS
    #minConfidence = options.minC
    #runApriori()
    #printFrequentItemsets()
    #printRules()
