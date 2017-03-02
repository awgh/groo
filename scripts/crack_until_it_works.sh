#!/bin/bash

ESSID=$1
BSSID=$2
GROO_ROOT=$3
AIRCRACK=$4

echo "Cracking $ESSID..."

trap "false" SIGTERM

rm -f $GROO_ROOT/logs/$ESSID.log

while [ ! -s $GROO_ROOT/logs/$ESSID.log ]; \
do \

$AIRCRACK -z -e $ESSID $GROO_ROOT/dumps/dump*.cap | \
tee >( \
grep 'KEY FOUND'| \
grep -v '00:00:00:00:00:00:00:00:00:00'| \
tee -a -i $GROO_ROOT/logs/$ESSID.log \
);

done  

echo "SUCCESS"
cp $GROO_ROOT/logs/$ESSID.log $GROO_ROOT/results/$ESSID.log
echo $BSSID >> $GROO_ROOT/results/$ESSID.log
read x
