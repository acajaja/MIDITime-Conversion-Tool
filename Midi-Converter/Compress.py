import fnmatch
import os
import argparse
import re
import csv

from classes.IOManager import IOManager
from classes.Compressor import Compressor

parser = argparse.ArgumentParser(description='Apply compression to input')
parser.add_argument('-i', '--interval', default=1, type=float, help='Defaults to 1 second. Value in seconds determines the compression level by grouping milliseconds into "interval". Decimal values are ok too: I.e., 0.5')
parser.add_argument('-m', '--multi', action='store_true', help='Default: Off. Turn on multi mode to compress the same file at different rates.')
parser.add_argument('-zf', '--zerofill', action='store_true', help='Defaults to False. If enabled, this will fill missing intervals with 0')
args = parser.parse_args()

manager = IOManager()
intervalSeconds = args.interval
zeroFill = args.zerofill

zeroFillText = 'Off'
zeroFileName = ''

if zeroFill == True:
    zeroFillText = 'On'

if zeroFill == True:
    zeroFileName = '-zerofill'

def writeCompressedData(dest, data):
    print 'Writing to: ', dest
    with open(dest, 'w') as handle:
        writer = csv.writer(handle)
        writer.writerows(data)

# Fire it up!
def main(s):
    for file in os.listdir(manager.sourceRoot):
        # Skip OS files
        if fnmatch.fnmatch(file, '*.csv') == False:
            continue

        absFilePath = os.path.join(manager.sourceRoot, file)
        print 'Loading ', absFilePath
        basename = os.path.splitext(os.path.basename(file))[0]
        pieces = re.search(r'^([0-9]{8}-[a-z]+).*$', basename)
        baseDestName = '%s-Compressed' % pieces.group(1)
        destDir = '%s/%s-CSV' % (manager.outputRoot, baseDestName)
        namePattern = '%s/%s-%sx%s.csv'

        if not os.path.isdir(destDir):
            os.makedirs(destDir)

        compressor = Compressor()

        # While we have the file open, we can generate a range of compression rates
        if args.multi == True:
            for x in compressor.multiModeRates:
                intervalMilliseconds = x * 1000
                print 'Proceeding with compression at %sx with zero fill %s...' % (intervalMilliseconds, zeroFillText)
                compressed = compressor.compressCheckAndCollapse(absFilePath, intervalMilliseconds, zeroFill)
                dest = namePattern % (destDir, baseDestName, x, zeroFileName)
                writeCompressedData(dest, compressed)
        else:
            intervalMilliseconds = s * 1000
            print 'Proceeding with compression at %sx with zero fill %s...' % (intervalMilliseconds, zeroFillText)
            compressed = compressor.compressCheckAndCollapse(absFilePath, intervalMilliseconds, zeroFill)
            dest = namePattern % (destDir, baseDestName, s, zeroFileName)
            writeCompressedData(dest, compressed)

        print 'Done'

if __name__ == "__main__":
    main(intervalSeconds)
