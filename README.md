----
## The Data-to-MIDI Conversion Repository

This houses all files related to data-to-MIDI conversion.

----
## Requirements

Python >= 2.7.10 < 3

----
## Data-to-MIDI Converter

This project is the result of a need to convert time series data to MIDI for use in MoogFest 2017.

This repository holds the scripts that wrap the existing Python MIDI utilities in the midiutil library.

Please see the following repositories for details regarding that specific code:  
[midiutil](https://github.com/duggan/midiutil)  
[MIDITime](https://github.com/cirlabs/miditime)

----
## Overview

### Directory Structure

* MIDI // Store for MIDI files
* Midi-Converter
  + classes
    - Config0001.py // A configuration object used to configure the following converter object.
    - CreateMidiFromData.py // The main converter wrapper/object.
    - IOManager.py // This is a set up utility that sets up the paths to the proper folders.
    - Scales.py // A collection of various scales that can be used to configure the converter.
    - Utilities.py // Some general utilities.
    - Visualize.py // Basic visualization in graph form (slow on larger files).
  + Compress.py // Apply time compression to raw data. I.e., compress 1000 milliseconds into 1 second and add all the counts for those milliseconds.
  + ConvertDataForMiditime.py // Convert a data set to MIDI using a given config.
  + GenerateMovingAverage.py // Apply a moving average to a data set.
  + README.md (this file)
* output // Temporary place for output.
* scripts
* sources // Temporary place for source files

The top-level file _ConvertDataForMiditime.py_ is the interface and should be the only place you need to make settings.

### Data Formatting

The data consumed by MIDITime is expected to be in a certain format. This assumes CSV input files with 2 columns: timestamp & count.

* timestamp = a 13 digit millisecond timestamp

_ConvertDataForMiditime.py_ consumes your data file(s) and builds the appropriate list to pass in to MIDITime.

----
## Usage

1. Copy your raw data files to the _sources_ folder.
2. Make your settings in and then run the following file:

```
$ python ConvertDataForMiditime.py
```

This can start to take A LONG TIME (many hours, even days) if you are importing large files and/or many files but when finished, you will have the complete MIDI file(s) in the destination of your choice.

Once you have your MIDI files you should move them into their respective place in the MIDI folder.
