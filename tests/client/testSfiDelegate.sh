#!/bin/bash

export PATH=$PATH:/etc/sfa
source sfi_config
CWD=$(pwd)

rm -f saved_record.*

python $(CWD)/sfi.py show $SFI_USER
python $(CWD)/sfi.py delegate --user plc.arizona.gackscentral

#rm -f saved_record.*
