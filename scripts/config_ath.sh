#!/bin/bash
CHANNEL=$1
airmon-ng stop ath1 > /dev/null 2>&1
airmon-ng start wifi0 $CHANNEL > /dev/null 2>&1
