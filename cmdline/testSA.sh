# The following lines use the root account of the MyPLC. This assumes that the
# Administrator_Default has a private key that is located in the file
# root.pkey in the current directory.
#USERNAME=root
#PARENT_HRN=planetlab.us.pl
#USER_HRN=$PARENT_HRN.Administrator_Default

# The following lines use Tony Mack's planetlab account on a live PLC
# database (tony: copy your private key to tmack.pkey in the current directory)
USERNAME=tmack
PARENT_HRN=planetlab.us.princeton
USER_HRN=$PARENT_HRN.Mack_Tony

TEST_USER_HRN=$PARENT_HRN.testuser
TEST_SLICE_HRN=$PARENT_HRN.testslice1
TEST_NODE_HRN=$PARENT_HRN.testnode1

TEST_NODE_IP=198.0.0.133

CRED_FN=$USERNAME.cred
CERT_FN=$USERNAME.cert
SA_CRED_FN=$USERNAME_ma.cred

rm -f $CRED_FN
rm -f $CERT_FN
rm -f $SA_CRED_FN
rm -f testkey.pkey
rm -f testkey.gid

echo XXXXX -------------------------------------------------------------------
echo XXXXX Getting Self Credential
python ./genicli.py --username $USERNAME --credfile None --outfile $CRED_FN getCredential user $USER_HRN

echo XXXXX -------------------------------------------------------------------
echo XXXXX Resolving Self
python ./genicli.py --username $USERNAME resolve $USER_HRN

echo XXXXX -------------------------------------------------------------------
echo XXXXX Getting SA Credential
python ./genicli.py --username $USERNAME --outfile $SA_CRED_FN getCredential sa $PARENT_HRN

echo XXXXX -------------------------------------------------------------------
echo XXXXX List records in an authority
python ./genicli.py --username $USERNAME --credfile $SA_CRED_FN list

echo XXXXX -------------------------------------------------------------------
echo XXXXX Create a private key
python ./genicli.py --username testkey createKey

echo XXXXX -------------------------------------------------------------------
echo XXXXX Create a GID for a user
python ./genicli.py --username $USERNAME --credfile $SA_CRED_FN --outfile testuser.gid createGid $TEST_USER_HRN None testkey.pkey

echo XXXXX -------------------------------------------------------------------
echo XXXXX Create a GID for a slice
python ./genicli.py --username $USERNAME --credfile $SA_CRED_FN --outfile testslice.gid createGid $TEST_SLICE_HRN None testkey.pkey

echo XXXXX -------------------------------------------------------------------
echo XXXXX Create a GID for a node
python ./genicli.py --username $USERNAME --credfile $SA_CRED_FN --outfile testnode.gid createGid $TEST_NODE_HRN None testkey.pkey

echo XXXXX -------------------------------------------------------------------
echo XXXXX Register a user
python ./genicli.py --username $USERNAME --credfile $SA_CRED_FN --email test1234@test.com register user $TEST_USER_HRN testuser.gid

echo XXXXX -------------------------------------------------------------------
echo XXXXX Resolve the test user
python ./genicli.py --username $USERNAME --credfile $SA_CRED_FN resolve $TEST_USER_HRN

echo XXXXX -------------------------------------------------------------------
echo XXXXX Register a slice
python ./genicli.py --username $USERNAME --credfile $SA_CRED_FN register slice $TEST_SLICE_HRN testslice.gid

echo XXXXX -------------------------------------------------------------------
echo XXXXX Resolve the test slice
python ./genicli.py --username $USERNAME --credfile $SA_CRED_FN resolve $TEST_SLICE_HRN

echo XXXXX -------------------------------------------------------------------
echo XXXXX Register a node
python ./genicli.py --username $USERNAME --credfile $SA_CRED_FN --ip $TEST_NODE_IP --dns testnode1.lan register node $TEST_NODE_HRN testnode.gid

echo XXXXX -------------------------------------------------------------------
echo XXXXX Resolve the test node
python ./genicli.py --username $USERNAME --credfile $SA_CRED_FN resolve $TEST_NODE_HRN

echo XXXXX -------------------------------------------------------------------
echo XXXXX Remove the test node
python ./genicli.py --username $USERNAME --credfile $SA_CRED_FN remove node $TEST_NODE_HRN

echo XXXXX -------------------------------------------------------------------
echo XXXXX Remove the test slice
python ./genicli.py --username $USERNAME --credfile $SA_CRED_FN remove slice $TEST_SLICE_HRN

echo XXXXX -------------------------------------------------------------------
echo XXXXX Remove a user
python ./genicli.py --username $USERNAME --credfile $SA_CRED_FN remove user $TEST_USER_HRN
