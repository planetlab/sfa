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
echo XXXXX Stop a Slice
python ./genicli.py --server $NODE_URL --username test --credfile pltest1.cred --outfile pltest1.cred stopSlice planetlab.us.pl.test1

echo XXXXX -------------------------------------------------------------------
echo XXXXX Start a Slice
python ./genicli.py --server $NODE_URL --username test --credfile pltest1.cred --outfile pltest1.cred startSlice planetlab.us.pl.test1

echo XXXXX -------------------------------------------------------------------
echo XXXXX Reset a Slice
python ./genicli.py --server $NODE_URL --username test --credfile pltest1.cred --outfile pltest1.cred resetSlice planetlab.us.pl.test1
