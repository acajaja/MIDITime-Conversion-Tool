class Config0001(object):
    def __init__(self):
        self.ABS_FILE_PATH = None
        self.MIDI_DEFAULT_NOTE_LENGTH = 1
        self.MIDI_DEFAULT_VELOCITY = 90

        self.ROOT_DIR = None
        self.ONE_YEAR_SECONDS = 86400
        self.BPM = 60
        self.BASE_OCTAVE = 1
        self.TOTAL_OCTAVES = 8
        self.REVERSED = False
        self.LOG_OR_LINEAR_SCALE = 'linear'
        self.FILENAME = None
        self.CURRENT_SCALE = None
        self.MY_DATA = None
        self.README_FILE = None

        self.MIDI_MIN = 1
        self.MIDI_MAX = 127
        self.MIDI_NOTE_LENGTH = self.MIDI_DEFAULT_NOTE_LENGTH
        self.MIDI_VELOCITY = self.MIDI_DEFAULT_VELOCITY
        self.MIDI_VELOCITY_MIN = None
        self.MIDI_VELOCITY_MAX = None
        self.MIDI_FILE_PATH = None
        self.RANDOM_MIDI_VELOCITY = False

        self.EVENT_LOW_COUNT = 0
        self.EVENT_HIGH_COUNT = 0

    def getOptions(self):
        return self.__dict__

    def getReversedText(self):
        return '-reversed' if self.REVERSED else ''
