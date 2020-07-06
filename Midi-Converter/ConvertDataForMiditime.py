import os
import sys

parent_dirA = os.path.abspath(os.path.dirname(__file__))

sys.path.append(os.path.abspath(os.path.join(parent_dirA, '../vendor')))

import argparse
import fnmatch
import pytz
import csv
import re

from datetime import datetime
from multiprocessing import Pool
from classes.ValidateMidiValue import ValidateMidiValue
from classes.IOManager import IOManager
from classes.Config0001 import Config0001
from classes.CreateMidiFromData import CreateMidiFromData
from classes.Scales import Scales

timezone = 'America/New_York'
delimiter = ','
daysInOneYear = 365.25
oneHourActualSeconds = 3600
oneHalfDayActualSeconds = oneHourActualSeconds * 12 # 43200
threeHoursActualSeconds = oneHalfDayActualSeconds / 2 # 21600
oneDayActualSeconds = oneHourActualSeconds * 24 # 86400
oneWeekActualSeconds = oneDayActualSeconds * 7 # 604800
oneYearActualSeconds = oneDayActualSeconds * daysInOneYear # 31557600
oneMonthActualSeconds = oneYearActualSeconds / 12 # 2629800
sixMonthsActualSeconds = oneYearActualSeconds / 2 # 15778800
years = [threeHoursActualSeconds, oneHalfDayActualSeconds, oneDayActualSeconds, oneWeekActualSeconds, oneMonthActualSeconds, sixMonthsActualSeconds, oneYearActualSeconds]
noteLengths = [0.1, 0.3, 0.5, 0.8, 1, 1.5, 2, 3]
bpms = [30, 60, 80, 120, 180, 240, 320]

parser = argparse.ArgumentParser(formatter_class=argparse.RawDescriptionHelpFormatter,
                                 description='''Convert 1 or more CSV files to MIDI. Simply add your source files to the
'sources' folder and run this script. The results are placed in the 'output'
folder.

This script assumes the following:
    1. Input file(s) are CSV (Comma Separated Values).
    2. Columns should be: timestamp,count.
    3. DO NOT include a header row.
    4. Timestamp should be a millisecond timestamp input for the date/time.''')
parser.add_argument('-c', '--cpus', default=1, type=int, help='Default: 1. The number of workers/CPUs to use, only if multi mode is on.')
parser.add_argument('-m', '--multi', default=False, action='store_true', help='Default: Off. Turn on multi mode and it will generate all permutations of years, note lengths, & bpm.')
parser.add_argument('-ys', '--yearseconds', default=oneDayActualSeconds, type=int, help=('Default: %s. This sets the length of time in seconds of the MIDI container the notes are plotted in.' % oneDayActualSeconds))
parser.add_argument('-bpm', '--beatsperminute', default=120, type=int, help='Default: 120. Set the Beats Per Minute.')
parser.add_argument('-bo', '--baseoctave', default=3, type=int, help='Default: 4. Set the base octave.')
parser.add_argument('-r', '--range', default=4, type=int, help='Default: 3. Set the total range of octaves.')
parser.add_argument('--reverse', dest='isReversed', action='store_true', help='Reverse the vertical direction the MIDI notes are plotted in. I.e., top > bottom instead of bottom > top.')
parser.add_argument('-a', '--algorithm', default='linear', type=str, help='Default: linear. Choose between "linear" or "log". This determines how the notes are plotted in time and space.')
parser.add_argument('-nl', '--notelength', default=1, type=float, help='Default: 1. Set the length of each MIDI note. I.e., 1, 1.1, 0.5')
parser.add_argument('-s', '--scale', default='D_DORIAN', type=str, help='Default: D Dorian. Set the scale to use.')
parser.add_argument('-min', default=1, action=ValidateMidiValue, type=int, help='Default: 1. Set the MIDI minimum base value.')
parser.add_argument('-max', default=127, action=ValidateMidiValue, type=int, help='Default: 127. Set the MIDI maximum value.')
parser.add_argument('-minvel', default=55, action=ValidateMidiValue, type=int, help='Default: 55. Set the minimum note velocity.')
parser.add_argument('-maxvel', default=120, action=ValidateMidiValue, type=int, help='Default: 120. Set the maximum note velocity.')
parser.add_argument('-vel', '--velocity', action=ValidateMidiValue, type=int, help='Set the velocity. *This is required if you are not using the random velocity option.')

args = parser.parse_args()
manager = IOManager()

if args.velocity > 0:
    randomvel = False
else:
    randomvel = True


def populateConfig():
    print 'Populating config object...'
    # Init config object
    config = Config0001()
    config.ROOT_OUTPUT_DIR = manager.outputRoot

    # Customize configuration here
    config.ONE_YEAR_SECONDS = args.yearseconds
    config.BPM = args.beatsperminute
    config.BASE_OCTAVE = args.baseoctave
    config.TOTAL_OCTAVES = args.range
    config.REVERSED = args.isReversed
    config.LOG_OR_LINEAR_SCALE = args.algorithm
    config.CURRENT_SCALE = getattr(Scales, args.scale)
    config.MIDI_MAX = args.max
    config.MIDI_MIN = args.min
    config.MIDI_NOTE_LENGTH = args.notelength
    config.RANDOM_MIDI_VELOCITY = randomvel
    config.MIDI_VELOCITY = args.velocity
    config.MIDI_VELOCITY_MIN = args.minvel
    config.MIDI_VELOCITY_MAX = args.maxvel
    print 'Population complete.'
    return config


def createMidiFilesFromConfig(config):
    if config.ABS_FILE_PATH is None:
        print 'There is no source file path set. Cannot continue.'
        os._exit(0)

    config.MY_DATA = []
    counter = []

    print 'Reading file and formatting for use with MIDITime: ', config.ABS_FILE_PATH

    with open(config.ABS_FILE_PATH) as handle:
        reader = csv.reader(handle)
        for rawTimestamp, rawCount in reader:
            timestamp = int(rawTimestamp) / 1000.0
            newDate = datetime.fromtimestamp(timestamp, pytz.timezone(timezone))
            count = int(rawCount)
            counter.append(count)
            config.MY_DATA.append({'event_date': newDate, 'magnitude': count})

    config.EVENT_LOW_COUNT = min(counter)
    config.EVENT_HIGH_COUNT = max(counter)
    del counter

    print 'Formatting complete.'
    print 'Attempting to create MIDI from config...'
    midiObj = CreateMidiFromData(config)
    midiObj.createMidiFile()
    configOutput = os.path.join(midiObj.outputDest, '%s-README' % midiObj.outFile)
    config.MIDI_FILE_PATH = midiObj.outFilePath
    configData = config.getOptions()

    print 'Writing config to: ', configOutput
    manager.writeConfigToFile(configOutput, configData)
    print 'Done.'


# Otherwise, let's get them
def main():
    if args.multi:
        print '** Running in multi mode. **'
        pool = Pool(args.cpus)

    for fname in os.listdir(manager.sourceRoot):
        # Skip non-csv files
        if not fnmatch.fnmatch(fname, '*.csv'):
            continue

        rawAbsFilePath = os.path.join(manager.sourceRoot, fname)
        baseFilename = os.path.splitext(fname)[0]
        pieces = re.search(r'^([0-9]{8})-([a-z]+)(-([A-Za-z]+))?.*$', baseFilename)
        pieceCount = len(pieces.groups())
        date = pieces.group(1)
        event = pieces.group(2)[0].upper() + pieces.group(2)[1:]
        outFolderName = '%s-%s' % (date, event)

        if pieces.group(3) != None:
            outFolderName += '-%s' % pieces.group(3)

        if pieces.group(4) != None:
            outFolderName += '-%s' % pieces.group(4)

        if args.multi:
            configs = []

            for year in years:
                for bpm in bpms:
                    for noteLength in noteLengths:
                        config = populateConfig()
                        config.ROOT_OUTPUT_DIR = '%s/%s-%d-%d' % (config.ROOT_OUTPUT_DIR, outFolderName, year, bpm)
                        config.ONE_YEAR_SECONDS = year
                        config.ABS_FILE_PATH = rawAbsFilePath
                        config.FILENAME = baseFilename
                        config.MIDI_NOTE_LENGTH = noteLength
                        config.BPM = bpm
                        configs.append(config)

            # run config permutations in process pool
            pool.map(createMidiFilesFromConfig, configs)
        else:
            config = populateConfig()
            config.ROOT_OUTPUT_DIR = '%s/%s-%d-%d' % (config.ROOT_OUTPUT_DIR, outFolderName, config.ONE_YEAR_SECONDS, config.BPM)
            config.ABS_FILE_PATH = rawAbsFilePath
            config.FILENAME = baseFilename
            createMidiFilesFromConfig(config)


if __name__ == "__main__":
    main()
