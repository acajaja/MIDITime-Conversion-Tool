import os
import sys

from random import randint
from miditime.miditime import MIDITime


class CreateMidiFromData(object):
    # Constants
    MIDI_MIN = 1
    MIDI_MAX = 127
    MIDI_RANGE = MIDI_MAX - MIDI_MIN
    MIDI_DEFAULT_NOTE_LENGTH = 1
    MIDI_DEFAULT_VELOCITY = 90
    OUTPUT_FILE_PATTERN = '%s-%s-%s-%s-%s-%s-%s%s.mid'

    # properties
    config = None
    highestCount = 0
    lowestCount = 0
    noteLength = MIDI_DEFAULT_NOTE_LENGTH
    outFile = None
    outputDest = None
    outFilePath = None
    rawCountRange = 0
    velocity = MIDI_DEFAULT_VELOCITY

    #
    def __init__(self, config):
        self.config = config
        options = self.config.getOptions()
        self.lowestCount = options.get('EVENT_LOW_COUNT')
        self.highestCount = options.get('EVENT_HIGH_COUNT')
        self.rawCountRange = (self.highestCount - self.lowestCount)

        if self.lowestCount >= self.highestCount:
            raise RuntimeError('There is not enough of a range to calculate beats: Low = %d, High = %d' % (self.highestCount, self.lowestCount))

        if options.has_key('MIDI_MAX'):
            self.MIDI_MAX = options.get('MIDI_MAX')
            self.MIDI_RANGE = self.MIDI_MAX - self.MIDI_MIN

        if options.has_key('MIDI_MIN'):
            self.MIDI_MIN = options.get('MIDI_MIN')
            self.MIDI_RANGE = self.MIDI_MAX - self.MIDI_MIN

        if options.has_key('MIDI_NOTE_LENGTH'):
            self.noteLength = options.get('MIDI_NOTE_LENGTH')

        if options.has_key('MIDI_VELOCITY'):
            self.velocity = options.get('MIDI_VELOCITY')

        self.outputDest = options.get('ROOT_OUTPUT_DIR')
        self.outFile = self.OUTPUT_FILE_PATTERN % (
            options.get('FILENAME'), str(options.get('BPM')), str(options.get('ONE_YEAR_SECONDS')),
            str(options.get('BASE_OCTAVE')), str(options.get('TOTAL_OCTAVES')), options.get('LOG_OR_LINEAR_SCALE'), str(self.noteLength), self.config.getReversedText()
        )

        if not os.path.isdir(self.outputDest):
            os.makedirs(self.outputDest)
            print "The output directory '%s' does not exist, will create it." % self.outputDest
            print 'Done.'

        self.outFilePath = os.path.join(self.outputDest, self.outFile)

    # Convert "magnitude" to pitch
    def mag_to_pitch_tuned(self, magnitude):
        c = self.config.getOptions()
        cs = c.get('CURRENT_SCALE')
        # Where does this data point sit in the domain of your data? (I.E. the min magnitude is 3, the max in 5.6).
        # In this case the optional 'True' means the scale is reversed, so the highest value will return the lowest percentage.
        if c.get('LOG_OR_LINEAR_SCALE') == 'linear':
            scale_pct = self.midiTime.linear_scale_pct(self.lowestCount, self.highestCount, magnitude, c.get('REVERSED'))
        elif c.get('LOG_OR_LINEAR_SCALE') == 'log':
            scale_pct = self.midiTime.log_scale_pct(self.lowestCount, self.highestCount, magnitude, c.get('REVERSED'), 'log')

        # Find the note that matches your data point
        note = self.midiTime.scale_to_note(scale_pct, cs.get('scale'))

        # Translate that note to a MIDI pitch
        midi_pitch = self.midiTime.note_to_midi_pitch(note)

        return midi_pitch

    # Convert a value to the MIDI range (0 - 127)
    def convert_to_midi_range(self, value):
        newValue = (((value - self.lowestCount) * self.MIDI_RANGE) / self.rawCountRange) + self.MIDI_MIN
        #print "Convert %s to %s" % (value, newValue)
        return newValue

    # Choose to save the output of self.midiTime.save_midi() or not
    def saveWrapper(self, writeToFile=False, outputMidiFile=None):
        # Output the results of MIDITime
        if writeToFile and outputMidiFile:
            origStdout = sys.stdout
            dumpFile = '%s-raw.txt' % (outputMidiFile)
            handle = open(dumpFile, 'w')
            sys.stdout = handle
            # This outputs the converted data
            self.midiTime.save_midi()
            sys.stdout = origStdout
            handle.close()
        else:
            self.midiTime.save_midi()

        print 'Wrote: ', self.outFile

    # Determine the velocity to use
    def getNoteVelocity(self):
        if self.config.RANDOM_MIDI_VELOCITY:
            velocity = randint(self.config.MIDI_VELOCITY_MIN, self.config.MIDI_VELOCITY_MAX)
        else:
            velocity = self.config.MIDI_VELOCITY

        return velocity

    # Create a MIDITime object, inject our data and output a MIDI file
    def createMidiFile(self):
        c = self.config.getOptions()
        cs = c.get('CURRENT_SCALE')

        # Create MIDITime object
        self.midiTime = MIDITime(c.get('BPM'), self.outFilePath, c.get('ONE_YEAR_SECONDS'), c.get('BASE_OCTAVE'), c.get('TOTAL_OCTAVES'))

        # Convert data
        myData_epoched = [
            {
                'days_since_epoch': self.midiTime.days_since_epoch(d['event_date']),
                'magnitude': d['magnitude']
            }
            for d in c.get('MY_DATA')
        ]
        myData_timed = [
            {
                'beat': self.midiTime.beat(d['days_since_epoch']),
                'magnitude': d['magnitude']
            }
            for d in myData_epoched
        ]

        # Start time of 1st note
        startTime = myData_timed[0]['beat']

        print "Low: %s High: %s" % (self.lowestCount, self.highestCount)

        # Now build note list
        # Python does not have an ordered set, so we must use an ordered map's keys
        noteList = []

        for d in myData_timed:
            noteStart = d['beat'] - startTime
            noteData = (
                noteStart,
                self.mag_to_pitch_tuned(d['magnitude']),
                self.getNoteVelocity(),
                self.noteLength  # duration, in beats
            )

            noteList.append(noteData)

        # Add a track with those notes
        self.midiTime.add_track(noteList)

        # Output the results of MIDITime
        self.saveWrapper()
