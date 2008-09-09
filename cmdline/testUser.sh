rm -f test.cred
rm -f test.cert

echo XXXXX -------------------------------------------------------------------
echo XXXXX Getting Credential
python ./genicli.py --username test --credfile None --outfile test.cred getCredential user planetlab.us.pl.account_test

echo XXXXX -------------------------------------------------------------------
echo XXXXX Resolving Self
python ./genicli.py --username test resolve planetlab.us.pl.account_test

echo XXXXX -------------------------------------------------------------------
echo XXXXX Update Self
python ./genicli.py --username test update user planetlab.us.pl.account_test

# XXX - this fails because 'list' is an operation for authorities, and our
#   credential is a user credential
#echo XXXXX -------------------------------------------------------------------
#echo XXXXX List records in an authority
#python ./genicli.py --username test list
