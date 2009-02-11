#!/bin/bash

source configSfi.sh

CWD=`pwd`
DEMO_AUTH='planetlab.us'
DEMO_PL_AUTH='planetlab.us.pl'

echo XXXXX ------------------------------------------------
echo XXXXX list contents of authority
echo XXXXX ------------------------------------------------

python ./sfi.py list $DEMO_PL_AUTH

echo XXXXX ------------------------------------------------
echo XXXXX show contents of authority
echo XXXXX ------------------------------------------------

python ./sfi.py show $DEMO_PL_AUTH


echo XXXXX ------------------------------------------------
echo XXXXX list available node +rspec+
echo XXXXX ------------------------------------------------

python ./sfi.py nodes

echo XXXXX ------------------------------------------------
echo XXXXX list available node +hrn+
echo XXXXX ------------------------------------------------

python ./sfi.py nodes hrn

