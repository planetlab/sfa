#!/bin/bash

source configSfi.sh

rm -f saved_record.*

python ./sfi.py show -o saved_record.$SFI_USER $SFI_USER
python ./sfi.py list -o saved_record.$SFI_AUTH $SFI_AUTH

#rm -f saved_record.*
