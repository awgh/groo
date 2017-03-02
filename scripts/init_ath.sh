#!/bin/bash

sudo -v
#sudo wlanconfig ath0 destroy
sudo wlanconfig ath1 create wlandev wifi0 wlanmode monitor
sudo ifconfig ath1 up

