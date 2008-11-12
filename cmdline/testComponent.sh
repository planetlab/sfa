# Assumptions:
#    planetlab.us.pl.account_test is a user that exists on the registry
#    planetlab.us.pl.test1 (pl_test1) is a slice that exists on the node

rm -f test.cred
rm -f test.cert
rm -f pltest1.cred

NODE_URL=https://198.0.0.131:12345/

SA_CRED_NAME=rootsa.cred

SLICE_KEY_NAME=testcw
SLICE_KEY_FN=$SLICE_KEY_NAME.pkey

SLICE_NAME=planetlab.us.pl.testcw
SLICE_CRED_NAME=testcw.cred
SLICE_TICKET_NAME=testcw.ticket
SLICE_GID_NAME=testcw.gid

echo XXXXX -------------------------------------------------------------------
echo XXXXX Getting User Credential
python ./genicli.py --username test --credfile None --outfile test.cred getCredential user planetlab.us.pl.account_test

echo XXXXX -------------------------------------------------------------------
echo XXXXX Create a private key
python ./genicli.py --username $SLICE_KEY_NAME createKey

echo XXXXX -------------------------------------------------------------------
echo XXXXX Getting SA Credential
python ./genicli.py --username root --outfile $SA_CRED_NAME getCredential sa planetlab.us.pl

echo XXXXX -------------------------------------------------------------------
echo XXXXX Create a GID for a slice
python ./genicli.py --username root --credfile rootsa.cred --outfile $SLICE_GID_NAME createGid $SLICE_NAME None $SLICE_KEY_FN

echo XXXXX -------------------------------------------------------------------
echo XXXXX If the test slice already exists, Remove the test slice
python ./genicli.py --username root --credfile $SA_CRED_NAME remove slice $SLICE_NAME

echo XXXXX -------------------------------------------------------------------
echo XXXXX Register a slice
python ./genicli.py --username root --credfile $SA_CRED_NAME register slice $SLICE_NAME $SLICE_GID_NAME

echo XXXXX -------------------------------------------------------------------
echo XXXXX Get Slice Credential
python ./genicli.py --username test --outfile $SLICE_CRED_NAME getCredential slice $SLICE_NAME

echo XXXXX -------------------------------------------------------------------
echo XXXXX Get a Ticket
python ./genicli.py --username test --credfile $SLICE_CRED_NAME --outfile $SLICE_TICKET_NAME getTicket $SLICE_NAME

echo XXXXX -------------------------------------------------------------------
echo XXXXX Redeem a Ticket
python ./genicli.py --server $NODE_URL --username test --ticketfile $SLICE_TICKET_NAME redeemTicket

echo XXXXX -------------------------------------------------------------------
echo XXXXX Stop a Slice
python ./genicli.py --server $NODE_URL --username test --credfile $SLICE_CRED_NAME stopSlice

echo XXXXX -------------------------------------------------------------------
echo XXXXX Start a Slice
python ./genicli.py --server $NODE_URL --username test --credfile $SLICE_CRED_NAME startSlice

echo XXXXX -------------------------------------------------------------------
echo XXXXX Reset a Slice
python ./genicli.py --server $NODE_URL --username test --credfile $SLICE_CRED_NAME resetSlice

echo XXXXX -------------------------------------------------------------------
echo XXXXX Delete a Slice
python ./genicli.py --server $NODE_URL --username test --credfile $SLICE_CRED_NAME deleteSlice

echo XXXXX -------------------------------------------------------------------
echo XXXXX List Slices
python ./genicli.py --server $NODE_URL --username test --credfile $SLICE_CRED_NAME listSlices
