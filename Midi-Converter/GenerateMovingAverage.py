import fnmatch
import numpy
import argparse
import os
from classes.IOManager import IOManager
from classes.MovingAverage import MovingAverage

parser = argparse.ArgumentParser(description='Apply a moving average to input or extract a slice of time.')
parser.add_argument('-p', '--points', default=1, type=int, help='Default: 1. Specify the number of points to generate the moving average from. Using 1 implies no moving average (1 x 1 = 1) but is useful for extracting slices of time between the start & end points.')
parser.add_argument('-e', '--end', required=True, type=int, help='Required. Specify the end point in seconds. I.e., 30 seconds from the start time.')
parser.add_argument('-s', '--start', required=True, type=int, help='Required. Specify the starting point in seconds. I.e., 90 seconds from the beginning.')
args = parser.parse_args()

manager = IOManager()
movingAverage = MovingAverage()

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
    start = args.start*60*1000
    end = args.end*60*1000

    # Get data
    fileHandle = open(filePath, 'r')
    rawData = [map(int, line.split(',')) for line in fileHandle]
    fileHandle.close()

    print "Create %s point moving average from %s" % (args.points, filePath)
    newFilePath = '%s/%s-%sMA.csv' % (manager.outputRoot, basename, args.points)

    try:
        newData = movingAverage.createMovingAverage(rawData, args.points, start, end)
        numpy.savetxt(newFilePath, newData, fmt='%d', delimiter=',')
        print "Wrote %s" % newFilePath
    except IndexError:
        print "The values have gone out of bounds. Stopping."
        os._exit(1)

print "Done"
