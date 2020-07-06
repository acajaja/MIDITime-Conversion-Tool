import fnmatch
import numpy
import argparse
import os
import pytz
import re

from datetime import datetime
from classes.IOManager import IOManager
from classes.MovingAverage import MovingAverage

parser = argparse.ArgumentParser(description='Apply a moving average to input or extract a slice of time.')
parser.add_argument('-i', '--interval', default=30, type=int, help='Default: 30 minutes. Specify the number of minutes use for the slice size.')
parser.add_argument('-m', '--multi', action='store_true', help='Default: False. Run in multi mode to generate a set of slice in "multiModeIntervals" (5, 10, 15, 30, 60).')
args = parser.parse_args()

manager = IOManager()
movingAverage = MovingAverage()
multiModeIntervals = [5, 10, 15, 30, 60]
onedayminutes = 1440

def generateAndSave(rawData, interval, basename):
    start = 0
    startCount = 0
    counter = 0
    end = interval * 60 * 1000
    endCount = interval
    # Expecting something like: 20161128-clicks*
    pieces = re.search(r'^([0-9]{8})\-([a-z]+).*', basename)
    destDir = '%s/%s-Slices-CSV/%s/%d' % (manager.outputRoot, pieces.group(1), pieces.group(2), interval)

    if not os.path.isdir(destDir):
        os.makedirs(destDir)

    while counter <= onedayminutes:
        try:
            newData = movingAverage.createMovingAverage(rawData, 1, start, end)
            startCount += interval
            endCount += interval
            start = startCount * 60 * 1000
            end = endCount * 60 * 1000

            newStart = datetime.fromtimestamp(start / 1000.0, pytz.timezone('UTC'))
            stringStartDate = newStart.strftime("%H%M")

            newEnd = datetime.fromtimestamp(end / 1000.0, pytz.timezone('UTC'))
            stringEndDate = newEnd.strftime("%H%M")

            newFilePath = '%s/%s-%s-%s.csv' % (destDir, basename, stringStartDate, stringEndDate)
            numpy.savetxt(newFilePath, newData, fmt='%d', delimiter=',')
            print "Wrote %s" % newFilePath
            counter += interval
        except IndexError:
            print 'The values have gone out of bounds. Stopping.'
            break

def main():
    if args.multi == True:
        print '** Running in Multi Mode **'

    # Otherwise, let's get them
    for file in manager.files:
        # Skip OS files
        if fnmatch.fnmatch(file, '*.csv') == False:
            continue

            # Can't use directories
        absFilePath = os.path.join(manager.sourceRoot, file)
        if os.path.isdir(absFilePath):
            continue

        filePath = '%s/%s' % (manager.sourceRoot, file)
        basename = os.path.splitext(os.path.basename(file))[0]

        # Get data
        fileHandle = open(filePath, 'r')
        rawData = [map(int, line.split(',')) for line in fileHandle]
        fileHandle.close()

        print 'Reading: ', absFilePath

        if args.multi == True:
            for interval in multiModeIntervals:
                print 'Extracting time slices from file at %d minute intervals: %s' % (interval, filePath)
                generateAndSave(rawData, interval, basename)
        else:
            print 'Extracting time slices from file at %d minute intervals: %s' % (args.interval, filePath)
            generateAndSave(rawData, args.interval, basename)

    print "Done"

if __name__ == "__main__":
    main()
