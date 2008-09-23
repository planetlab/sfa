# Assumptions:
#    planetlab.us.pl.account_test is a user that exists on the registry
#    planetlab.us.pl.test1 (pl_test1) is a slice that exists on the node

rm -f test.cred
rm -f test.cert
rm -f pltest1.cred

NODE_URL=https://198.0.0.131:12345/

echo XXXXX -------------------------------------------------------------------
echo XXXXX Getting User Credential
python ./genicli.py --username test --credfile None --outfile test.cred getCredential user planetlab.us.pl.account_test

echo XXXXX -------------------------------------------------------------------
echo XXXXX Get Slice Credential
python ./genicli.py --username test --outfile pltest1.cred getCredential slice planetlab.us.pl.test1

echo XXXXX -------------------------------------------------------------------
echo XXXXX Get a Ticket
python ./genicli.py --username test --credfile pltest1.cred --outfile pltest1.ticket getTicket planetlab.us.pl.test1

echo XXXXX -------------------------------------------------------------------
echo XXXXX Redeem a Ticket
python ./genicli.py --server $NODE_URL --username test --ticketfile pltest1.ticket redeemTicket

echo XXXXX -------------------------------------------------------------------
echo XXXXX Stop a Slice
python ./genicli.py --server $NODE_URL --username test --credfile pltest1.cred stopSlice

echo XXXXX -------------------------------------------------------------------
echo XXXXX Start a Slice
python ./genicli.py --server $NODE_URL --username test --credfile pltest1.cred startSlice

echo XXXXX -------------------------------------------------------------------
echo XXXXX Reset a Slice
python ./genicli.py --server $NODE_URL --username test --credfile pltest1.cred resetSlice

echo XXXXX -------------------------------------------------------------------
echo XXXXX Delete a Slice
python ./genicli.py --server $NODE_URL --username test --credfile pltest1.cred deleteSlice

echo XXXXX -------------------------------------------------------------------
echo XXXXX List Slices
python ./genicli.py --server $NODE_URL --username test --credfile pltest1.cred --outfile pltest1.cred listSlices

