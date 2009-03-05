#!/bin/bash

source configSfi.sh

CWD=`pwd`

# private key to use when creating GID for new slice
export TEST_KEY=$CWD/testkey.pkey

export TEST_SLICE_GID=$CWD/testslice.gid
export TEST_SLICE_RECORD=$CWD/testslice.record
export TEST_SLICE_HRN=$SFI_AUTH.testslice

echo XXXXX -------------------------------------------------------------------
echo XXXXX Removing the test slice. this will cause an error if the slice does
echo XXXXX not exist -- this error can be ignored
echo XXXXX -------------------------------------------------------------------

python ./sfi.py remove --type slice $TEST_SLICE_HRN

echo XXXXX -------------------------------------------------------------------
echo XXXXX Creating a record for the test slice
echo XXXXX -------------------------------------------------------------------

python ./editRecord.py --hrn $TEST_SLICE_HRN --gidhrn $TEST_SLICE_HRN --gidkeyfile $TEST_KEY --type slice --addresearcher $SFI_USER --outfile $TEST_SLICE_RECORD

echo XXXXX -------------------------------------------------------------------
echo XXXXX Adding the test slice, $TEST_SLICE_HRN
echo XXXXX -------------------------------------------------------------------

python ./sfi.py add $TEST_SLICE_RECORD

echo XXXXX -------------------------------------------------------------------
echo XXXXX The slice should have one researcher, $SFI_USER
echo XXXXX -------------------------------------------------------------------

python ./sfi.py show $TEST_SLICE_HRN

echo XXXXX -------------------------------------------------------------------
echo XXXXX Adding $TEST_USER_2 to the slice researchers
echo XXXXX -------------------------------------------------------------------

python ./editRecord.py --infile $TEST_SLICE_RECORD --outfile $TEST_SLICE_RECORD --addresearcher $TEST_USER_2 --outfile $TEST_SLICE_RECORD

echo XXXXX -------------------------------------------------------------------
echo XXXXX Updating the slice
echo XXXXX -------------------------------------------------------------------

python ./sfi.py update $TEST_SLICE_RECORD

echo XXXXX -------------------------------------------------------------------
echo XXXXX The slice record should now have two users: $SFI_USER, $TEST_USER_2
echo XXXXX -------------------------------------------------------------------

python ./sfi.py show $TEST_SLICE_HRN

