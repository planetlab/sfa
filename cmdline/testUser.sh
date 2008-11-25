# Assumptions
#    1) PLC Wrapper is up and running
#    2) Private key for test user has been copied into $USERNAME.pkey in the
#       current directory. (If this private key has a passphrase, remove it by
#       doing "ssh-keygen -pf <filename>")

# The following lines use a test account. The account has a first name of "test"
# and a last name of "account". The private key should be in the file test.pkey
USERNAME=test
PARENT_HRN=planetlab.us.pl
USER_HRN=$PARENT_HRN.account_test

# The following lines use Scott Baker's planetlab account on a live PLC
# database. Modify these to use the appropriate values
# USERNAME=bakers
# PARENT_HRN=planetlab.us.arizona
# USER_HRN=$PARENT_HRN.Baker_Scott

# The following lines use Tony Mack's planetlab account on a live PLC
# database (tony: copy your private key to tmack.pkey in the current directory)
USERNAME=tmack
PARENT_HRN=planetlab.us.princeton
USER_HRN=$PARENT_HRN.Mack_Tony

PRIVKEY_FN=$USERNAME.pkey
CRED_FN=$USERNAME.cred
CERT_FN=$USERNAME.cert

rm -f $CRED_FN
rm -f $CERT_FN

echo XXXXX -------------------------------------------------------------------
echo XXXXX Getting Credential
python ./genicli.py --username $USERNAME --credfile None --outfile $CRED_FN getCredential user $USER_HRN

echo XXXXX -------------------------------------------------------------------
echo XXXXX Resolving Authority
python ./genicli.py --username $USERNAME resolve $PARENT_HRN

echo XXXXX -------------------------------------------------------------------
echo XXXXX Resolving Self
python ./genicli.py --username $USERNAME resolve $USER_HRN

echo XXXXX -------------------------------------------------------------------
echo XXXXX Update Self
python ./genicli.py --username $USERNAME update user $USER_HRN

