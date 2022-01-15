import heapq
from collections import Counter

import storm


class TopNFinderBolt(storm.BasicBolt):
    # Initialize this instance
    def initialize(self, conf, context):
        self._conf = conf
        self._context = context

        storm.logInfo("TopNFinder bolt instance starting...")

        # TODO:
        # Task: set N
        self.N = 10
        # End

        # Hint: Add necessary instance variables and classes if needed
        self._maxHeap = []
        self._counter = Counter()

    def process(self, tup):
        '''
        TODO:
        Task: keep track of the top N words
        Hint: implement efficient algorithm so that it won't be shutdown before task finished
              the algorithm we used when we developed the auto-grader is maintaining a N size min-heap
        '''
        if tup.values[0] not in self._counter and tup.values[0] != "":
<<<<<<< HEAD
            storm.logInfo("TopN not in counter [%s:%s]" % (tup.values[0], tup.values[1]))
            if len(self._maxHeap) < self.N:
                heapq.heappush(self._maxHeap, [int(tup.values[1]), tup.values[0]])
                self._counter[tup.values[0]] = int(tup.values[1])
                storm.logInfo("TopN heap not full [%s:%s]" % (tup.values[0], tup.values[1]))
                
            elif int(tup.values[1]) > self._maxHeap[0][0]:
                count, word = heapq.heappop(self._maxHeap)
                if int(tup.values[1]) > self._counter[word]:
                    del self._counter[word]
                    self._counter[tup.values[0]] = int(tup.values[1])
                    heapq.heappush(self._maxHeap, [int(tup.values[1]), tup.values[0]])
                    storm.logInfo("TopN heap full > [%s:%s]  [%s:%s]" % (tup.values[0], tup.values[1], word, count))
                else:
                    heapq.heappush(self._maxHeap, [self._counter[word], word])
                    storm.logInfo("TopN heap full < [%s:%s] [%s:%s]" % (tup.values[0], tup.values[1], word, count))
        elif tup.values[0] != "":
            storm.logInfo("TopN in counter [%s:%s]" % (tup.values[0], tup.values[1]))
            self._counter[tup.values[0]] = int(tup.values[1])
            storm.logInfo("TopN update count [%s:%s]" % (tup.values[0], tup.values[1]))
=======
            if len(self._maxHeap) < self.N:
                heapq.heappush(self._maxHeap, [int(tup.values[1]), tup.values[0]])
                self._counter[tup.values[0]] = int(tup.values[1])
                
            elif int(tup.values[1]) > self._maxHeap[0][0]:
                count, word = heapq.heappushpop(self._maxHeap, [int(tup.values[1]), tup.values[0]])
                if int(tup.values[1]) > self._counter[word]:
                    del self._counter[word]
                    self._counter[tup.values[0]] = int(tup.values[1])
                else:
                    heapq.heappushpop(self._maxHeap, [self._counter[word], word])
                
        else:
            self._counter[tup.values[0]] = int(tup.values[1])
>>>>>>> 1f566f4389eb45b2c157c714846f88b3c64d13f8
            
        maxList = []
        for i in range(len(self._maxHeap)):
            maxList.append(self._maxHeap[i][1])
        
        storm.logInfo("Emitting Heap [%s:%s]" % ('top-N', ", ".join(maxList)))
        storm.emit(["top-N", ", ".join(maxList)])
            
        # End

# Start the bolt when it's invoked
TopNFinderBolt().run()
