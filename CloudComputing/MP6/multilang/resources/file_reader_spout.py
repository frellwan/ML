# import os
# from os.path import join
from time import sleep

# from streamparse import Spout
import storm


class FileReaderSpout(storm.Spout):

    def initialize(self, conf, context):
        self._conf = conf
        self._context = context
        self._complete = False

        storm.logInfo("Spout instance starting...")

        # TODO:
        # Task: Initialize the file reader
        self._file = open('/tmp/data.txt', 'r')
        # End

    def nextTuple(self):
        # TODO:
        # Task 1: read the next line and emit a tuple for it
        # Task 2: don't forget to sleep for 1 second when the file is entirely read to prevent a busy-loop
        try:
            sentence = self._file.next()
            storm.logInfo("Emiting %s" % sentence)
            storm.emit([sentence])
        except StopIteration:
            sleep(1)
        finally:
            pass
        
        # End


# Start the spout when it's invoked
FileReaderSpout().run()
