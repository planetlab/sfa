rm -f root.cred
rm -f root.cert
rm -f rootsa.cred
rm -f testkey.pkey
rm -f testkey.gid

echo XXXXX -------------------------------------------------------------------
echo XXXXX Getting Self Credential
python ./genicli.py --username root --credfile None --outfile root.cred getCredential user planetlab.us.pl.Administrator_Default

echo XXXXX -------------------------------------------------------------------
echo XXXXX Resolving Self
python ./genicli.py --username root resolve planetlab.us.pl.account_test

echo XXXXX -------------------------------------------------------------------
echo XXXXX Getting SA Credential
python ./genicli.py --username root --outfile rootsa.cred getCredential sa planetlab.us.pl

echo XXXXX -------------------------------------------------------------------
echo XXXXX List records in an authority
python ./genicli.py --username root --credfile rootsa.cred list

echo XXXXX -------------------------------------------------------------------
echo XXXXX Create a private key
python ./genicli.py --username testkey createKey


echo XXXXX -------------------------------------------------------------------
echo XXXXX Create a GID for a user
python ./genicli.py --username root --credfile rootsa.cred --outfile testuser.gid createGid planetlab.us.pl.testuser None testkey.pkey

echo XXXXX -------------------------------------------------------------------
echo XXXXX Create a GID for a slice
python ./genicli.py --username root --credfile rootsa.cred --outfile testslice.gid createGid planetlab.us.pl.testslice1 None testkey.pkey

echo XXXXX -------------------------------------------------------------------
echo XXXXX Register a user
python ./genicli.py --username root --credfile rootsa.cred --email test1234@test.com register user planetlab.us.pl.testuser testuser.gid

echo XXXXX -------------------------------------------------------------------
echo XXXXX Resolve the test user
python ./genicli.py --username root --credfile rootsa.cred resolve planetlab.us.pl.testuser

echo XXXXX -------------------------------------------------------------------
echo XXXXX Register a slice
python ./genicli.py --username root --credfile rootsa.cred --email test1234@test.com register slice planetlab.us.pl.testslice1 testslice.gid

echo XXXXX -------------------------------------------------------------------
echo XXXXX Remove a user
python ./genicli.py --username root --credfile rootsa.cred remove user planet\
lab.us.pl.testuser
