rm -f root.cred
rm -f root.cert
rm -f rootsa.cred
rm -f testkey.pkey
rm -f testkey.gid

echo XXXXX -------------------------------------------------------------------
echo XXXXX Getting Self Credential
python ./genicli.py --username root --credfile None --outfile root.cred getCredential user planetlab.us.pl.Administrator_Default

echo XXXXX -------------------------------------------------------------------
echo XXXXX Getting SA Credential
python ./genicli.py --username root --outfile rootsa.cred getCredential sa planetlab.us

echo XXXXX -------------------------------------------------------------------
echo XXXXX Create a private key
python ./genicli.py --username testkey createKey

echo XXXXX -------------------------------------------------------------------
echo XXXXX Create a GID for an authority
python ./genicli.py --username root --credfile rootsa.cred --outfile testauth.gid createGid planetlab.us.testauth None testkey.pkey

echo XXXXX -------------------------------------------------------------------
echo XXXXX Register a slice authority
python ./genicli.py --username root --credfile rootsa.cred register sa planetlab.us.testauth testauth.gid

echo XXXXX -------------------------------------------------------------------
echo XXXXX Register a management authority
python ./genicli.py --username root --credfile rootsa.cred register ma planetlab.us.testauth testauth.gid

echo XXXXX -------------------------------------------------------------------
echo XXXXX Resolve the test slice authority
python ./genicli.py --username root --credfile rootsa.cred resolve planetlab.us.testauth

echo XXXXX -------------------------------------------------------------------
echo XXXXX Remove a the test management authority
python ./genicli.py --username root --credfile rootsa.cred remove ma planetlab.us.testauth

echo XXXXX -------------------------------------------------------------------
echo XXXXX Remove the test slice authority
python ./genicli.py --username root --credfile rootsa.cred remove sa planetlab.us.testauth
