# Assumptions:
#    planetlab.us.pl.account_test is a user that exists on the registry
#    planetlab.us.pl.test1 (pl_test1) is a slice that exists on the node

rm -f test.cred
rm -f test.cert
rm -f pltest1.cred

#USERNAME=test
#PARENT_HRN=planetlab.us.pl
#USER_HRN=$PARENT_HRN.account_test

# The following lines use Tony Mack's planetlab account on a live PLC
# database (tony: copy your private key to tmack.pkey in the current directory)
USERNAME=tmack
PARENT_HRN=planetlab.us.princeton
USER_HRN=$PARENT_HRN.Mack_Tony

NODE_URL=https://198.0.0.131:12345/

SA_CRED_FN=rootsa.cred

SLICE_KEY_NAME=testcw
SLICE_KEY_FN=$SLICE_KEY_NAME.pkey

SLICE_NAME=$PARENT_HRN.testcw
SLICE_CRED_NAME=testcw.cred
SLICE_TICKET_NAME=testcw.ticket
SLICE_GID_NAME=testcw.gid

CRED_FN=$USERNAME.cred
CERT_FN=$USERNAME.cert

rm -f $SA_CRED_FN
rm -f $CRED_FN
rm -f $CERT_FN

echo XXXXX -------------------------------------------------------------------
echo XXXXX Getting User Credential
python ./genicli.py --username $USERNAME --credfile None --outfile $CRED_FN getCredential user $USER_HRN

echo XXXXX -------------------------------------------------------------------
echo XXXXX Create a private key
python ./genicli.py --username $SLICE_KEY_NAME createKey

echo XXXXX -------------------------------------------------------------------
echo XXXXX Getting SA Credential
python ./genicli.py --username $USERNAME --outfile $SA_CRED_FN getCredential sa $PARENT_HRN

echo XXXXX -------------------------------------------------------------------
echo XXXXX Create a GID for a slice
python ./genicli.py --username $USERNAME --credfile $SA_CRED_FN --outfile $SLICE_GID_NAME createGid $SLICE_NAME None $SLICE_KEY_FN

echo XXXXX -------------------------------------------------------------------
echo XXXXX If the test slice already exists, Remove the test slice
python ./genicli.py --username $USERNAME --credfile $SA_CRED_FN remove slice $SLICE_NAME

echo XXXXX -------------------------------------------------------------------
echo XXXXX Register a slice
python ./genicli.py --username $USERNAME --credfile $SA_CRED_FN register slice $SLICE_NAME $SLICE_GID_NAME

echo XXXXX -------------------------------------------------------------------
echo XXXXX Get Slice Credential
python ./genicli.py --username $USERNAME --outfile $SLICE_CRED_NAME getCredential slice $SLICE_NAME

echo XXXXX -------------------------------------------------------------------
echo XXXXX Get a Ticket
python ./genicli.py --username $USERNAME --credfile $SLICE_CRED_NAME --outfile $SLICE_TICKET_NAME getTicket $SLICE_NAME

echo XXXXX -------------------------------------------------------------------
echo XXXXX Redeem a Ticket
python ./genicli.py --server $NODE_URL --username $USERNAME --ticketfile $SLICE_TICKET_NAME redeemTicket

echo XXXXX -------------------------------------------------------------------
echo XXXXX Stop a Slice
python ./genicli.py --server $NODE_URL --username $USERNAME --credfile $SLICE_CRED_NAME stopSlice

echo XXXXX -------------------------------------------------------------------
echo XXXXX Start a Slice
python ./genicli.py --server $NODE_URL --username $USERNAME --credfile $SLICE_CRED_NAME startSlice

echo XXXXX -------------------------------------------------------------------
echo XXXXX Reset a Slice
python ./genicli.py --server $NODE_URL --username $USERNAME --credfile $SLICE_CRED_NAME resetSlice

echo XXXXX -------------------------------------------------------------------
echo XXXXX Delete a Slice
python ./genicli.py --server $NODE_URL --username $USERNAME --credfile $SLICE_CRED_NAME deleteSlice

echo XXXXX -------------------------------------------------------------------
echo XXXXX List Slices
python ./genicli.py --server $NODE_URL --username $USERNAME --credfile $SLICE_CRED_NAME listSlices
