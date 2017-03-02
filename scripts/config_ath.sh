#!/bin/bash
CHANNEL=$1
IFACE=$2
airmon-ng stop $IFACE > /dev/null 2>&1
airmon-ng start wifi0 $CHANNEL > /dev/null 2>&1
