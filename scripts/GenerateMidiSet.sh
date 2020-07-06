#!/bin/sh

# A batch script to automate generating permutations of MIDI settings.
# This will likely run for a long time depending on how many source files you have so be prepared!

ys=false
bo=""
range=""

while getopts "y:b:r:" myarg
do
  case $myarg in
    y)
      if [[ $OPTARG =~ ^[1-9][0-9]+$ ]]; then
        ys=$OPTARG
      fi
      ;;
    b)
      if [[ $OPTARG =~ ^[1-5]$ ]]; then
        bo=" -bo $OPTARG"
      fi
      ;;
    r)
      if [[ $OPTARG =~ ^[1-7]$ ]]; then
        range=" -r $OPTARG"
      fi
      ;;
    \?)
      echo "Invalid option: -$OPTARG" >&2
      exit 1
      ;;
    :)
      echo "Option -$OPTARG requires an argument." >&2
      exit 1
  esac
done

cd ~/Repositories/moog-fest/Midi-Converter

echo "Converting data using $ys \"year seconds\"\n"

python ConvertDataForMiditime.py -ys $ys -nl 0.1$range$bo
python ConvertDataForMiditime.py -ys $ys -nl 0.5$range$bo
python ConvertDataForMiditime.py -ys $ys -nl 0.8$range$bo
python ConvertDataForMiditime.py -ys $ys -nl 1$range$bo
python ConvertDataForMiditime.py -ys $ys -nl 2$range$bo

python ConvertDataForMiditime.py -ys $ys -nl 0.1 --reverse$range$bo
python ConvertDataForMiditime.py -ys $ys -nl 0.5 --reverse$range$bo
python ConvertDataForMiditime.py -ys $ys -nl 0.8 --reverse$range$bo
python ConvertDataForMiditime.py -ys $ys -nl 1 --reverse$range$bo
python ConvertDataForMiditime.py -ys $ys -nl 2 --reverse$range$bo

python ConvertDataForMiditime.py -ys $ys -nl 0.1 -a log$range$bo
python ConvertDataForMiditime.py -ys $ys -nl 0.5 -a log$range$bo
python ConvertDataForMiditime.py -ys $ys -nl 0.8 -a log$range$bo
python ConvertDataForMiditime.py -ys $ys -nl 1 -a log$range$bo
python ConvertDataForMiditime.py -ys $ys -nl 2 -a log$range$bo

python ConvertDataForMiditime.py -ys $ys -nl 0.1 -a log --reverse$range$bo
python ConvertDataForMiditime.py -ys $ys -nl 0.5 -a log --reverse$range$bo
python ConvertDataForMiditime.py -ys $ys -nl 0.8 -a log --reverse$range$bo
python ConvertDataForMiditime.py -ys $ys -nl 1 -a log --reverse$range$bo
python ConvertDataForMiditime.py -ys $ys -nl 2 -a log --reverse$range$bo

exit 0
