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
echo XXXXX show users authority
echo XXXXX ------------------------------------------------

python ./sfi.py show $DEMO_PL_AUTH

echo XXXXX ------------------------------------------------
echo XXXXX list available node +rspec+
echo XXXXX ------------------------------------------------

python ./sfi.py nodes

echo XXXXX ------------------------------------------------
echo XXXXX list available node +dns+
echo XXXXX ------------------------------------------------

python ./sfi.py nodes dns

echo XXXXX ------------------------------------------------
echo XXXXX list slices at the aggregate
echo XXXXX ------------------------------------------------

python ./sfi.py slices 


echo XXXXX ------------------------------------------------
echo XXXXX list resources being used by pl_tmack
echo XXXXX ------------------------------------------------

python ./sfi.py resources planetlab.us.pl.tmack




