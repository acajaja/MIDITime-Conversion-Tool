#!/bin/sh

function clearSources {
    echo "Clear source dir...
"
    rm -rf ../source/*.csv
}

function moveFileAndZip {
    mv ./*.csv "$1/"
    echo "Zipping files into $1.zip...
"
    zip -r "$1.zip" "$1"
}

#
# Create CSV slices first to generate some files
#
python ../Midi-Converter/ExtractSlices.py -m


cd ../output

# Try to get the date part of the file name to create folder with
# We should only ever bee woring with some sort of day
for file in *.csv
do
  DATE="$(echo $file | sed -n -E 's/^([0-9]{8}).*/\1/p')"
  break
done

#
if [ "$DATE" == "" ]
then
    echo "Cannot determine the date from the CSV file(s) given.
Done.
"
    exit 0
fi

echo "Moving slice files...
"
DIR1="$DATE-Slices-CSV"
mkdir $DIR1
moveFileAndZip $DIR1

#
# Create time-compressed CSV files using the same sources
#
python ../Midi-Converter/Compress.py -m

echo "Moving compressed files...
"
DIR2="$DATE-Compressed-CSV"
mkdir $DIR2
moveFileAndZip $DIR2

exit 0
