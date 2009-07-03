#!/bin/bash

export PATH=$PATH:/etc/sfa
source sfi_config
CWD=$(pwd)

rm -f saved_record.*

python $(CWD)/sfi.py show -o saved_record.$SFI_USER $SFI_USER
python $(CWD)/sfi.py list -o saved_record.$SFI_AUTH $SFI_AUTH

#rm -f saved_record.*
