import numpy as np
from datetime import datetime
from pytz import timezone

class MovingAverage(object):
    timezone = 'America/New_York'

    # Calculate a moving average. 1 implies no moving average.
    #
    # values Array of values
    # window int The number of points used to generate the moving average. 1 implies no moving average.
    def movingaverage(self, values, window):
        if window == 1:
            return values

        weights = np.repeat(1.0, window) / window
        return np.convolve(values, weights, 'valid')

    # Generate a moving average from the given rawData
    #
    #   rawData = Set of data to work on
    #	window = number or data points to use in M.A. 1 implies no moving average (useful for extracting slices).
    # 	startTimeRel = x*60*1000 - set x to 15; start time 15 mins from beginning
    # 	stopTimeRel = x*60*1000 - set x to 25; 25 mins from beginning (producing 10 minutes of data)
    # returns the new data
    def createMovingAverage(self, rawData, window = 1, startTimeRel = 0, stopTimeRel = 1000000000):
        myTz = timezone(self.timezone)
        numRecords = len(rawData)
        print("Loaded {} records.".format(numRecords))

        first = rawData[0]
        firstTimestamp = first[0]
        print "Found first timestamp: {}".format(firstTimestamp)

        last = rawData[numRecords-1]
        lastTimestamp = last[0]
        print "Found last timestamp: {}".format(lastTimestamp)

        start = startTimeRel + firstTimestamp
        stop = min(firstTimestamp + stopTimeRel, lastTimestamp)
        endDate = datetime.fromtimestamp(stop / 1000.0, myTz)
        startDate = datetime.fromtimestamp(start / 1000.0, myTz)

        print 'Trimming records to start: {} ({}) and stop: {} ({}).'.format(startDate, start, endDate, stop)

        b = [elem for elem in rawData if elem[0] >= start and elem[0] <= stop]
        b = np.array(b)

        x = b[:,0]
        y = b[:,1]

        yMA = self.movingaverage(y, window)
        xMA = x[len(x) - len(yMA):]

        modified_data = np.column_stack((xMA, yMA))

        return (modified_data)
