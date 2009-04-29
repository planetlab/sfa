#!/bin/bash

source configSfi.sh

rm -f saved_record.*

python ./sfi.py show $SFI_USER
python ./sfi.py delegate --user plc.arizona.gackscentral

#rm -f saved_record.*
