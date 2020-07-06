import os
import numpy
import pytz
import csv

from IOManager import IOManager
from collections import OrderedDict
from datetime import datetime

class Compressor(object):
    timezone = 'America/New_York'
    dateTimeStringPattern = '%m-%d-%Y %I:%M:%S'
    outFilePattern = '%s-%dx%s.csv'

    countCheck = 0
    runningTotal = 0
    multiModeRates = [1, 3, 5, 10, 30, 60, 300, 600]

    def compress(self, absFilePath, intervalMilliseconds, zeroFill):
        print 'Begin compression...'

        newData = OrderedDict()
        self.runningTotal = 0

        with open(absFilePath) as handle:
            reader = csv.reader(handle)
            firstLine = reader.next()
            handle.seek(0)

            try:
                print 'Setting boundaries...'
                intervalStart = int(firstLine[0])
                intervalEnd = intervalStart + intervalMilliseconds
                newData[intervalStart] = 0
            except IndexError:
                print 'Nothing to do'
                return None

            for rawTimestamp, rawCount in reader:
                ts = int(rawTimestamp)
                count = int(rawCount)
                self.runningTotal += count

                if ts < intervalEnd:
                    newData[intervalStart] += count
                elif zeroFill == False and ts >= intervalEnd:
                    intervalStart = ts
                    intervalEnd = intervalStart + intervalMilliseconds
                    newData[intervalStart] = count
                else:
                    print 'Zero filling...'
                    # while ts is greater than the intervalEnd, we need to fill each interval with 0, and go
                    # to the next interval
                    while ts >= intervalEnd:
                        intervalStart = intervalEnd
                        intervalEnd = intervalStart + intervalMilliseconds
                        newData[intervalStart] = 0

                    # once here, we have found the proper interval for this count
                    newData[intervalStart] += count

        return newData

    def integrityCheck(self, data):
        print 'Performing integrity check...'
        self.countCheck = 0

        for ts, count in data.iteritems():
            self.countCheck += count
            newDate = datetime.fromtimestamp(ts / 1000, pytz.timezone(self.timezone))
            stringDate = newDate.strftime(self.dateTimeStringPattern)
            # Show what the new timestamps look like
            print stringDate, '--', self.countCheck, '--', self.runningTotal

        return self.runningTotal == self.countCheck

    def compressCheckAndCollapse(self, absFilePath, intervalMilliseconds, zeroFill):
        newData = self.compress(absFilePath, intervalMilliseconds, zeroFill)
        integrityCheck = self.integrityCheck(newData)

        if integrityCheck == True:
            print 'Count is good. Double checked against original input: %d == %d.' % (self.runningTotal, self.countCheck)

            timestampKeys = newData.keys()
            countValues = newData.values()
            collapsedData = numpy.column_stack((timestampKeys, countValues))
            return collapsedData
            # self.write(newData, intervalSeconds, zeroFill, basename)
        else:
            print 'Integrity check failed. Cannot proceed.'
            os._exit(0)
